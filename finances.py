import streamlit as st

# Настройка стиля (темная тема и шрифты)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e1e1e; padding: 15px; border-radius: 10px; border-bottom: 4px solid #2196f3; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ Семейный Бюджет: Выход в Ноль")

# Данные конвертов
if 'envelopes' not in st.session_state:
    st.session_state.envelopes = [
        {"name": "Продукты", "balance": 250, "limit": 2000},
        {"name": "Доп. уроки детей", "balance": 1850, "limit": 2500},
        {"name": "Машина (бензин)", "balance": 700, "limit": 1500},
        {"name": "Памперсы/Уход", "balance": 450, "limit": 600},
        {"name": "Разное/Запас", "balance": 380, "limit": 1000}
    ]

# Панель состояния
total_balance = sum(e['balance'] for e in st.session_state.envelopes)
st.sidebar.metric("Доступно на месяц", f"{total_balance} ₪")
st.sidebar.write("---")
st.sidebar.write("Доход: 18000 ₪")
st.sidebar.write("Фикс. платежи: 10990 ₪")

# Отображение конвертов в ряд
cols = st.columns(len(st.session_state.envelopes))
for i, env in enumerate(st.session_state.envelopes):
    with cols[i]:
        # Логика цвета (Светофор)
        percent = env['balance'] / env['limit']
        if percent < 0.15: color = "🔴"
        elif percent < 0.5: color = "🟡"
        else: color = "🔵"
        
        st.metric(f"{color} {env['name']}", f"{env['balance']} ₪")
        st.progress(min(max(percent, 0.0), 1.0))

# ИИ ВВОД
st.write("---")
user_input = st.text_input("ИИ Помощник: напиши расход (например: еда 100)")

if user_input:
    try:
        parts = user_input.split()
        name_input = parts[0].lower()
        amount = float(parts[1])
        
        for e in st.session_state.envelopes:
            if name_input in e['name'].lower():
                e['balance'] -= amount
                st.success(f"Списано {amount} ₪ из '{e['name']}'")
                st.rerun()
    except:
        st.error("Напиши в формате: название сумма (например: машина 50)")
