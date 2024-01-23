# -*- coding: utf-8 -*-
"""App

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fFVYjURSmZ4-6CZwrk9GQBk5ZlOPvOL9
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas as pd

file_path_1 = "https://raw.githubusercontent/NickyLay/Dicoding_Analisis_Data/main/order_payments_dataset.csv"
file_path_2 = "https://raw.githubusercontent/NickyLay/Dicoding_Analisis_Data/main/orders_dataset.csv"
df_1 = pd.read_csv(file_path_1)
df_2 = pd.read_csv(file_path_2)

# Drop rows with missing values
df_1.dropna(inplace=True)
df_2.dropna(inplace=True)

# Filter data for credit card payments
df_1_credit_card = df_1[df_1['payment_type'] == 'credit_card']
df_1_credit_card_final = df_1_credit_card.drop(columns=['payment_sequential'])

# Filter data for delivered
df_2_delivered = df_2[df_2['order_status'] == 'delivered']
df_2_delivered_final = df_2_delivered.drop(columns=['order_id','customer_id'])

#question 1
# Group by 'payment_installments' and calculate mean and std
grouped_data = df_1_credit_card.groupby('payment_installments')['payment_value'].agg(['mean', 'std']).reset_index()

#question 2
# Convert timestamp columns to datetime format
# Convert timestamp columns to datetime format
timestamp_columns = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']

for col in timestamp_columns:
    df_2_delivered_final[col] = pd.to_datetime(df_2_delivered_final[col], format='%Y-%m-%d %H:%M:%S')

# Calculate the actual delivery time
df_2_delivered_final['actual_delivery_time'] = (df_2_delivered_final['order_delivered_customer_date'] - df_2_delivered_final['order_purchase_timestamp']).dt.days

# Calculate the estimated delivery time
df_2_delivered_final['estimated_delivery_time'] = (df_2_delivered_final['order_estimated_delivery_date'] - df_2_delivered_final['order_purchase_timestamp']).dt.days

# Calculate the difference between actual and estimated delivery time
df_2_delivered_final['delivery_time_difference'] = (df_2_delivered_final['order_delivered_customer_date'] - df_2_delivered_final['order_estimated_delivery_date']).dt.days

# Group by estimated delivery time and calculate mean
average_actual_delivery_time = df_2_delivered_final.groupby('estimated_delivery_time')['actual_delivery_time'].mean()
average_actual_delivery_time_df = average_actual_delivery_time.reset_index()

# Group by estimated delivery time and calculate mean difference
average_difference = df_2_delivered_final.groupby('estimated_delivery_time')['delivery_time_difference'].mean()
average_difference_df = average_difference.reset_index()

# Streamlit app code
st.title('Delivery Time Analysis')


# Visualization 1: Average and Standard Deviation for Each Number of Installments
st.subheader('Average and Standard Deviation for Each Number of Installments')

# Plotting using Matplotlib
fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(grouped_data['payment_installments'], grouped_data['mean'], yerr=grouped_data['std'], capsize=5, color='skyblue')
ax.set_title('Average and Standard Deviation for Each Number of Installments')
ax.set_xlabel('Number of Installments')
ax.set_ylabel('Payment Value')

# Display the plot in Streamlit
st.pyplot(fig)

# Visualization 2: Average Actual Delivery Time for Each Estimated Delivery Time
st.subheader('Average Actual Delivery Time for Each Estimated Delivery Time')
st.dataframe(average_actual_delivery_time_df.head(10))  # Display the top 10 rows

# Bar chart for Average Difference
st.subheader('Bar Chart: Average Difference between Actual and Estimated Delivery Time')
st.bar_chart(average_actual_delivery_time_df.set_index('estimated_delivery_time'))

# Visualization 3: Average Difference between Actual and Estimated Delivery Time
st.subheader('Average Difference between Actual and Estimated Delivery Time for Each Estimated Delivery Time')
st.dataframe(average_difference_df.head(10))  # Display the top 10 rows

# Bar chart for Average Difference
st.subheader('Bar Chart: Average Difference between Actual and Estimated Delivery Time')
st.bar_chart(average_difference_df.set_index('estimated_delivery_time'))

st.subheader('Kesimpulan: ')
formatted_text = """
- Walau terdapat tren kenaikan jumlah uang yang dibayar dengan jumlah cicilan yang dilakukan, kenaikan bersifat fluktuatif sehingga disimpulkan tidak ada korelasi antaran 2 variabel tersebut

- Semakin lama waktu pengiriman produk, jarak antara estimasi waktu yang dibutuhkan dengan waktu asli yang dibutuhkan semakin meningkat, maka perlu dilakukan pengalibrasian estimasi waktu agar tidak terlalu jauh dari waktu asli yang diperlukan.

"""
st.markdown(formatted_text)