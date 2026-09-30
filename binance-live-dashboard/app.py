"""Binance live dashboard built on Dash 4 WebSocket callbacks.
 
One async callback per browser connection opens the Binance
stream and pushes every update straight to the page. No thread,
no polling, no shared global state.
"""
import json
import time
from collections import deque
 
import dash
from dash import dcc, html, callback, ctx, set_props
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.graph_objects as go
# websockets (plural): the async client that talks to Binance.
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed
 
# backend='fastapi' gives Dash an async server, and
# websocket_callbacks=True runs callbacks over a persistent
# connection so set_props can push updates as they happen.
app = dash.Dash(
    __name__,
    backend='fastapi',
    websocket_callbacks=True,
    external_stylesheets=[
        dbc.themes.CYBORG,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],
)
server = app.server   # uvicorn app:server in production
 
 
def binance_url(symbol: str) -> str:
    """Combined stream URL: trades, 1-minute candles and ticker."""
    s = f'{symbol}@trade/{symbol}@kline_1m/{symbol}@ticker'
    return f'wss://stream.binance.com:9443/stream?streams={s}'
 
 
def kpi_card(title: str, value: str, color: str, icon: str) -> dbc.Card:
    """One small stat card with an icon, used for the ticker row."""
    return dbc.Card(dbc.CardBody([
        html.Div([html.I(className=f'{icon} me-2'), title],
                 className='text-muted small'),
        html.H4(value, style={'color': color}, className='mb-0'),
    ]), className='shadow-sm')
 
 
def ticker_cards(t: dict) -> list:
    """Build the four KPI cards from the latest 24h ticker dict."""
    price, change = t.get('price', 0), t.get('change', 0)
    color = '#00B4D8' if change >= 0 else '#E05A2B'
    arrow = ('fa-solid fa-caret-up' if change >= 0
             else 'fa-solid fa-caret-down')
    return [
        dbc.Col(kpi_card('Price', f'${price:,.2f}', color,
                         'fa-solid fa-dollar-sign'), md=3),
        dbc.Col(kpi_card('24h Change', f'{change:+.2f}%', color,
                         arrow), md=3),
        dbc.Col(kpi_card('24h High', f'${t.get("high", 0):,.2f}',
                         '#28a745', 'bi bi-graph-up'), md=3),
        dbc.Col(kpi_card('24h Volume', f'{t.get("volume", 0):,.0f}',
                         '#6C63FF', 'bi bi-bar-chart-fill'), md=3),
    ]
 
 
def candle_fig(candles: list, sym: str) -> go.Figure:
    """Candlestick figure from the rolling list of 1-minute candles."""
    fig = go.Figure()
    if not candles:
        fig.update_layout(template='plotly_dark',
                          title='Waiting for data...')
        return fig
    cdf = pd.DataFrame(candles)
    fig.add_trace(go.Candlestick(
        x=cdf['time'], open=cdf['open'], high=cdf['high'],
        low=cdf['low'], close=cdf['close'],
        increasing_line_color='#00B4D8',
        decreasing_line_color='#E05A2B'))
    fig.update_layout(template='plotly_dark',
                      title=f'{sym} - 1-Minute Candles',
                      xaxis_rangeslider_visible=False, height=480)
    return fig

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2([
            html.I(className='fa-brands fa-bitcoin me-2 text-warning'),
            'Binance Live Dashboard'
        ], className='mt-3'), md=6),
        dbc.Col(dcc.Dropdown(
            id='symbol-dd',
            options=[
                {'label': 'BTC/USDT', 'value': 'btcusdt'},
                {'label': 'ETH/USDT', 'value': 'ethusdt'},
                {'label': 'SOL/USDT', 'value': 'solusdt'},
                {'label': 'BNB/USDT', 'value': 'bnbusdt'},
            ],
            value='btcusdt', clearable=False, className='mt-3'),
            md=3),
        dbc.Col(dbc.Badge([
            html.I(className='fa-solid fa-circle-dot me-1'),
            ' STREAMING'
        ], color='success', className='mt-4 fs-6'), md=2),
    ]),
 
    # Filled by set_props from the stream callback below.
    dbc.Row(id='ticker-cards', className='mt-3 g-3'),
 
    dbc.Row([
        dbc.Col(dcc.Graph(id='candle-chart'), md=8),
        dbc.Col([
            html.H5([
                html.I(className='bi bi-activity me-2 text-info'),
                'Live Trades'
            ], className='mt-2'),
            dag.AgGrid(
                id='trades-grid',
                columnDefs=[
                    {'field': 'side', 'width': 80,
                     'cellStyle': {'function':
                        "params.value==='BUY' ? "
                        "{color:'#00B4D8',fontWeight:'bold'} : "
                        "{color:'#E05A2B',fontWeight:'bold'}"}},
                    {'field': 'price', 'width': 130,
                     'valueFormatter': {'function':
                        'd3.format(",.2f")(params.value)'}},
                    {'field': 'qty', 'width': 110,
                     'valueFormatter': {'function':
                        'd3.format(".4f")(params.value)'}},
                ],
                rowData=[],
                defaultColDef={'resizable': True},
                style={'height': '480px'},
            )
        ], md=4),
    ], className='mt-3'),
], fluid=True)


