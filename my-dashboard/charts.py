import plotly.express as px
 
stocks = px.data.stocks()   # built-in dataset: ships with plotly
 
fig = px.line(
    stocks, x='date', y='GOOG',
    title='Google Stock Price (Normalised)',
    markers=True, template='plotly_white'
)
fig.update_traces(line=dict(width=2.5, color='#00B4D8'))
fig.show()