import streamlit as st
import datetime
import requests

# ТВОЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbxkvxn-l1zlwpsXV7EsiuOr1xoFQCThBk6KFbeaIUzD7reCD2zoLMo2hdbpKmizEWxf/exec"

st.set_page_config(page_title="Выход в Ноль", layout="centered")

# 1. КОНВЕРТЫ С ИКОНКАМИ И ЦВЕТАМИ (ИТОГО + ФИКС = 18 500 ₪)
# Я подобрал цвета как на твоих скриншотах
CATEGORIES = {
    "Продукты": {"limit": 4000, "icon": "🍎", "color": "#FFF9E5"},
    "Машина": {"limit": 500, "icon": "🚗", "color": "#E5F1FF"},
    "Одежда": {"limit": 200, "icon": "👕", "color": "#FFE5F1"},
    "Арина": {"limit": 100, "icon": "👧", "color": "#F3E5FF"},
    "Натан": {"limit": 100, "icon": "👦", "color": "#E5F9FF"},
    "Лео": {"limit": 300, "icon": "👶", "color": "#E5FFF3"},
    "Доп. уроки": {"limit": 2254, "icon": "📚", "color": "#FFF0E5"},
    "Разное": {"limit": 256, "icon": "📦", "color": "#F2F2F7"}
}

# 2. СТИЛИ (МАКСИМАЛЬНО БЛИЗКО К СКРИНШОТАМ)
st.markdown("""
    <style>
    header, footer, #MainMenu, [data-testid="stSidebar"] {visibility: hidden !important; display: none !important;}
    .block-container {padding-top: 1rem !important;}
    
    html, body, [class*="stApp"] { background-color: #ffffff !important; }

    /* Главный круг из скриншота "Smart Budgeting" */
    .hero-container { text-align: center; padding: 20px 0; }
    .main-circle {
        width: 180px; height: 180px; border-radius: 90px;
        margin: 0 auto; display: flex; align-items: center; justify-content: center;
        border: 12px solid #30d158;
        box-shadow: 0 15px 35px rgba(48,209,88,0.1);
    }
    
    /* Карточки как в "Budget Planner" */
    .item-card {
        border-radius: 22px; padding: 18px; margin-bottom: 12px;
        border: 1px solid rgba(0,0,0,0.03);
        display: flex; flexDirection: column; justify-content: space-between;
    }
    .item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .item-icon { font-size: 20px; }
    .item-name { font-size: 11px; font-weight: 700; color: #8e8e93; text-transform: uppercase; }
    .item-value { font-size: 24px; font-weight: 600; color: #1c1c1e; }
    
    /* Тонкий прогресс-бар */
    .p-bar-bg { height: 4px; background: rgba(0,0,0,0.05); border-radius: 2px; margin-top: 8px; }
    .p-bar-fill { height: 100%; border-radius: 2px; }
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

# 4. ИНТЕРФЕЙС (ГЛАВНЫЙ ЭКРАН)
total_limit = sum(c['limit'] for c in CATEGORIES.values())
total_spent = sum(spent.values())
total_left = total_limit - total_spent

st.markdown(f'<div class="hero-container"><p style="color:#8e8e93; font-weight:700; font-size:12px;">МАРТ 2026</p></div>', unsafe_allow_html=True)

# КРУГ ОСТАТКА
st.markdown(f"""
    <div class="hero-container">
        <div class="main-circle">
            <div>
                <div style="font-size:44px; font-weight:300;">{int(total_left)}</div>
                <div style="font-size:10px; font-weight:700; color:#30d158;">ОСТАТОК ₪</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# СЕТКА КАТЕГОРИЙ (2 в ряд)
cols = st.columns(2)
for i, (name, info) in enumerate(CATEGORIES.items()):
    val = info['limit'] - spent.get(name, 0)
    pct = max(0, min(1, val / info['limit']))
    color = "#30d158" if pct > 0.3 else "#ff3b30"
    
    with cols[i % 2]:
        st.markdown(f"""
            <div class="item-card" style="background-color: {info['color']};">
                <div class="item-header">
                    <span class="item-name">{name}</span>
                    <span class="item-icon">{info['icon']}</span>
                </div>
                <div class="item-value">{int(val)} ₪</div>
                <div class="p-bar-bg">
                    <div class="p-bar-fill" style="width: {int(pct*100)}%; background: {color};"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ФОРМА (Сделаем её очень простой)
with st.form("quick_add", clear_on_submit=True):
    st.markdown('<p style="font-size:12px; font-weight:700; color:#8e8e93;">ВНЕСТИ НОВУЮ ТРАТУ</p>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1: cat = st.selectbox("Что?", list(CATEGORIES.keys()))
    with c2: amt = st.number_input("Сколько?", min_value=0, step=1, value=None, placeholder="₪")
    if st.form_submit_button("СОХРАНИТЬ В ОБЛАКО"):
        if amt:
            try:
                requests.post(SHEET_URL, json={"category": cat, "amount": amt}, timeout=5)
                st.cache_data.clear()
                st.rerun()
            except: st.error("Ошибка!")

# ФИКСИРОВАННЫЕ ВНИЗУ
with st.expander("🔒 Обязательные платежи (10 790 ₪)"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.markdown(f'<div style="display:flex; justify-content:space-between; font-size:14px; padding:5px 0;"><span>{n}</span><b>{v} ₪</b></div>', unsafe_allow_html=True)
