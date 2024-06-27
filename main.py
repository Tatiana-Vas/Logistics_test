import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd


# JSON files path
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
rentals_file_path = os.path.join(base_path, 'rentals.json')
wagons_file_path = os.path.join(base_path, 'wagons.json')

# Loading data from JSON files to DataFrame
rentals = pd.read_json(rentals_file_path, encoding='utf-8')
wagons = pd.read_json(wagons_file_path, encoding='utf-8')

# Data type conversion
rentals['start_date'] = pd.to_datetime(rentals['start_date'])
rentals['end_date'] = pd.to_datetime(rentals['end_date'])

# Checking for missing data and data types
print("Пропуски в данных:")
print(rentals.isnull().sum())
print(wagons.isnull().sum())

print("\nТипы данных в rentals:")
print(rentals.dtypes)
print("\nТипы данных в wagons:")
print(wagons.dtypes)

# Removing rows with missing data
rentals.dropna(inplace=True)
wagons.dropna(inplace=True)

# Adding column MONTH
rentals['month'] = rentals['start_date'].dt.to_period('M')

# Sum of revenue by month
monthly_revenue = rentals.groupby('month')['cost'].sum().reset_index()
print("\nДанные по месячной выручке:")
print(monthly_revenue)

# Converting the MONTH column data type to a string
monthly_revenue['month'] = monthly_revenue['month'].dt.strftime('%B %Y')

# Plotting a graph for revenue by month
plt.figure(figsize=(10, 6))
sns.lineplot(data=monthly_revenue, x='month', y='cost', marker='o')
plt.title('Изменение общей выручки по месяцам')
plt.xlabel('Месяц', labelpad=15)
plt.ylabel('Общая выручка')
plt.grid(True)
plt.show()

# Data merging
merged_data = pd.merge(rentals, wagons, on='wagon_id')

# Revenue by wagon type
revenue_by_wagon_type = merged_data.groupby('wagon_type')['cost'].sum().reset_index()
# Sorting revenue by wagon type by cost
revenue_by_wagon_type = revenue_by_wagon_type.sort_values(by='cost', ascending=False).reset_index(drop=True)

# Number of rentals by wagon type
rental_count_by_wagon_type = merged_data.groupby('wagon_type')['rental_id'].count().reset_index()
rental_count_by_wagon_type.rename(columns={'rental_id': 'rental_count'}, inplace=True)
# Sorting rental count by wagon type by rental_count
rental_count_by_wagon_type = rental_count_by_wagon_type.sort_values(by='rental_count', ascending=False).\
    reset_index(drop=True)

# Calculate rental duration in days
merged_data['rental_duration'] = (merged_data['end_date'] - merged_data['start_date']).dt.days
# Calculate cost per day
merged_data['cost_per_day'] = merged_data['cost'] / merged_data['rental_duration']
# Average cost per day by wagon type
avg_cost_per_day_by_wagon_type = merged_data.groupby('wagon_type')['cost_per_day'].mean().reset_index()
# Sorting average cost per day by wagon type by cost_per_day
avg_cost_per_day_by_wagon_type = avg_cost_per_day_by_wagon_type.sort_values(by='cost_per_day', ascending=False).\
    reset_index(drop=True)

# Print data
print("\nДанные по выручке по типам вагонов:")
print(revenue_by_wagon_type)
print("\nДанные по количеству аренд по типам вагонов:")
print(rental_count_by_wagon_type)
print("\nСредняя стоимость аренды в день по типам вагонов:")
print(avg_cost_per_day_by_wagon_type)

# Plotting a graph for revenue by wagon type
plt.figure(figsize=(10, 6))
sns.barplot(data=revenue_by_wagon_type, x='wagon_type', y='cost')
plt.title('Общая выручка по типам вагонов')
plt.xlabel('Тип вагона', labelpad=15)
plt.ylabel('Общая выручка')
plt.grid(True)
plt.show()

# Plotting a graph for numbers of rentals by wagon type
plt.figure(figsize=(10, 6))
sns.barplot(data=rental_count_by_wagon_type, x='wagon_type', y='rental_count')
plt.title('Количество аренд по типам вагонов')
plt.xlabel('Тип вагона', labelpad=15)
plt.ylabel('Количество аренд')
plt.grid(True)
plt.show()

# Plotting a graph for average cost per day by wagon type
plt.figure(figsize=(10, 6))
sns.barplot(data=avg_cost_per_day_by_wagon_type, x='wagon_type', y='cost_per_day')
plt.title('Средняя стоимость аренды в день по типам вагонов')
plt.xlabel('Тип вагона', labelpad=15)
plt.ylabel('Средняя стоимость аренды в день')
plt.grid(True)
plt.show()
