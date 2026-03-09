import streamlit as st
import datetime
import requests

# ТВОЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbxkvxn-l1zlwpsXV7EsiuOr1xoFQCThBk6KFbeaIUzD7reCD2zoLMo2hdbpKmizEWxf/exec"

st.set_page_config(page_title="Выход в Ноль", layout="centered")

# 1. ЛИМИТЫ (ИТОГО С ФИКСИРОВАННЫМИ = 18 500 ₪)
LIMITS = {
    "Продукты": 4000, "Доп. уроки": 2254, "Лео": 300, 
    "Машина": 500, "Одежда": 200, "Арина": 100, 
    "Натан": 100, "Разное": 256
}

# 2. ПРОФЕССИОНАЛЬНЫЙ ДИЗАЙН (APPLE STYLE)
st.markdown("""
    <style>
    /* Полная очистка интерфейса от мусора Streamlit */
    header, footer, #MainMenu, [data-testid="stSidebar"] {visibility: hidden !important; display: none !important;}
    .block-container {padding-top: 2rem !important;}
    
    html, body, [class*="stApp"] { background-color: #f2f2f7 !important; color: #1c1c1e !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica; }

    /* Центрированный круг остатка */
    .hero-circle {
        width: 200px; height: 200px; border-radius: 100px;
        margin: 0 auto; display: flex; align-items: center; justify-content: center;
        background: white; border: 10px solid #30d158;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    }
    
    /* Карточки категорий */
    .env-card {
        background: white; border-radius: 24px; padding: 20px;
        margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        border: 1px solid #e5e5ea;
    }
    .env-title { font-size: 11px; color: #8e8e93; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .env-value { font-size: 28px; font-weight: 400; color: #1c1c1e; margin: 4px 0; }
    
    /* Светофор (Полоска прогресса) */
    .progress-bg { height: 4px; background: #f2f2f7; border-radius: 2px; width: 100%; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 2px; transition: width 0.5s ease; }

    /* Кнопка внесения */
    .stButton>button {
        background: #30d158 !important; color: white !important; border: none !important;
        border-radius: 18px !important; height: 60px; font-size: 18px; font-weight: 600;
        box-shadow: 0 10px 20px rgba(48,209,88,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ПОЛУЧЕНИЕ ДАННЫХ
@st.cache_data(ttl=2)
def load_data():
    try:
        r = requests.get(SHEET_URL, timeout=5)
        return r.json() if r.status_code == 200 else {}
    except: return {}

spent = load_data()
balances = {n: (v - spent.get(n, 0)) for n, v in LIMITS.items()}

# 4. ЛОГИКА ЦВЕТОВ
def get_color(pct):
    if pct > 0.5: return "#30d158" # Зеленый
    if pct > 0.2: return "#ff9f0a" # Оранжевый
    return "#ff3b30"               # Красный

# 5. ИНТЕРФЕЙС
total_left = sum(balances.values())
total_limit = sum(LIMITS.values())
total_pct = total_left / total_limit if total_limit > 0 else 0
main_color = get_color(total_pct)

st.markdown(f'<p style="text-align:center; color:#8e8e93; font-weight:600; font-size:13px; margin-bottom:0;">{datetime.datetime.now().strftime("%B %Y").upper()}</p>', unsafe_allow_html=True)

# БОЛЬШОЙ КРУГ
st.markdown(f"""
    <div style="padding: 30px 0;">
        <div class="hero-circle" style="border-color: {main_color};">
            <div style="text-align:center;">
                <div style="font-size:48px; font-weight:200;">{int(total_left)}</div>
                <div style="font-size:10px; font-weight:700; color:{main_color};">ОСТАТОК ₪</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# СЕТКА КОНВЕРТОВ (По 2 в ряд)
cols = st.columns(2)
for i, (name, bal) in enumerate(balances.items()):
    limit = LIMITS[name]
    pct = bal / limit if limit > 0 else 0
    color = get_color(pct)
    with cols[i % 2]:
        st.markdown(f"""
            <div class="env-card">
                <div class="env-title">{name}</div>
                <div class="env-value">{int(bal)} <span style="font-size:14px; color:#c7c7cc;">₪</span></div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width:{int(pct*100)}%; background:{color};"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ФИКСИРОВАННЫЕ ПЛАТЕЖИ (Красивая сноска внизу)
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("💳 Обязательные платежи (Детали)"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.write(f"**{n}**: {v} ₪")

st.write("---")

# ФОРМА ВВОДА
with st.form("add_transaction", clear_on_submit=True):
    cat = st.selectbox("КАТЕГОРИЯ", list(LIMITS.keys()))
    amt = st.number_input("СУММА ТРАТЫ", min_value=0, step=1, value=None, placeholder="0 ₪")
    if st.form_submit_button("ВНЕСТИ В ТАБЛИЦУ"):
        if amt:
            try:
                requests.post(SHEET_URL, json={"category": cat, "amount": amt}, timeout=5)
                st.cache_data.clear()
                st.rerun()
            except: st.error("Ошибка сети")
