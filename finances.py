import streamlit as st
import datetime
import requests

SHEET_URL = "https://script.google.com/macros/s/AKfycbxkvxn-l1zlwpsXV7EsiuOr1xoFQCThBk6KFbeaIUzD7reCD2zoLMo2hdbpKmizEWxf/exec"

st.set_page_config(page_title="Выход в Ноль", layout="centered")

# ЛИМИТЫ (ИТОГО + ФИКС = 18 500 ₪)
CATEGORIES = {
    "Продукты": {"limit": 4000, "icon": "🛒", "bg": "#FFEDD5", "color": "#F5A623"},
    "Машина": {"limit": 500, "icon": "🚗", "bg": "#E0F2FE", "color": "#38BDF8"},
    "Лео": {"limit": 300, "icon": "🍼", "bg": "#D1FAE5", "color": "#34D399"},
    "Арина": {"limit": 100, "icon": "👧", "bg": "#F3E8FF", "color": "#A78BFA"},
    "Натан": {"limit": 100, "icon": "👦", "bg": "#E0F2FE", "color": "#38BDF8"},
    "Доп. уроки": {"limit": 2254, "icon": "📚", "bg": "#FEF3C7", "color": "#FBBF24"},
    "Одежда": {"limit": 200, "icon": "👕", "bg": "#FAE8FF", "color": "#E879F9"},
    "Разное": {"limit": 256, "icon": "📦", "bg": "#FFE4E6", "color": "#FB7185"}
}

st.markdown("""
    <style>
    header, footer, #MainMenu, [data-testid="stSidebar"] {visibility: hidden !important; display: none !important;}
    html, body, [class*="stApp"] { background-color: #FDFBF7 !important; }
    .hero-widget { background: #FFFFFF; border-radius: 24px; padding: 25px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.04); margin-bottom: 20px; }
    .budget-card { background: #FFFFFF; border-radius: 20px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); display: flex; flex-direction: column; align-items: center; }
    .cat-name { color: #8E8E93; font-size: 14px; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; }
    .cat-amount { color: #2D3142; font-size: 28px; font-weight: 800; margin-bottom: 12px; }
    .progress-track { width: 100%; height: 6px; background: #F2F2F7; border-radius: 3px; }
    .progress-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease; }
    .stButton>button { background: #2D3142 !important; color: white !important; border-radius: 20px !important; height: 60px; font-size: 18px; font-weight: 700; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=0)
def load_data():
    try:
        r = requests.get(SHEET_URL, timeout=10)
        return r.json()
    except: return {"spent": {}, "history": []}

data = load_data()
spent = data.get("spent", {})
history = data.get("history", [])

total_left = sum(c['limit'] for c in CATEGORIES.values()) - sum(spent.values())

st.markdown(f'<div class="hero-widget"><div style="font-size:14px; font-weight:700; color:#8E8E93;">МАРТ 2026</div><div style="font-size:48px; font-weight:800; color:#2D3142;">{int(total_left)} ₪</div><div style="color:#34D399; font-weight:700;">ОСТАТОК В КОНВЕРТАХ</div></div>', unsafe_allow_html=True)

cols = st.columns(2)
for i, (name, info) in enumerate(CATEGORIES.items()):
    limit = info['limit']
    val = limit - spent.get(name, 0)
    pct = max(0, min(1, val / limit)) if limit > 0 else 0
    with cols[i % 2]:
        st.markdown(f"""
            <div class="budget-card">
                <div style="width:50px; height:50px; border-radius:50%; background:{info['bg']}; display:flex; align-items:center; justify-content:center; font-size:24px; margin-bottom:10px;">{info['icon']}</div>
                <div class="cat-name">{name}</div>
                <div class="cat-amount" style="color:{'#FF3B30' if val < 0 else '#2D3142'};">{int(val)}</div>
                <div class="progress-track"><div class="progress-fill" style="width:{int(pct*100)}%; background-color:{info['color'] if val >= 0 else '#FF3B30'};"></div></div>
            </div>
        """, unsafe_allow_html=True)

if history:
    with st.expander("🕒 ИСТОРИЯ ОПЕРАЦИЙ", expanded=True):
        for item in history:
            st.markdown(f'<div style="display:flex; justify-content:space-between; padding:12px 0; border-bottom:1px solid #F2F2F7; font-size:14px;"><span>{item["date"]} <b>{item["category"]}</b></span><span style="color:#FF3B30; font-weight:700;">-{int(item["amount"])} ₪</span></div>', unsafe_allow_html=True)

st.write("---")
with st.form("add_form", clear_on_submit=True):
    cat = st.selectbox("Категория", list(CATEGORIES.keys()))
    amt = st.number_input("Сумма", min_value=0, step=1, value=None, placeholder="₪")
    if st.form_submit_button("ВНЕСТИ ТРАТУ") and amt:
        requests.post(SHEET_URL, json={"category": cat, "amount": amt})
        st.cache_data.clear()
        st.rerun()

with st.expander("🔒 ОБЯЗАТЕЛЬНЫЕ ПЛАТЕЖИ (10 790 ₪)"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.write(f"**{n}**: {v} ₪")
