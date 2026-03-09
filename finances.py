import streamlit as st
import pandas as pd
import os

# ДАННЫЕ ИЗ ВАШЕЙ ТАБЛИЦЫ
SALARY = 18000
FIXED_COSTS = 10990
STOCK_MARKET = 500 
TOTAL_FIXED = FIXED_COSTS + STOCK_MARKET

# ВАШИ КОНВЕРТЫ ДЛЯ ВЫХОДА В НОЛЬ
ENVELOPE_PLAN = [
    {"Название": "🛒 Продукты", "План": 3100},
    {"Название": "📚 Доп. уроки детей", "План": 1850},
    {"Название": "🚗 Машина (бензин)", "План": 700},
    {"Название": "👶 Памперсы/Уход", "План": 450},
    {"Название": "🆘 Разное/Запас", "План": 410}
]

st.set_page_config(page_title="Наш Бюджет 0:00", layout="wide")
st.title("⚖️ Семейный Бюджет: Выход в Ноль")

# Файл для хранения ваших трат
if not os.path.exists("envelopes.csv"):
    df = pd.DataFrame(ENVELOPE_PLAN)
    df["Остаток"] = df["План"]
    df.to_csv("envelopes.csv", index=False)

env_df = pd.read_csv("envelopes.csv")

st.sidebar.header("📊 Общая картина")
st.sidebar.write(f"Доход: **{SALARY} ₪**")
st.sidebar.write(f"Фикс. платежи: **{FIXED_COSTS} ₪**")
st.sidebar.write(f"Биржа: **{STOCK_MARKET} ₪**")
st.sidebar.divider()
st.sidebar.success(f"Доступно на месяц: **{SALARY - TOTAL_FIXED} ₪**")

st.subheader("Наши Конверты")
cols = st.columns(len(ENVELOPE_PLAN))
for i, row in env_df.iterrows():
    with cols[i]:
        pct = row["Остаток"] / row["План"] if row["План"] > 0 else 0
        st.metric(label=row["Название"], value=f"{row['Остаток']} ₪")
        st.progress(min(1.0, pct))

st.divider()
with st.form("spend_log", clear_on_submit=True):
    col1, col2 = st.columns(2)
    target = col1.selectbox("Выберите конверт", env_df["Название"])
    amt = col2.number_input("Сумма покупки (₪)", min_value=1)
    if st.form_submit_button("✅ Записать расход"):
        idx = env_df[env_df["Название"] == target].index[0]
        if env_df.at[idx, "Остаток"] >= amt:
            env_df.at[idx, "Остаток"] -= amt
            env_df.to_csv("envelopes.csv", index=False)
            st.success(f"Записано! Остаток в {target}: {env_df.at[idx, 'Остаток']} ₪")
            st.rerun()
        else:
            st.error("В этом конверте закончились деньги!")
