import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# pie chart 
fig = px.pie(
    tips, values='total_bill', names='day',
    hole=0.4, title='Revenue Share by Day'
)
fig.update_traces(textposition='inside', textinfo='percent+label')
total = tips['total_bill'].sum()
fig.add_annotation(text=f'${total:,.0f}', x=0.5, y=0.5,
                   showarrow=False, font_size=28)
fig.show()

# Choropleth Maps
gap = px.data.gapminder().query("year == 2007")
fig = px.choropleth(
    gap,
    locations='country',            # region column in the dataframe
    locationmode='country names',   # how to read it; 4 modes below
    #   'ISO-3' (default)  'country names'  'USA-states'  'geojson-id'
    color='lifeExp',
    hover_name='country',
    color_continuous_scale='Viridis',
    title='Life Expectancy by Country (2007)'
)
fig.show()

# scatter_map
carshare = px.data.carshare()
fig = px.scatter_map(
    carshare,
    lat='centroid_lat', lon='centroid_lon',
    color='peak_hour', size='car_hours',
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=15, zoom=10,
    map_style='open-street-map',
    title='Montreal Car-Share Availability'
)
fig.show()

# animated charts
gapminder = px.data.gapminder()   # full dataset, all years 
fig = px.scatter(
    gapminder, x='gdpPercap', y='lifeExp',
    size='pop', color='continent', hover_name='country',
    animation_frame='year', log_x=True, size_max=55,
    range_y=[25, 90], title='Life Expectancy vs GDP per Capita'
)
fig.show()

# funnel charts
fig = px.funnel(
    x=[100000, 42000, 18000, 9500, 7200],
    y=['Visitors','Views','Cart','Checkout','Purchase'],
    title='Customer Acquisition Funnel'
)
# fig.update_traces(textinfo='value+percent initial')   # % of the first stage on each bar
fig.show()

# heatmaps
tips = px.data.tips()
corr = tips[['total_bill','tip','size']].corr()
fig = px.imshow(
    corr, text_auto='.2f',
    color_continuous_scale='RdBu_r',
    title='Correlation Heatmap'
)
fig.show() 

# facets
fig = px.scatter(
    tips, x='total_bill', y='tip',
    color='smoker', facet_col='day',
    # facet_col_wrap=2,   # wrap the 4 panels into a 2x2 grid
    category_orders={'day': ['Thur','Fri','Sat','Sun']},
    title='Tips by Day - Small Multiples',
    template='plotly_white'
)
fig.show()

# Customising Any Chart
daily = tips.groupby('day', as_index=False)['total_bill'].sum()
fig = px.bar(
    daily, x='day', y='total_bill',
    labels={'total_bill': 'Revenue ($)', 'day': 'Day of Week'},
    category_orders={'day': ['Thur','Fri','Sat','Sun']},
    color='day',
    color_discrete_sequence=px.colors.qualitative.Set2,
    hover_data={'total_bill': ':$,.2f'},
    template='plotly_white'
)
fig.update_layout(
    title_font_size=18, plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Arial', size=12),
    legend_title_text='',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, x=0),
    margin=dict(l=40, r=20, t=60, b=40),
    hovermode='x unified'
)
fig.update_traces(marker_line_width=0, opacity=0.85)
fig.update_xaxes(showgrid=False, tickangle=-45)  # rotate crowded labels
fig.update_yaxes(gridcolor='#EEEEEE', tickprefix='$', tickformat=',.0f')
fig.add_hline(y=1000, line_dash='dash', annotation_text='Daily Target')
fig.show()

# hover
daily = tips.groupby('day', as_index=False).agg(
    total_bill=('total_bill', 'sum'), orders=('total_bill', 'size'))
fig = px.bar(daily, x='day', y='total_bill',
             custom_data=['orders'])
fig.update_traces(hovertemplate=(
    '<b>%{x}</b><br>Revenue: $%{y:,.2f}'
    '<br>Orders: %{customdata[0]}<extra></extra>'))
fig.show()

