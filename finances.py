import streamlit as st
import datetime
import requests

# ТВОЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbxkvxn-l1zlwpsXV7EsiuOr1xoFQCThBk6KFbeaIUzD7reCD2zoLMo2hdbpKmizEWxf/exec"

st.set_page_config(page_title="Выход в Ноль", layout="centered")

# 1. ТВОИ 8 КОНВЕРТОВ (АРИНА И НАТАН ОТДЕЛЬНО, ИТОГО + ФИКС = 18 500 ₪)
CATEGORIES = {
    "Продукты": {"limit": 4000, "icon": "🛒", "bg": "#FFEDD5", "color": "#F5A623"},
    "Машина": {"limit": 500, "icon": "🚗", "bg": "#E0F2FE", "color": "#38BDF8"},
    "Лео": {"limit": 300, "icon": "🍼", "bg": "#D1FAE5", "color": "#34D399"},
    "Арина": {"limit": 100, "icon": "👧", "bg": "#F3E8FF", "color": "#A78BFA"},
    "Натан": {"limit": 100, "icon": "👦", "bg": "#E0F2FE", "color": "#38BDF8"},
    "Доп. уроки": {"limit": 2254, "icon": "📚", "bg": "#FEF3C7", "color": "#FBBF24"},
    "Одежда": {"limit": 200, "icon": "👗", "bg": "#FAE8FF", "color": "#E879F9"},
    "Разное": {"limit": 256, "icon": "📦", "bg": "#FFE4E6", "color": "#FB7185"}
}

# 2. ДИЗАЙН "BUDGET PLANNER" (КРАСИВЫЙ И ЧИТАЕМЫЙ)
st.markdown("""
    <style>
    header, footer, #MainMenu, [data-testid="stSidebar"] {visibility: hidden !important; display: none !important;}
    .block-container {padding-top: 1.5rem !important; padding-bottom: 2rem !important;}
    
    html, body, [class*="stApp"] { background-color: #FDFBF7 !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }

    /* Главный виджет */
    .hero-widget {
        background: #FFFFFF; border-radius: 24px; padding: 25px; text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04); margin-bottom: 20px;
    }
    .hero-title { color: #8E8E93; font-size: 16px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .hero-amount { color: #2D3142; font-size: 46px; font-weight: 800; margin: 8px 0; }

    /* Карточки конвертов */
    .budget-card {
        background: #FFFFFF; border-radius: 20px; padding: 18px; margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); display: flex; flex-direction: column; align-items: center;
    }
    .icon-circle {
        width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-size: 26px; margin-bottom: 12px;
    }
    
    .cat-name { color: #8E8E93; font-size: 15px; font-weight: 800; margin-bottom: 6px; text-transform: uppercase; text-align: center; }
    .cat-amount { color: #2D3142; font-size: 26px; font-weight: 800; margin-bottom: 15px; }
    
    /* Полоска прогресса */
    .progress-track { width: 100%; height: 5px; background: #F2F2F7; border-radius: 3px; }
    .progress-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease; }
    
    /* Кнопка */
    .stButton>button {
        background: #2D3142 !important; color: white !important; border-radius: 18px !important;
        height: 56px; font-size: 16px; font-weight: 700; border: none !important; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ЗАГРУЗКА ДАННЫХ
@st.cache_data(ttl=2)
def load_all_data():
    try:
        r = requests.get(SHEET_URL, timeout=5)
        return r.json() if r.status_code == 200 else {"spent": {}, "history": []}
    except: return {"spent": {}, "history": []}

data = load_all_data()
spent = data.get("spent", {})
history = data.get("history", [])

# 4. ГЛАВНЫЙ ОСТАТОК
total_limit = sum(c['limit'] for c in CATEGORIES.values())
total_spent = sum(spent.values())
total_left = total_limit - total_spent

st.markdown(f"""
    <div class="hero-widget">
        <div class="hero-title">МАРТ 2026</div>
        <div class="hero-amount">{int(total_left)} ₪</div>
        <div style="color: #34D399; font-size: 14px; font-weight: 700;">Остаток в конвертах</div>
    </div>
""", unsafe_allow_html=True)

# 5. СЕТКА КАРТОЧЕК
cols = st.columns(2)
for i, (name, info) in enumerate(CATEGORIES.items()):
    limit = info['limit']
    val = limit - spent.get(name, 0)
    pct = max(0, min(1, val / limit)) if limit > 0 else 0
    
    # Красный цвет при перерасходе
    bar_color = info['color'] if val >= 0 else "#FF3B30"
    text_color = "#2D3142" if val >= 0 else "#FF3B30"

    with cols[i % 2]:
        st.markdown(f"""
            <div class="budget-card">
                <div class="icon-circle" style="background-color: {info['bg']}; color: {info['color']};">
                    {info['icon']}
                </div>
                <div class="cat-name">{name}</div>
                <div class="cat-amount" style="color: {text_color};">{int(val)}</div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: {int(pct*100)}%; background-color: {bar_color};"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# 6. ИСТОРИЯ ОПЕРАЦИЙ
if history:
    with st.expander("🕒 ИСТОРИЯ ТРАТ", expanded=True):
        for item in history:
            st.markdown(f'<div style="display:flex; justify-content:space-between; padding:12px 0; border-bottom:1px solid #F2F2F7; font-size:15px;"><span style="color:#8E8E93;">{item["date"]} <b style="color:#2D3142;">{item["category"]}</b></span><span style="color:#FF3B30; font-weight:700;">-{int(item["amount"])} ₪</span></div>', unsafe_allow_html=True)

st.write("---")

# 7. ФОРМА ВВОДА
with st.form("add_transaction", clear_on_submit=True):
    cat = st.selectbox("Категория", list(CATEGORIES.keys()))
    amt = st.number_input("Сумма", min_value=0, step=1, value=None, placeholder="₪")
    if st.form_submit_button("ВНЕСТИ ТРАТУ"):
        if amt:
            try:
                requests.post(SHEET_URL, json={"category": cat, "amount": amt}, timeout=5)
                st.cache_data.clear()
                st.rerun()
            except:
                pass

# 8. ОБЯЗАТЕЛЬНЫЕ ПЛАТЕЖИ ВНИЗУ
st.write("---")
with st.expander("🔒 ОБЯЗАТЕЛЬНЫЕ ПЛАТЕЖИ (10 790 ₪)"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.markdown(f'<div style="display:flex; justify-content:space-between; font-size:15px; padding:8px 0; border-bottom:1px solid #f2f2f7;"><span>{n}</span><b style="color:#2D3142;">{v} ₪</b></div>', unsafe_allow_html=True)
