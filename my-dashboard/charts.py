import plotly.express as px
stocks = px.data.stocks()   # built-in dataset: ships with plotly
gapminder = px.data.gapminder()
pop = gapminder.groupby(['year','continent'], as_index=False)['pop'].sum()

# line chart
fig = px.line(
    stocks, x='date', y='GOOG',
    title='Google Stock Price (Normalised)',
    markers=True, template='plotly_white'
)
fig.update_traces(line=dict(width=2.5, color='#00B4D8'))
fig.show()

# area chart
fig = px.area(
    pop, x='year', y='pop', color='continent',
    # groupnorm='fraction',   # bands stack to 100% to show each continent's share
    title='World Population by Continent',
    template='plotly_white'
)
fig.show()