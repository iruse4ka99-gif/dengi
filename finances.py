import streamlit as st
import datetime

# 1. СТИЛИ И ИНТЕРФЕЙС
st.markdown("""
    <style>
    .salary-circle {
        width: 150px; height: 150px; border-radius: 50%;
        background: conic-gradient(#4caf50 var(--percent), #333 0);
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; color: white; margin: auto; font-weight: bold;
    }
    .envelope-card { padding: 15px; border-radius: 12px; text-align: center; color: white; margin-bottom: 10px; }
    .green-card { background-color: #1e3a2f; border-bottom: 5px solid #4caf50; }
    .orange-card { background-color: #3d2b1f; border-bottom: 5px solid #ff9800; }
    .red-card { background-color: #5e1919; border-bottom: 6px solid #f44336; }
    .hist-item { background: #262730; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 5px solid #2196f3; }
    </style>
    """, unsafe_allow_html=True)

# 2. ИНИЦИАЛИЗАЦИЯ И УМНЫЕ КАТЕГОРИИ
if 'envelopes' not in st.session_state:
    st.session_state.envelopes = {
        "Продукты": {"balance": 2500, "limit": 3000, "keys": ["еда", "кола", "сок", "хлеб", "молоко", "ужин", "супермаркет"]},
        "Уроки": {"balance": 1850, "limit": 2500, "keys": ["школа", "плавание", "кружок", "учитель", "секция"]},
        "Машина": {"balance": 700, "limit": 1500, "keys": ["бензин", "панго", "парковка", "гараж", "топливо"]},
        "Уход/Дети": {"balance": 450, "limit": 600, "keys": ["паста", "щетка", "памперс", "крем", "мыло", "косметика", "аптека"]},
        "Разное": {"balance": 380, "limit": 1000, "keys": []}
    }
    st.session_state.history = []

# 3. КРУГ ЗАРПЛАТЫ (СВЕРХУ)
total_left = sum(e['balance'] for e in st.session_state.envelopes.values())
income = 18000
pct = int((total_left / income) * 100)

st.write("### 💰 Баланс зарплаты")
st.markdown(f'<div class="salary-circle" style="--percent: {pct}%">{pct}%</div>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Осталось: {total_left} ₪ из {income}</p>", unsafe_allow_html=True)

# 4. КОНВЕРТЫ
cols = st.columns(5)
for i, (name, data) in enumerate(st.session_state.envelopes.items()):
    with cols[i]:
        usage = data['balance'] / data['limit']
        card_color = "green-card" if usage > 0.5 else ("orange-card" if usage > 0.2 else "red-card")
        st.markdown(f'<div class="envelope-card {card_color}"><b>{name}</b><br><span style="font-size:22px;">{data["balance"]} ₪</span></div>', unsafe_allow_html=True)

# 5. ИИ ВВОД
st.write("---")
with st.form("ai_form", clear_on_submit=True):
    user_input = st.text_input("Напиши (например: кола 10 или паста 20)")
    if st.form_submit_button("Записать"):
        try:
            parts = user_input.lower().split()
            word, amount = parts[0], float(parts[1])
            
            # УМНЫЙ ПОИСК
            target = "Разное"
            for name, d in st.session_state.envelopes.items():
                if word in name.lower() or any(k in word for k in d['keys']):
                    target = name
                    break
            
            st.session_state.envelopes[target]['balance'] -= amount
            st.session_state.history.insert(0, f"🕒 {datetime.datetime.now().strftime('%H:%M')} | {word.capitalize()}: -{amount} ₪ ({target})")
            st.rerun()
        except: st.error("Формат: слово сумма")

# 6. ИСТОРИЯ
st.write("### 📜 Последние действия")
for entry in st.session_state.history[:5]:
    st.markdown(f'<div class="hist-item">{entry}</div>', unsafe_allow_html=True)