@callback(persistent=True)
async def stream():
    """Run for the life of each browser connection.
 
    Opens the Binance stream for the chosen symbol and pushes
    every update straight to the page with set_props. Reconnects
    if the socket drops, and switches streams when the dropdown
    changes.
    """
    ws = ctx.websocket
    while not ws.is_shutdown:
        # A persistent callback has no Input arguments, so it asks
        # the page for the dropdown's value. None on first load
        # (nothing chosen yet) falls back to BTC/USDT.
        symbol = await ws.get_prop('symbol-dd', 'value') or 'btcusdt'
        sym = symbol.upper()
        # A deque with maxlen=50 keeps only the 50 latest trades:
        # the oldest drops off by itself when a new one is added.
        trades = deque(maxlen=50)     # newest trade first
        candles = {}                  # open time -> candle
        last_check = last_push = time.monotonic()
        switched = False
 
        # Each turn of this loop is one connection. If Binance drops
        # it, connect() opens a new one and the loop carries on.
        async for binance in connect(binance_url(symbol)):
            try:
                async for raw in binance:   # one turn per message
                    if ws.is_shutdown:
                        return
                    # Combined streams wrap each event under 'data'.
                    data = json.loads(raw)['data']
                    event = data.get('e')  # which stream sent it
 
                    if event == 'trade':  # one executed trade
                        trades.appendleft({
                            # m: buyer was the maker, so a sell
                            'side': 'SELL' if data['m'] else 'BUY',
                            'price': float(data['p']),
                            'qty': float(data['q']),
                        })
                        # Trades arrive many times a second, so
                        # push the grid at most four times a second.
                        if time.monotonic() - last_push > 0.25:
                            last_push = time.monotonic()
                            set_props('trades-grid',
                                      {'rowData': list(trades)})
 
                    elif event == 'kline':  # 1-minute candle
                        k = data['k']
                        # Keyed by open time, so the live candle
                        # updates in place until it closes.
                        candles[k['t']] = {
                            'time': pd.to_datetime(k['t'], unit='ms'),
                            'open': float(k['o']),
                            'high': float(k['h']),
                            'low': float(k['l']),
                            'close': float(k['c']),
                        }
                        if len(candles) > 120:      # keep last 2 hours
                            del candles[min(candles)]
                        # redraw the chart with all candles so far
                        set_props('candle-chart', {
                            'figure': candle_fig(list(candles.values()),
                                                 sym)})
 
                    elif event == '24hrTicker':  # 24-hour summary
                        ticker = {
                            'price': float(data['c']),    # last price
                            'change': float(data['P']),  # % change, 24h
                            'high': float(data['h']),     # 24h high
                            'low': float(data['l']),      # 24h low
                            'volume': float(data['v']),   # 24h volume
                        }
                        # rebuild the four KPI cards
                        set_props('ticker-cards',
                                  {'children': ticker_cards(ticker)})
 
                    # Once a second, see if the user picked a new coin.
                    if time.monotonic() - last_check > 1:
                        last_check = time.monotonic()
                        try:
                            picked = await ws.get_prop('symbol-dd',
                                                       'value')
                        except TimeoutError:
                            continue      # browser busy; retry later
                        if picked and picked != symbol:
                            switched = True
                            break
            except ConnectionClosed:
                continue          # let the outer loop reconnect
            if switched or ws.is_shutdown:
                break             # leave the reconnect loop too
 
 
if __name__ == '__main__':
    app.run(debug=True)