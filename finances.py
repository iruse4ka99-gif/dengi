import streamlit as st

# Настройка стиля
st.set_page_config(page_title="Выход в Ноль", layout="wide")

# Глобальный стиль для цветных карточек
st.markdown("""
    <style>
    .stMetric { background: none !important; border: none !important; }
    .envelope-card { padding: 20px; border-radius: 15px; margin-bottom: 10px; color: white; text-align: center; border: 1px solid #333; }
    .green-card { background-color: #1e3a2f; border-bottom: 5px solid #4caf50; }
    .orange-card { background-color: #3d2b1f; border-bottom: 5px solid #ff9800; }
    .red-card { background-color: #3d1f1f; border-bottom: 5px solid #f44336; }
    .fixed-card { background-color: #1a1c24; border-bottom: 5px solid #2196f3; }
    </style>
    """, unsafe_allow_html=True)

# Инициализация данных
if 'envelopes' not in st.session_state:
    st.session_state.envelopes = {
        "Продукты": {"balance": 250, "limit": 2000},
        "Доп. уроки": {"balance": 1850, "limit": 2500},
        "Машина": {"balance": 700, "limit": 1500},
        "Памперсы": {"balance": 450, "limit": 600},
        "Разное": {"balance": 380, "limit": 1000}
    }
if 'fixed_env' not in st.session_state:
    st.session_state.fixed_env = {"Электричество": 600, "Вода": 200, "Арнона": 800}
if 'history' not in st.session_state:
    st.session_state.history = []

# Шапка
st.title("⚖️ Семейный Бюджет: Выход в Ноль")
total_left = sum(e['balance'] for e in st.session_state.envelopes.values())
st.subheader(f"Доступно в конвертах: {total_left} ₪")

# ОТОБРАЖЕНИЕ КОНВЕРТОВ
cols = st.columns(5)
for i, (name, data) in enumerate(st.session_state.envelopes.items()):
    with cols[i]:
        pct = data['balance'] / data['limit']
        card_class = "green-card"
        if pct < 0.2: card_class = "red-card"
        elif pct < 0.5: card_class = "orange-card"
        
        st.markdown(f"""<div class="envelope-card {card_class}">
            <div style="font-size:14px; opacity:0.8;">{name}</div>
            <div style="font-size:24px; font-weight:bold;">{data['balance']} ₪</div>
            <div style="font-size:12px;">Лимит: {data['limit']}</div>
        </div>""", unsafe_allow_html=True)

# ПОСТОЯННЫЕ КОНВЕРТЫ
st.write("### 📌 Постоянные расходы")
f_cols = st.columns(3)
for i, (name, val) in enumerate(st.session_state.fixed_env.items()):
    with f_cols[i]:
        st.markdown(f"""<div class="envelope-card fixed-card">
            <div>{name}</div><div style="font-size:20px;">{val} ₪</div>
        </div>""", unsafe_allow_html=True)

# ИИ ВВОД И ИСТОРИЯ
st.write("---")
col_input, col_hist = st.columns([1, 1])

with col_input:
    st.write("### 💬 ИИ Помощник")
    user_text = st.text_input("Напиши (например: еда 50)", key="input")
    if st.button("Записать расход"):
        try:
            parts = user_text.split()
            cat = parts[0].lower()
            amt = float(parts[1])
            for real_name in st.session_state.envelopes:
                if cat in real_name.lower():
                    st.session_state.envelopes[real_name]['balance'] -= amt
                    st.session_state.history.insert(0, f"Списано {amt} ₪ с '{real_name}'")
                    st.rerun()
        except:
            st.warning("Напиши название и сумму через пробел")

with col_hist:
    st.write("### 📜 История")
    if not st.session_state.history:
        st.write("Пока нет записей")
    for item in st.session_state.history[:10]:
        st.write(item)
