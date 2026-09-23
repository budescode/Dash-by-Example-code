import plotly.express as px
stocks = px.data.stocks()   # built-in dataset: ships with plotly


# line chart
gapminder = px.data.gapminder()
fig = px.line(
    stocks, x='date', y='GOOG',
    title='Google Stock Price (Normalised)',
    markers=True, template='plotly_white'
)
fig.update_traces(line=dict(width=2.5, color='#00B4D8'))
fig.show()

# area chart
pop = gapminder.groupby(['year','continent'], as_index=False)['pop'].sum()
fig = px.area(
    pop, x='year', y='pop', color='continent',
    # groupnorm='fraction',   # bands stack to 100% to show each continent's share
    title='World Population by Continent',
    template='plotly_white'
)
fig.show()

# barchart
tips = px.data.tips()
daily = tips.groupby('day', as_index=False)['total_bill'].sum() 
fig = px.bar(
    daily, x='day', y='total_bill',
    color='day', text_auto=True,
    category_orders={'day': ['Thur','Fri','Sat','Sun']},  # weekdays in order
    title='Total Restaurant Bills by Day',
    template='plotly_white'
)
fig.update_layout(showlegend=False)
fig.show()

# grouped bar chart

avg = tips.groupby(['day','sex'], as_index=False)['total_bill'].mean()
fig = px.bar(
    avg, x='day', y='total_bill',
    color='sex', barmode='group',   # try barmode='stack'
    category_orders={'day': ['Thur','Fri','Sat','Sun']},
    title='Average Bill by Day and Sex',
    template='plotly_white',
    text_auto=True,
)
fig.show()

# histogram

fig = px.histogram(
    tips, x='total_bill', nbins=20,
    title='Distribution of Total Bills',
    template='plotly_white', text_auto=True
)
fig.update_traces(
    marker_color='brown',
    marker_line_width=1, marker_line_color='white')
fig.show()

# box plot

fig = px.box(
    tips, x='day', y='total_bill', color='smoker',
    # points='all',   # draw every observation as dots beside each box
    category_orders={'day': ['Thur','Fri','Sat','Sun']},
    title='Bill Distribution by Day',
    template='plotly_white'
)
fig.show()

# scattered plot
# trendline needs statsmodels: pip install statsmodels
fig = px.scatter(
    tips, x='total_bill', y='tip',
    color='smoker', size='size',
    hover_name='day',
    trendline='lowess',   # options: 'ols', 'lowess', 'rolling', 'ewm', 'expanding'
    title='Tips vs Total Bill', template='plotly_white'
)
fig.show()