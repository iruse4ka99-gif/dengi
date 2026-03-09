import streamlit as st
import datetime
import requests

# ТВОЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbxkvxn-l1zlwpsXV7EsiuOr1xoFQCThBk6KFbeaIUzD7reCD2zoLMo2hdbpKmizEWxf/exec"

st.set_page_config(page_title="Выход в Ноль", layout="centered") # Центрируем всё

# 1. ТВОИ НОВЫЕ ЛИМИТЫ (ИТОГО: 18 500 ₪)
LIMITS = {
    "Продукты": 4000, "Доп. уроки": 2254, "Лео": 300, 
    "Машина": 500, "Одежда": 200, "Арина": 100, 
    "Натан": 100, "Разное": 256  # Подрезали, чтобы выйти в 18 500
}

# 2. СТИЛИ (УДАЛЯЕМ ВЕСЬ МУСОР)
st.markdown("""
    <style>
    /* Прячем меню и шестеренки Streamlit */
    header, footer, #MainMenu {visibility: hidden !important;}
    [data-testid="stSidebar"] {display: none !important;}
    
    html, body, [class*="stApp"] { background-color: #ffffff !important; }
    
    /* Главный круг */
    .main-circle {
        width: 160px; height: 160px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto; border: 6px solid #30d158;
        box-shadow: 0 10px 40px rgba(48,209,88,0.15);
    }
    
    /* Красивые карточки */
    .card {
        background: #f8f9fa; border-radius: 20px; padding: 15px;
        text-align: center; border: 1px solid #eeeeee; margin-bottom: 10px;
    }
    .card-num { font-size: 24px; font-weight: 600; color: #1a1a1a; }
    .card-label { font-size: 10px; color: #8e8e93; text-transform: uppercase; font-weight: 700; }
    
    /* Кнопка */
    .stButton>button {
        background-color: #30d158 !important; color: white !important;
        border-radius: 16px !important; height: 55px; width: 100%;
        font-size: 18px; font-weight: 700; border: none !important;
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

# 4. ИНТЕРФЕЙС
now = datetime.datetime.now()
st.markdown(f'<div style="text-align:center; color:#8e8e93; font-size:12px; margin-top:20px; font-weight:600;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

# ГЛАВНЫЙ КРУГ
total_left = sum(balances.values())
st.markdown(f"""
    <div style="padding: 40px 0;">
        <div class="main-circle">
            <div style="text-align:center;">
                <div style="font-size:42px; font-weight:300; color:#1a1a1a;">{int(total_left)}</div>
                <div style="font-size:10px; font-weight:700; color:#30d158; letter-spacing:1px;">ОСТАТОК ₪</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# КАРТОЧКИ (СЕТКА 2x4)
cols = st.columns(2) # Делаем по 2 в ряд, так удобнее на телефоне
items = list(balances.items())
for i in range(len(items)):
    with cols[i % 2]:
        name, bal = items[i]
        st.markdown(f"""
            <div class="card">
                <div class="card-label">{name}</div>
                <div class="card-num">{int(bal)}</div>
            </div>
        """, unsafe_allow_html=True)

# ФИКСИРОВАННЫЕ РАСХОДЫ (Упрятали в красивый раскрывающийся список вниз)
with st.expander("🔒 Обязательные платежи (10 790 ₪)"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.markdown(f'<div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #f2f2f7; font-size:14px;"><span>{n}</span><b>{v} ₪</b></div>', unsafe_allow_html=True)

st.write("---")

# ФОРМА ВВОДА
with st.form("add_spend", clear_on_submit=True):
    cat = st.selectbox("КАТЕГОРИЯ", list(LIMITS.keys()))
    amt = st.number_input("СУММА", min_value=0, step=1, value=None, placeholder="Введите сумму ₪")
    if st.form_submit_button("ВНЕСТИ ТРАТУ"):
        if amt:
            try:
                requests.post(SHEET_URL, json={"category": cat, "amount": amt}, timeout=5)
                st.cache_data.clear()
                st.rerun()
            except: st.error("Нет связи с таблицей")
