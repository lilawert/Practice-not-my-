import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Функция для загрузки данных из файла Excel
def load_data(path):
    df = pd.read_excel(path, sheet_name='Данные')
    df['Дата'] = pd.to_datetime(df['Дата'])
    return df

# Загрузка данных
path = "данные.xlsx"
data = load_data(path)

# Фильтры
st.sidebar.header("Фильтрация данных")

# Фильтр по месяцу
month_options = ["Все"] + list(data['Дата'].dt.strftime('%b').unique())
month = st.sidebar.selectbox("Выберите месяц", options=month_options, index=0)

# Фильтр по дате
date_range = st.sidebar.date_input("Выберите диапазон дат", value=(data['Дата'].min(), data['Дата'].max()))

# Фильтр по товару
product_options = ["Все"] + list(data['Товар'].unique())
product = st.sidebar.selectbox("Выберите товар", options=product_options, index=0)

# Фильтр по контрагенту
contractor_options = ["Все"] + list(data['Контрагент'].unique())
contractor = st.sidebar.selectbox("Выберите контрагента", options=contractor_options, index=0)

# Фильтр по менеджеру
manager_options = ["Все"] + list(data['Менеджер'].unique())
manager = st.sidebar.selectbox("Выберите менеджера", options=manager_options, index=0)

# Применение фильтров
filtered_data = data.copy()
if month != "Все":
    filtered_data = filtered_data[filtered_data['Дата'].dt.strftime('%b') == month]
if date_range[0] is not None:
    filtered_data = filtered_data[filtered_data['Дата'] >= pd.to_datetime(date_range[0])]
if date_range[1] is not None:
    filtered_data = filtered_data[filtered_data['Дата'] <= pd.to_datetime(date_range[1])]
if product != "Все":
    filtered_data = filtered_data[filtered_data['Товар'] == product]
if contractor != "Все":
    filtered_data = filtered_data[filtered_data['Контрагент'] == contractor]
if manager != "Все":
    filtered_data = filtered_data[filtered_data['Менеджер'] == manager]

# Основные KPI
st.header("Основные KPI")
total_profit = filtered_data['Прибыль'].sum()
total_sales = filtered_data['Сумма'].sum()
best_manager = filtered_data.groupby('Менеджер')['Количество'].sum().idxmax()
best_manager_sales = filtered_data.groupby('Менеджер')['Количество'].sum().max()

col1, col2, col3 = st.columns(3)
col1.metric(label="Общая прибыль, млн руб", value=round(total_profit / 1e6, 2))
col2.metric(label="Лучший менеджер по количеству продаж", value=best_manager)
col3.metric(label="Общая сумма продаж, млн руб", value=round(total_sales / 1e6, 2))

# Прибыль по месяцам
st.header("Прибыль по месяцам, тыс руб")
monthly_profit = filtered_data.resample('M', on='Дата')['Прибыль'].sum() / 1e3
monthly_profit.index = monthly_profit.index.strftime('%b')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=monthly_profit, ax=ax, marker='o', color='skyblue')
ax.set_title("Прибыль по месяцам, тыс руб", fontsize=16)
ax.set_xlabel("Месяц", fontsize=14)
ax.set_ylabel("Прибыль, тыс руб", fontsize=14)
st.pyplot(fig)

# Продажи по товарам
st.header("Продажи по товарам, тыс руб")
product_sales = filtered_data.groupby('Товар')['Сумма'].sum() / 1e3
fig, ax = plt.subplots(figsize=(10, 6))
product_sales.plot.pie(ax=ax, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
ax.set_title("Продажи по товарам, тыс руб", fontsize=16)
ax.set_ylabel("")
st.pyplot(fig)

# Продажи по городам
st.header("Продажи по городам, тыс руб")
city_sales = filtered_data.groupby('Город')['Сумма'].sum() / 1e3
fig, ax = plt.subplots(figsize=(10, 6))
city_sales.plot.bar(ax=ax, color='skyblue')
ax.set_title("Продажи по городам, тыс руб", fontsize=16)
ax.set_xlabel("Город", fontsize=14)
ax.set_ylabel("Сумма продаж, тыс руб", fontsize=14)
st.pyplot(fig)

# Менеджеры, количество продаж
st.header("Менеджеры, количество продаж")
manager_sales = filtered_data.groupby('Менеджер')['Количество'].sum()
fig, ax = plt.subplots(figsize=(10, 6))
manager_sales.plot.barh(ax=ax, color='skyblue')
ax.set_title("Менеджеры, количество продаж", fontsize=16)
ax.set_xlabel("Количество продаж", fontsize=14)
ax.set_ylabel("Менеджер", fontsize=14)
st.pyplot(fig)
