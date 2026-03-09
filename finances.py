import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ПРОФЕССИОНАЛЬНЫЙ ДИЗАЙН (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="stApp"] {
        font-family: 'Inter', sans-serif;
        background-color: #080a0c;
        color: #e0e0e0;
    }

    /* Главный неоновый круг */
    .circle-container {
        display: flex; justify-content: center; padding: 30px 0;
    }
    .main-circle {
        width: 200px; height: 200px; border-radius: 50%;
        background: radial-gradient(closest-side, #080a0c 88%, transparent 89% 100%),
        conic-gradient(#00f2fe var(--p), #1a1f25 0);
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.15);
        border: 1px solid #1a1f25;
    }
    .circle-data { text-align: center; }
    .circle-amount { font-size: 32px; font-weight: 600; color: #fff; }
    .circle-label { font-size: 10px; color: #666; letter-spacing: 2px; }

    /* Карточки конвертов (Премиум вид) */
    .env-card {
        background: rgba(26, 31, 37, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .env-card:hover {
        border: 1px solid rgba(0, 242, 254, 0.3);
        transform: translateY(-5px);
    }
    .env-title { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
    .env-value { font-size: 26px; font-weight: 600; color: #fff; margin-bottom: 5px; }
    .env-progress-bar {
        height: 4px; background: #1a1f25; border-radius: 2px; margin: 10px 0; overflow: hidden;
    }
    .env-progress-fill { height: 100%; background: var(--c); box-shadow: 0 0 10px var(--c); }

    /* Убираем мусор Streamlit */
    div.stButton > button {
        background-color: transparent !important;
        border: 1px solid #1a1f25 !important;
        color: #444 !important;
        border-radius: 10px !important;
        width: 100%; height: 30px; font-size: 12px;
    }
    div.stButton > button:hover { border-color: #00f2fe !important; color: #00f2fe !important; }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ (Категории из твоей таблицы)
if 'db' not in st.session_state:
    st.session_state.db = {
        "envs": {
            "Продукты": {"b": 4000, "l": 4000, "c": "#00f2fe"},
            "Машина": {"b": 1365, "l": 1365, "c": "#f9d423"},
            "Доп. уроки": {"b": 1850, "l": 1850, "c": "#4facfe"},
            "Одежда": {"b": 1000, "l": 1000, "c": "#ff0844"},
            "Личные": {"b": 500, "l": 500, "c": "#667eea"},
            "Памперсы": {"b": 450, "l": 450, "c": "#f093fb"},
            "Животные": {"b": 200, "l": 200, "c": "#5ee7df"},
            "Красота": {"b": 335, "l": 335, "c": "#ebc0fd"},
            "Разное": {"b": 1300, "l": 1300, "c": "#888"}
        },
        "log": []
    }

# ВЕРХНИЙ БЛОК: НЕОНОВЫЙ КРУГ
total_left = sum(v['b'] for v in st.session_state.db['envs'].values())
pct = int((total_left / 18000) * 100)

st.markdown(f"""
    <div class="circle-container">
        <div class="main-circle" style="--p: {pct}%">
            <div class="circle-data">
                <div class="circle-amount">{int(total_left)} ₪</div>
                <div class="circle-label">ОСТАТОК</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# СЕТКА КОНВЕРТОВ
items = list(st.session_state.db['envs'].items())
for i in range(0, len(items), 3):
    cols = st.columns(3)
    for j, (name, d) in enumerate(items[i:i+3]):
        with cols[j]:
            p_fill = (d['b'] / d['l']) * 100
            st.markdown(f"""
                <div class="env-card">
                    <div class="env-title">{name}</div>
                    <div class="env-value">{int(d['b'])} ₪</div>
                    <div class="env-progress-bar">
                        <div class="env-progress-fill" style="--c: {d['c']}; width: {p_fill}%"></div>
                    </div>
                    <div style="font-size: 10px; color: #555;">ЛИМИТ {int(d['l'])} ₪</div>
                </div>
            """, unsafe_allow_html=True)
            # Кнопки управления (минималистичные)
            c1, c2 = st.columns(2)
            with c1: st.button("История", key=f"h_{name}")
            with c2: st.button("Опции", key=f"s_{name}")

# ВВОД
st.write("---")
with st.form("premium_input", clear_on_submit=True):
    vvod = st.text_input("Внеси расход (напр: машина 100)")
    if st.form_submit_button("ПОДТВЕРДИТЬ"):
        # Логика списания остается той же
        parts = vvod.split()
        if len(parts) == 2:
            cat, amt = parts[0].lower(), float(parts[1])
            target = "Разное"
            for n in st.session_state.db['envs']:
                if cat in n.lower(): target = n; break
            st.session_state.db['envs'][target]['b'] -= amt
            st.rerun()
