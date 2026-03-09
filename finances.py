import streamlit as st
import datetime

# Настройка
st.set_page_config(page_title="Выход в Ноль", layout="wide")

# Улучшенные стили
st.markdown("""
    <style>
    .envelope-card { padding: 15px; border-radius: 12px; margin-bottom: 5px; color: white; text-align: center; min-height: 110px; }
    .green-card { background-color: #1e3a2f; border-bottom: 5px solid #4caf50; }
    .orange-card { background-color: #3d2b1f; border-bottom: 5px solid #ff9800; }
    .red-card { background-color: #5e1919; border-bottom: 6px solid #f44336; }
    .fixed-card { background-color: #1a1c24; border-bottom: 4px solid #2196f3; }
    
    /* Стиль истории как в чате */
    .history-item { 
        background: #262730; border-radius: 10px; padding: 10px; 
        margin-bottom: 8px; border-left: 5px solid #444; color: #ddd;
    }
    .hist-time { font-size: 10px; color: #888; display: block; }
    .hist-amount { font-weight: bold; color: #f44336; }
    </style>
    """, unsafe_allow_html=True)

# Инициализация
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

# 1. ФИКСИРОВАННЫЕ (ВВЕРХУ)
st.write("### 📌 Постоянные расходы")
f_cols = st.columns(3)
for i, (name, val) in enumerate(st.session_state.fixed.items()):
    with f_cols[i]:
        st.markdown(f'<div class="envelope-card fixed-card"><div>{name}</div><div style="font-size:20px;">{val} ₪</div></div>', unsafe_allow_html=True)

st.write("---")

# 2. КОНВЕРТЫ
st.write("### 💰 Наши Конверты")
cols = st.columns(5)
for i, (name, data) in enumerate(st.session_state.envelopes.items()):
    with cols[i]:
        pct = data['balance'] / data['limit']
        card_class = "green-card"
        if pct < 0.2: card_class = "red-card"
        elif pct < 0.5: card_class = "orange-card"
        
        st.markdown(f"""<div class="envelope-card {card_class}">
            <div style="font-size:13px; opacity:0.8;">{name}</div>
            <div style="font-size:24px; font-weight:bold;">{data['balance']} ₪</div>
            <div style="font-size:10px;">Лимит: {data['limit']}</div>
        </div>""", unsafe_allow_html=True)
        
        if st.button(f"📜 История", key=f"h_{name}"):
            st.session_state.show_history = name

# 3. ИИ ВВОД
st.write("---")
st.write("### 💬 ИИ Помощник")

with st.form("ai_form", clear_on_submit=True):
    user_text = st.text_input("Напиши расход (например: косметика 50)")
    submitted = st.form_submit_button("Записать расход")
    
    if submitted and user_text:
        try:
            parts = user_text.split()
            cat_input = parts[0].lower()
            amt = float(parts[1])
            time_now = datetime.datetime.now().strftime("%H:%M")
            
            # Логика поиска: если не нашел, идем в "Разное"
            target_name = "Разное"
            for real_name in st.session_state.envelopes:
                if cat_input in real_name.lower():
                    target_name = real_name
                    break
            
            st.session_state.envelopes[target_name]['balance'] -= amt
            log_entry = f"**{target_name}**: -{amt} ₪ ({cat_input})"
            st.session_state.envelopes[target_name]['history'].insert(0, {"time": time_now, "msg": log_entry})
            
            if target_name == "Разное" and cat_input not in "разное":
                st.info(f"Конверт '{cat_input}' не найден. Записал в 'Разное'")
            else:
                st.success(f"Записано {amt} ₪ в {target_name}")
            st.rerun()
        except:
            st.error("Напиши правильно: название сумма")

# ВЫВОД ИСТОРИИ (ПОД КОНВЕРТОМ ИЛИ ОБЩЕЙ)
if 'show_history' in st.session_state:
    st.write(f"### 📜 История: {st.session_state.show_history}")
    h_data = st.session_state.envelopes[st.session_state.show_history]['history']
    if not h_data:
        st.write("Трат пока нет")
    for h in h_data[:10]:
        st.markdown(f"""<div class="history-item">
            <span class="hist-time">{h['time']}</span>
            {h['msg']}
        </div>""", unsafe_allow_html=True)

