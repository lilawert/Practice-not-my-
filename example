import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Функция для загрузки данных из файла Excel
def load_data(path):
    df = pd.read_excel(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

# Загрузка данных~
path = "results.xlsx"
data = load_data(path)

# Фильтры
st.sidebar.header("Фильтрация данных")

# Фильтр по supplierArticle
supplier_article_options = ["Все"] + list(data['supplierArticle'].unique())
supplier_article = st.sidebar.selectbox(
    "Выберите supplierArticle",
    options=supplier_article_options,
    index=0
)

# Фильтр по category
category_options = ["Все"] + list(data['category'].unique())
category = st.sidebar.selectbox(
    "Выберите категорию",
    options=category_options,
    index=0
)

# Фильтр по date
date_range = st.sidebar.date_input(
    "Выберите диапазон дат",
    value=(data['date'].min(), data['date'].max())
)

# Применение фильтров
filtered_data = data.copy()
if supplier_article != "Все":
    filtered_data = filtered_data[filtered_data['supplierArticle'] == supplier_article]
if category != "Все":
    filtered_data = filtered_data[filtered_data['category'] == category]
if date_range[0] is not None:
    filtered_data = filtered_data[filtered_data['date'] >= pd.to_datetime(date_range[0])]
if date_range[1] is not None:
    filtered_data = filtered_data[filtered_data['date'] <= pd.to_datetime(date_range[1])]
data = filtered_data

# Отображение таблицы данных
st.dataframe(data)

# Основные KPI
st.header("Основные KPI")
total_records = len(data)
mean_value = data['finishedPrice'].mean()
max_value = data['finishedPrice'].max()

# Создание колонок для KPI карточек
col1, col2, col3 = st.columns([1, 2, 1])
col1.metric(label="Общее количество записей", value=total_records)
col2.metric(label="Среднее значение стоимости заказа", value=mean_value)
col3.metric(label="Самый дорогой заказ", value=max_value)

# Временные зависимости
st.header("Временные зависимости")
filtered_data = data.set_index('date')
orders_per_day = filtered_data.groupby(filtered_data.index).size()

fig, ax = plt.subplots()
sns.lineplot(data=orders_per_day, ax=ax)
ax.set_title("Количество заказов по датам")
ax.set_xlabel("Дата")
ax.set_ylabel("Количество заказов")
st.pyplot(fig)

# Барчарт
st.header("Барчарт")
fig, ax = plt.subplots()
sns.barplot(data=filtered_data, x='category', y='finishedPrice', ax=ax)
ax.set_title("Барчарт по категориям")
ax.set_xlabel("Категория")
ax.set_ylabel("Значение")
st.pyplot(fig)
