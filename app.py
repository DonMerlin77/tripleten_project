import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')

df['odometer']= df['odometer'].fillna(df['odometer'].median())
df['odometer'].isnull().sum()

df['is_4wd']= df['is_4wd'].fillna(0)
df['is_4wd'].isnull().sum()

st.header('Vehicle Prices in the US')

st.write('This app shows the prices of vehicles in the US based on condition, if it is 4 wheel drive, and the odometer reading.')

st.write('This is a display of the prices of cars a number of them per price.'
'You can toggle the color on or off to see the distribution of prices.')
price_counts = df['price'].value_counts().reset_index()
price_counts.columns = ['price', 'count']

use_color = st.checkbox("Color by Count", value=True)

if use_color:
    fig = px.scatter(price_counts, x='price', y='count', 
                     title='Price Distribution', 
                     labels={'price': 'Price', 'count': 'Frequency'},
                     color='count', 
                     color_continuous_scale='Viridis')
else:
    fig = px.scatter(price_counts, x='price', y='count', 
                     title='Price Distribution', 
                     labels={'price': 'Price', 'count': 'Frequency'})

fig.update_layout(
    xaxis_title="Price",
    yaxis_title="Car Count",
    showlegend=use_color  
)

st.plotly_chart(fig)

st.write('This will display the condition of cars and the number of them per condition.')

condition_order = ['salvage', 'new', 'fair', 'like new', 'good', 'excellent']
cond_car = px.histogram(df, x='condition', 
                   title='Distribution of Vehicle Condition', 
                   color='condition', 
                   category_orders={'condition': condition_order}
                   )
st.plotly_chart(cond_car)

st.write(f'This will show us the number of cars that have 4 wheel drive and those that don\'t. There will also be a toggle for either showning 4wd, not or both.')

df_price_filter= df[df['price']<200000]

show_4wd = st.checkbox('Show 4WD', value= True)
show_not_4wd = st.checkbox('Show Not 4WD', value= True)

if show_4wd and not show_not_4wd:
    df_filter = df_price_filter[df_price_filter['is_4wd']== 1]
elif show_not_4wd and not show_4wd:
    df_filter = df_price_filter[df_price_filter['is_4wd']== 0]
else:
    df_filter = df_price_filter

four_wd_hist = px.histogram(df_filter, 
                            x='price', 
                            color='is_4wd', 
                            title='Price Distribution by 4WD Status', 
                            labels={'is_4wd': '4WD Status', 'price': 'Price'},  
                            color_discrete_map={0: 'blue', 1: 'red'},
                            nbins=50,  
                            barmode='group')  


legend_labels = {0.0: 'Not 4WD', 1.0: '4WD', '0': 'Not 4WD', '1': '4WD'}

four_wd_hist.for_each_trace(lambda t: t.update(name=legend_labels.get(float(t.name), t.name)))
four_wd_hist.update_layout(
    yaxis_title='Car Count'  
)
st.plotly_chart(four_wd_hist)

st.write('This will compare the number of cars per odometer readings and the price of a car per the odometer.')

import plotly.subplots as sp

df_grouped = df_price_filter.groupby('odometer').agg(
    car_count=('price', 'size'),
    total_price=('price', 'sum')
).reset_index()

odo = sp.make_subplots(rows=1, cols=2, subplot_titles=('Car Count by Odometer', 'Total Price by Odometer'))

odo.add_trace(
    px.histogram(df_grouped, x='odometer', y='car_count', histfunc='sum').data[0],
    row=1, col=1
)

odo.add_trace(
    px.histogram(df_grouped, x='odometer', y='total_price', histfunc='sum').data[0],
    row=1, col=2
)

odo.update_layout(title_text='Car Count and Price Distribution by Odometer', 
                  showlegend=False,
                  xaxis_title= 'Odemeter in Miles',
                  yaxis_title_text= 'Car Count',
                  yaxis2_title_text= 'Total Price of Cars'
)
st.plotly_chart(odo)