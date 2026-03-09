import streamlit as st

# Настройка
st.set_page_config(page_title="Выход в Ноль", layout="wide")

# Стиль карточек
st.markdown("""
    <style>
    .envelope-card { padding: 15px; border-radius: 12px; margin-bottom: 5px; color: white; text-align: center; min-height: 120px; }
    .green-card { background-color: #1e3a2f; border-bottom: 5px solid #4caf50; }
    .orange-card { background-color: #3d2b1f; border-bottom: 5px solid #ff9800; }
    .red-card { background-color: #5e1919; border-bottom: 6px solid #f44336; }
    .fixed-card { background-color: #1a1c24; border-bottom: 4px solid #2196f3; }
    .last-spend { font-size: 11px; opacity: 0.8; margin-top: 5px; color: #ffbcbc; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #262730; color: white; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# Инициализация данных
if 'envelopes' not in st.session_state:
    st.session_state.envelopes = {
        "Продукты": {"balance": 250, "limit": 2000, "history": []},
        "Доп. уроки": {"balance": 1850, "limit": 2500, "history": []},
        "Машина": {"balance": 700, "limit": 1500, "history": []},
        "Памперсы": {"balance": 450, "limit": 600, "history": []},
        "Разное": {"balance": 380, "limit": 1000, "history": []}
    }
if 'fixed' not in st.session_state:
    st.session_state.fixed = {"Электричество": 600, "Вода": 200, "Арнона": 800}

# --- ФИКСИРОВАННЫЕ РАСХОДЫ (СВЕРХУ) ---
st.write("### 📌 Постоянные расходы")
f_cols = st.columns(3)
for i, (name, val) in enumerate(st.session_state.fixed.items()):
    with f_cols[i]:
        st.markdown(f'<div class="envelope-card fixed-card"><div>{name}</div><div style="font-size:22px;">{val} ₪</div></div>', unsafe_allow_html=True)

st.write("---")

# --- КОНВЕРТЫ (РАБОЧИЕ ОКОШКИ) ---
st.write("### 💰 Наши Конверты")
cols = st.columns(5)

for i, (name, data) in enumerate(st.session_state.envelopes.items()):
    with cols[i]:
        pct = data['balance'] / data['limit']
        card_class = "green-card"
        if pct < 0.2: card_class = "red-card"
        elif pct < 0.5: card_class = "orange-card"
        
        # Визуал конверта
        st.markdown(f"""<div class="envelope-card {card_class}">
            <div style="font-size:14px; opacity:0.8;">{name}</div>
            <div style="font-size:26px; font-weight:bold;">{data['balance']} ₪</div>
            <div style="font-size:11px;">Лимит: {data['limit']}</div>
        </div>""", unsafe_allow_html=True)
        
        # Кнопка открытия истории конкретного конверта
        if st.button(f"История {name}", key=f"btn_{name}"):
            st.info(f"**Детали категории {name}:**")
            if not data['history']:
                st.write("Трат пока нет")
            for record in data['history']:
                st.write(record)

# --- ИИ ВВОД (С АВТО-ОЧИСТКОЙ) ---
st.write("---")
st.write("### 💬 ИИ Помощник")

# Используем форму для авто-очистки поля после нажатия Enter или кнопки
with st.form("ai_form", clear_on_submit=True):
    user_text = st.text_input("Напиши расход (например: еда 50)")
    submitted = st.form_submit_button("Записать расход")
    
    if submitted and user_text:
        try:
            parts = user_text.split()
            cat_input = parts[0].lower()
            amt = float(parts[1])
            
            found = False
            for real_name in st.session_state.envelopes:
                if cat_input in real_name.lower():
                    st.session_state.envelopes[real_name]['balance'] -= amt
                    # Добавляем запись в личную историю конверта
                    import datetime
                    time_now = datetime.datetime.now().strftime("%H:%M")
                    st.session_state.envelopes[real_name]['history'].insert(0, f"🕒 {time_now} | -{amt} ₪")
                    st.success(f"Записано: {amt} ₪ в {real_name}")
                    found = True
                    st.rerun()
            if not found:
                st.error("Конверт не найден. Попробуй другое слово.")
        except:
            st.warning("Напиши формат правильно: название сумма (например: машина 100)")

total_sum = sum(e['balance'] for e in st.session_state.envelopes.values())
st.sidebar.metric("Остаток в конвертах", f"{total_sum} ₪")
