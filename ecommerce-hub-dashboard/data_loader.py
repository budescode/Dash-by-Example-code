"""Load and join the Olist e-commerce tables into df."""
import pandas as pd
 
# Read the four raw CSVs from the data/ folder.
orders    = pd.read_csv('data/olist_orders_dataset.csv',
                        parse_dates=['order_purchase_timestamp'])
items     = pd.read_csv('data/olist_order_items_dataset.csv')
customers = pd.read_csv('data/olist_customers_dataset.csv')
payments  = pd.read_csv('data/olist_order_payments_dataset.csv')
 
# Join item totals, customer state and payment value.
df = orders.merge(
    items.groupby('order_id')['price'].sum().reset_index(),
    on='order_id', how='left')
df = df.merge(
    customers[['customer_id', 'customer_state']],
    on='customer_id', how='left')
df = df.merge(
    payments.groupby('order_id')['payment_value'].sum()
            .reset_index(),
    on='order_id', how='left')
 
# Time columns used by the monthly trend chart.
df['month'] = df['order_purchase_timestamp'] \
    .dt.to_period('M').astype(str)
df['year'] = df['order_purchase_timestamp'].dt.year