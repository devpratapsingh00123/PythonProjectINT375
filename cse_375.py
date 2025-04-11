import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# 1. Load and Display Basic Information about the Dataset
df = pd.read_csv("C:\\Users\\user\\OneDrive\\Desktop\\ca3 int 375\\MTA_Daily_Ridership_Data__2020_-_2025.csv") # Display basic information
print(df.info())
print(df.head())

# 2. Handling Missing Data
'''
#2.1 Check for missing values
print(df.isnull().sum())
#2.2 Fill missing values with the column mean (for numerical data)
df.fillna(df.mean(numeric_only=True), inplace=True)
#2.3 Drop rows with missing values
df.dropna(inplace=True)
'''

#3. Data Manipulation using NumPy and Pandas
'''
# 3.1: Clean column names: replace spaces with underscores
df.columns = df.columns.str.strip().str.replace(' ', '_')
# 3.2: Print cleaned column names 
print("Cleaned Column Names:")
print(df.columns.tolist())
# 3.3: Convert Date with mixed formats
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Safely parse any format
# 3.4: Create 'Total_Ridership' by summing all 'Total_Estimated_Ridership' columns
ridership_columns = [col for col in df.columns if 'Total_Estimated_Ridership' in col]
df['Total_Ridership'] = df[ridership_columns].sum(axis=1)
# 3.5: Sort by date
df = df.sort_values(by='Date')
# 3.6: Add Weekday column
df['Weekday'] = df['Date'].dt.day_name()
# 3.7: Calculate average ridership
average_ridership = df['Total_Ridership'].mean()
print(f"\nAverage Ridership: {average_ridership:.2f}")
# 3.8: Ridership Difference from previous day
df['Ridership_Diff'] = df['Total_Ridership'].diff()
# 3.9: High Ridership flag: > 1.5x average
df['High_Ridership'] = np.where(df['Total_Ridership'] > 1.5 * average_ridership, True, False)
# 3.10: Display sample data
print("\nSample of manipulated data:")
print(df[['Date', 'Total_Ridership', 'Weekday', 'Ridership_Diff', 'High_Ridership']].head())
'''

# 4. Creating a Line Plot with Matplotlib
'''
# 4.1: Clean column names: remove leading/trailing spaces and replace spaces with underscores
df.columns = df.columns.str.strip().str.replace(' ', '_')
print("Cleaned Column Names:")
print(df.columns.tolist())
# 4.2: Handle missing data
print("\nMissing values before cleaning:")
print(df.isnull().sum())
ridership_cols = ['Subways:_Total_Estimated_Ridership', 'Buses:_Total_Estimated_Ridership']
#4.3: Drop rows where both ridership columns are missing
df = df.dropna(subset=ridership_cols, how='all')
#4.4: Fill any remaining missing values in these columns with 0
df[ridership_cols] = df[ridership_cols].fillna(0)
print("\nMissing values after cleaning:")
print(df.isnull().sum())
#4.5: Simulate time axis using row numbers (if you don't have a proper date column)
df['Time'] = range(1, len(df) + 1)

df['Subways_Smoothed'] = df['Subways:_Total_Estimated_Ridership'].rolling(window=10).mean()
df['Buses_Smoothed'] = df['Buses:_Total_Estimated_Ridership'].rolling(window=10).mean()

#4.6: Plot ridership trends over simulated time
plt.figure(figsize=(14, 6))
plt.plot(df['Time'], df['Subways_Smoothed'], label='Subways Ridership (Smoothed)', color='blue')
plt.plot(df['Time'], df['Buses_Smoothed'], label='Buses Ridership (Smoothed)', color='green')

# Optional: Add lighter raw data lines for reference
plt.plot(df['Time'], df['Subways:_Total_Estimated_Ridership'], alpha=0.2, color='blue', linestyle='dotted')
plt.plot(df['Time'], df['Buses:_Total_Estimated_Ridership'], alpha=0.2, color='green', linestyle='dotted')

# Labels and styling
plt.xlabel("Time (Simulated)")
plt.ylabel("Ridership")
plt.title("Ridership Trend Over Simulated Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
'''

# 5. Find the Top 5 Days with Highest Ridership
'''
# 5.1. Clean column names: strip spaces and replace spaces with underscores
df.columns = df.columns.str.strip().str.replace(' ', '_')
#5.2: Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
#5.3: Identify ridership columns (columns that include 'Total_Estimated_Ridership')
ridership_columns = [col for col in df.columns if "Total_Estimated_Ridership" in col]
#5.4: Create a new column for total daily ridership
df[ridership_columns] = df[ridership_columns].fillna(0)
df['Total_Ridership'] = df[ridership_columns].sum(axis=1)
#5.5: Drop any rows with an invalid Date (if conversion failed)
df = df.dropna(subset=['Date'])
#5.6: Sort the DataFrame by Date if needed (optional)
df = df.sort_values(by='Date')
# 5.7: Find the Top 5 Days with Highest Ridership
top5 = df.nlargest(5, 'Total_Ridership')
#5.8: Display the result
print("Top 5 Days with Highest Ridership:")
print(top5[['Date', 'Total_Ridership']])
'''

# 6. Scatterplot: Subway vs Bus Ridership
'''
#6.1 Clean column names: replace spaces with underscores and remove special characters
df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace(':', '')
#6.2 Handle missing data
df = df.dropna(subset=['Subways_Total_Estimated_Ridership', 'Buses_Total_Estimated_Ridership'])
#6.3 Create scatter plot: Subways vs Buses Ridership
plt.figure(figsize=(10, 6))
plt.scatter(df['Subways_Total_Estimated_Ridership'], df['Buses_Total_Estimated_Ridership'], alpha=0.7, color='blue', edgecolor='k')
plt.xlabel('Subways: Total Estimated Ridership')
plt.ylabel('Buses: Total Estimated Ridership')
plt.title('Scatterplot: Subways vs Buses Ridership')
plt.grid(True)
plt.tight_layout()
plt.show()
'''

# 7. Bar Plot: Average Ridership by Year
'''
# Clean column names: replace spaces with underscores
df.columns = df.columns.str.strip().str.replace(' ', '_')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop rows where both 'Subways:_Total_Estimated_Ridership' and 'Buses:_Total_Estimated_Ridership' are missing
df = df.dropna(subset=['Subways:_Total_Estimated_Ridership', 'Buses:_Total_Estimated_Ridership'], how='all')

# Fill remaining missing values in 'Subways:_Total_Estimated_Ridership' and 'Buses:_Total_Estimated_Ridership' with 0
df[['Subways:_Total_Estimated_Ridership', 'Buses:_Total_Estimated_Ridership']] = df[['Subways:_Total_Estimated_Ridership', 'Buses:_Total_Estimated_Ridership']].fillna(0)

# Extract month name from 'Date' column
df['Month'] = df['Date'].dt.strftime('%B')

# Create 'Total_Ridership' column by summing 'Subways:_Total_Estimated_Ridership' and 'Buses:_Total_Estimated_Ridership'
df['Total_Ridership'] = df['Subways:_Total_Estimated_Ridership'] + df['Buses:_Total_Estimated_Ridership']

# Group by month and sum total ridership
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

monthly_total = df.groupby('Month')['Total_Ridership'].sum().reindex(month_order).dropna()

# Plot using matplotlib
plt.figure(figsize=(12, 6))
plt.bar(monthly_total.index, monthly_total.values, color='orange')
plt.xlabel("Month")
plt.ylabel("Total Ridership")
plt.title("Monthly Ridership Trends")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
'''