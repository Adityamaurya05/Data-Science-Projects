import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA

# Load the dataset
df = pd.read_csv('SuperStore_Sales_Dataset_Program.csv')



# Group by customer_id to create customer-level features
customer_df = df.groupby('customer_id').agg({
    'sales': 'sum',
    'quantity': 'sum',
    'order_id': 'count'
}).rename(columns={
    'sales': 'total_sales',
    'quantity': 'total_quantity',
    'order_id': 'order_count'
}).reset_index()

# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(customer_df[['total_sales', 'total_quantity', 'order_count']])

# Determine the optimal number of clusters using the Elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(scaled_features)
    wcss.append(kmeans.inertia_)

# Plot the Elbow graph
plt.plot(range(1, 11), wcss)
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.title('Elbow Method')
plt.show()

# Choose an appropriate number of clusters (e.g., 3)
kmeans = KMeans(n_clusters=3, random_state=42)
customer_df['cluster'] = kmeans.fit_predict(scaled_features)

# Visualize the clusters
plt.figure(figsize=(10, 6))
plt.scatter(customer_df['total_sales'], customer_df['total_quantity'], c=customer_df['cluster'], cmap='viridis', s=50)
plt.title('Customer Segments')
plt.xlabel('Total Sales')
plt.ylabel('Total Quantity')
plt.colorbar(label='Cluster')
plt.show()

# Aggregate sales data by order_date
daily_sales = df.groupby('order_date')['sales'].sum().reset_index()

# Set order_date as index
daily_sales.set_index('order_date', inplace=True)

# Fit ARIMA model
model = ARIMA(daily_sales['sales'], order=(5, 1, 0))
model_fit = model.fit()

# Forecast the next 15 days
forecast = model_fit.forecast(steps=15)

# Plot historical sales data and forecasted sales
plt.figure(figsize=(10, 6))
plt.plot(daily_sales.index, daily_sales['sales'], label='Historical Sales')
plt.plot(forecast.index, forecast.values, color='red', linestyle='--', label='Forecasted Sales')
plt.title('Sales Forecasting for the Next 15 Days')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.legend()
plt.grid(True)
plt.show()
