import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
 
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ]
)
def get_ohlcv(ticker: str, period: str = '6mo') -> pd.DataFrame:
    """Download OHLCV price history for one ticker.
 
    Returns a DataFrame with Date, Open, High, Low, Close and
    Volume columns, with single-level (flattened) headers.
    """
    # Download raw price history from Yahoo Finance.
    df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
    df.reset_index(inplace=True)
    # Flatten any MultiIndex columns to plain names.
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    return df
 
def get_multi(tickers: list, period: str = '6mo') -> pd.DataFrame:
    """Fetch Close prices for several tickers, indexed to 100.
 
    Returns a long DataFrame (Date, Close, Ticker, Return),
    where Return indexes each series to 100 at its first date.
    """
    frames = []
    for t in tickers:
        # Keep only Date and Close for this ticker.
        d = get_ohlcv(t, period)[['Date','Close']]
        d['Ticker'] = t
        # Index to 100 at day one for easy comparison.
        d['Return'] = d['Close'] / d['Close'].iloc[0] * 100
        frames.append(d)
    return pd.concat(frames)

def candlestick_fig(df, ticker):
    """Build a candlestick + volume figure for one ticker.
 
    Adds 20/50-day moving averages and Bollinger Bands, and
    returns a 2-row Plotly Figure (price top, volume bottom).
    """
    # Moving averages and Bollinger Band levels.
    df['MA20']  = df['Close'].rolling(20).mean()
    df['MA50']  = df['Close'].rolling(50).mean()
    df['STD20'] = df['Close'].rolling(20).std()
    df['Upper'] = df['MA20'] + 2 * df['STD20']
    df['Lower'] = df['MA20'] - 2 * df['STD20']
 
    # Two stacked panels: price (top), volume (bottom).
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.75, 0.25], vertical_spacing=0.03)
 
    fig.add_trace(go.Candlestick(
        x=df['Date'], open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name=ticker,
        increasing_line_color='#00B4D8',
        decreasing_line_color='#E05A2B'
    ), row=1, col=1)
 
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name='MA20',
        line=dict(color='yellow', width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], name='MA50',
        line=dict(color='orange', width=1.5, dash='dot')), row=1, col=1)
 
    colours = ['#00B4D8' if c >= o else '#E05A2B'
               for c, o in zip(df['Close'], df['Open'])]
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'],
                         marker_color=colours, name='Volume'), row=2, col=1)
 
    # Dark theme, no rangeslider, unified hover.
    fig.update_layout(template='plotly_dark',
                      xaxis_rangeslider_visible=False,
                      title=f'{ticker} - Price & Volume',
                      height=550, hovermode='x unified')
    return fig


app.layout = dbc.Container([
    dcc.Interval(id='timer', interval=60_000, n_intervals=0),
 
    dbc.Row([
        dbc.Col(html.H2([
            html.I(className='fa-solid fa-chart-line me-2 text-info'),
            'Financial Market Monitor'
        ], className='mt-3'), md=5),
        dbc.Col(dbc.Input(id='ticker-input', value='AAPL',
                          debounce=True, placeholder='Ticker...', className='mt-3'), md=2),
        dbc.Col(dcc.Dropdown(id='period-dd',
            options=[{'label':l,'value':v} for l,v in
                [('1M','1mo'),('3M','3mo'),('6M','6mo'),('1Y','1y'),('2Y','2y')]],
            value='6mo', clearable=False, className='mt-3'), md=2),
        dbc.Col(dbc.Badge([
            html.I(className='fa-solid fa-circle-dot me-1'),
            ' LIVE'
        ], color='success', className='mt-4 fs-6'), md=2),
    ]),
 
    dbc.Row([dbc.Col(dcc.Graph(id='candle-chart'), md=12)], className='mt-2'),
 
    dbc.Row([
        dbc.Col([
            html.Label([
                html.I(className='bi bi-arrow-left-right me-1'),
                'Compare Tickers (comma-separated):'
            ]),
            dbc.Input(id='multi-input', value='AAPL,MSFT,GOOGL', debounce=True),
        ], md=6),
    ], className='mt-3'),
 
    dbc.Row([dbc.Col(dcc.Graph(id='compare-chart'), md=12)], className='mt-2'),
], fluid=True)


# Rebuild the candlestick chart. Triggers every 60s (the timer)
# and whenever the ticker or period changes.
@callback(
    Output('candle-chart', 'figure'),
    Input('timer', 'n_intervals'),
    Input('ticker-input', 'value'),
    Input('period-dd', 'value'),
)
def refresh_candle(n, ticker, period):
    df = get_ohlcv(ticker or 'AAPL', period or '6mo')
    return candlestick_fig(df, ticker or 'AAPL')
 
# Redraw the comparison chart when tickers or period change.
@callback(
    Output('compare-chart', 'figure'),
    Input('multi-input', 'value'),
    Input('period-dd', 'value'),
)
def refresh_compare(tickers_str, period):
    tickers = [t.strip().upper() for t in (tickers_str or 'AAPL').split(',')][:4]
    df = get_multi(tickers, period or '6mo')
    return px.line(df, x='Date', y='Return', color='Ticker',
                   title='Normalised Returns (base 100)',
                   template='plotly_dark')
 
if __name__ == '__main__':
    app.run(debug=True)