import streamlit as st
import datetime
import requests

# ТВОЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbxkvxn-l1zlwpsXV7EsiuOr1xoFQCThBk6KFbeaIUzD7reCD2zoLMo2hdbpKmizEWxf/exec"

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# 1. ДИЗАЙН (СВЕТОФОР И ГРАФИКА)
st.markdown("""
    <style>
    html, body, [class*="stApp"] { background-color: #f2f2f7 !important; color: #1c1c1e !important; }
    header, footer {visibility: hidden;}
    /* Кнопка Внести */
    .stButton>button {
        background-color: #30d158 !important; color: white !important; border-radius: 15px !important;
        height: 50px; width: 100%; font-weight: 700; border: none !important; box-shadow: 0 4px 10px rgba(48,209,88,0.3);
    }
    /* Карточки конвертов */
    .envelope-card {
        background-color: white; border-radius: 24px; padding: 20px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #e5e5ea;
    }
    .status-dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 5px; }
    /* Фиксированные расходы */
    .fixed-box { background: white; border-radius: 24px; padding: 25px; border: 1px solid #e5e5ea; }
    .fixed-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #f2f2f7; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 2. КОНВЕРТЫ (Лимиты на месяц)
LIMITS = {
    "Продукты": 4000, "Машина": 500, "Одежда": 200, 
    "Арина": 100, "Натан": 100, "Лео": 600, 
    "Доп. уроки": 2254, "Разное": 556
}

# 3. ЗАГРУЗКА ИЗ ОБЛАКА
@st.cache_data(ttl=5)
def get_data():
    try:
        r = requests.get(SHEET_URL, timeout=5)
        return r.json() if r.status_code == 200 else {}
    except: return {}

spent_db = get_data()

# 4. ЛОГИКА "СВЕТОФОРА"
def get_status(pct):
    if pct > 0.5: return "#30d158" # Зеленый
    if pct > 0.2: return "#ff9f0a" # Оранжевый
    return "#ff3b30"               # Красный

# 5. ИНТЕРФЕЙС
fixed_costs = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
now = datetime.datetime.now()
st.markdown(f'<div style="text-align:center; padding:20px 0; color:#8e8e93; font-weight:600; letter-spacing:1px;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3.5, 1.2])

with main_c:
    # ГЛАВНЫЙ ИНДИКАТОР
    balances = {n: (v - spent_db.get(n, 0)) for n, v in LIMITS.items()}
    total_left = sum(balances.values())
    total_limit = sum(LIMITS.values())
    total_pct = total_left / total_limit if total_limit > 0 else 0
    
    st.markdown(f"""
        <div style="text-align:center; margin-bottom:40px;">
            <h1 style="font-size:56px; font-weight:300; margin:0; color:#1c1c1e;">{int(total_left)} ₪</h1>
            <p style="color:{get_status(total_pct)}; font-weight:700; font-size:12px; margin:0;">ОСТАТОК В КОНВЕРТАХ</p>
        </div>
    """, unsafe_allow_html=True)

    # СЕТКА КОНВЕРТОВ (СВЕТОФОР)
    for i in range(0, len(LIMITS), 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx < len(LIMITS):
                name = list(LIMITS.keys())[idx]
                bal = balances[name]
                pct = bal / LIMITS[name] if LIMITS[name] > 0 else 0
                color = get_status(pct)
                with cols[j]:
                    st.markdown(f"""
                        <div class="envelope-card">
                            <div style="font-size:10px; color:#8e8e93; font-weight:700; margin-bottom:10px;">
                                <span class="status-dot" style="background-color:{color};"></span>{name.upper()}
                            </div>
                            <div style="font-size:26px; color:#1c1c1e; font-weight:400;">{int(bal)}</div>
                            <div style="height:3px; background:#f2f2f7; border-radius:2px; margin-top:10px;">
                                <div style="width:{int(pct*100)}%; height:100%; background:{color}; border-radius:2px;"></div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

with side_c:
    st.markdown('<div class="fixed-box">', unsafe_allow_html=True)
    st.write("🔒 **ФИКСИРОВАНО**")
    for n, v in fixed_costs.items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span style="font-weight:600;">{v} ₪</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")
# ФОРМА ВВОДА
with st.form("spend_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([1.5, 1, 1])
    with c1: cat = st.selectbox("Куда потратили?", list(LIMITS.keys()))
    with c2: amt = st.number_input("Сколько?", min_value=0, step=1, value=None, placeholder="₪")
    with c3:
        if st.form_submit_button("ВНЕСТИ ТРАТУ") and amt:
            try:
                requests.post(SHEET_URL, json={"category": cat, "amount": amt}, timeout=5)
                st.balloons()
                st.cache_data.clear()
                st.rerun()
            except: st.error("Ошибка связи")
