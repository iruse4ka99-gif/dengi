import streamlit as st
import datetime
import requests

# ТВОЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbxkvxn-l1zlwpsXV7EsiuOr1xoFQCThBk6KFbeaIUzD7reCD2zoLMo2hdbpKmizEWxf/exec"

st.set_page_config(page_title="Выход в Ноль", layout="centered")

# 1. КОНВЕРТЫ (ИТОГО + ФИКС = 18 500 ₪)
CATEGORIES = {
    "Продукты": {"limit": 4000, "icon": "🍎", "color": "#FFF9E5"},
    "Дети (А&Н)": {"limit": 200, "icon": "👫", "color": "#F3E5FF"},
    "Лео": {"limit": 300, "icon": "👶", "color": "#E5FFF3"},
    "Машина": {"limit": 500, "icon": "🚗", "color": "#E5F1FF"},
    "Доп. уроки": {"limit": 2254, "icon": "📚", "color": "#FFF0E5"},
    "Одежда": {"limit": 200, "icon": "👕", "color": "#FFE5F1"},
    "Разное": {"limit": 256, "icon": "📦", "color": "#F2F2F7"}
}

# 2. ОПТИМИЗИРОВАННЫЙ ДИЗАЙН (КОМПАКТНЫЙ РАЗМЕР)
st.markdown("""
    <style>
    header, footer, #MainMenu, [data-testid="stSidebar"] {visibility: hidden !important; display: none !important;}
    .block-container {padding-top: 0.5rem !important; padding-bottom: 1rem !important;}
    html, body, [class*="stApp"] { background-color: #ffffff !important; }

    /* Компактные карточки */
    .item-card {
        border-radius: 20px; padding: 15px; margin-bottom: 10px;
        border: 1px solid rgba(0,0,0,0.02);
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    .item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px; }
    .item-name { font-size: 9px; font-weight: 800; color: #8e8e93; text-transform: uppercase; }
    
    /* Тонкие линии */
    .p-bar-bg { height: 3px; background: rgba(0,0,0,0.05); border-radius: 2px; margin-top: 8px; }
    .p-bar-fill { height: 100%; border-radius: 2px; transition: all 0.5s ease; }
    
    /* Кнопка */
    .stButton>button {
        background: #30d158 !important; color: white !important; border-radius: 16px !important;
        height: 50px; font-size: 16px; font-weight: 700; border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_status_color(pct):
    if pct > 0.5: return "#30d158"
    if pct > 0.15: return "#ff9f0a"
    return "#ff3b30"

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

# 4. ГЛАВНЫЙ ЭКРАН (УМЕНЬШЕННЫЙ ЗАГОЛОВОК)
total_left = sum(c['limit'] for c in CATEGORIES.values()) - sum(spent.values())
main_color = get_status_color(total_left / sum(c['limit'] for c in CATEGORIES.values()))

st.markdown(f"""
    <div style="text-align:center; padding: 15px 0;">
        <h1 style="font-size:42px; font-weight:200; margin:0; color:{main_color};">{int(total_left)} ₪</h1>
        <p style="color:#8e8e93; font-weight:800; font-size:10px; margin:0; letter-spacing:1px;">МАРТ 2026</p>
    </div>
""", unsafe_allow_html=True)

# СЕТКА КОНВЕРТОВ (БОЛЕЕ АККУРАТНАЯ)
cols = st.columns(2)
for i, (name, info) in enumerate(CATEGORIES.items()):
    val = info['limit'] - spent.get(name, 0)
    pct = max(0, min(1, val / info['limit']))
    color = get_status_color(pct)
    val_color = color if pct < 0.25 else "#1c1c1e"
    if val < 0: val_color = "#ff3b30"

    with cols[i % 2]:
        st.markdown(f"""
            <div class="item-card" style="background-color: {info['color']};">
                <div class="item-header">
                    <span class="item-name">{name}</span>
                    <span style="font-size:16px;">{info['icon']}</span>
                </div>
                <div style="font-size:22px; font-weight:600; color:{val_color};">
                    {int(val)}
                </div>
                <div class="p-bar-bg">
                    <div class="p-bar-fill" style="width: {int(pct*100)}%; background: {color};"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ИСТОРИЯ
if history:
    with st.expander("🕒 ИСТОРИЯ"):
        for item in history:
            st.markdown(f'<div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #f2f2f7; font-size:12px;"><span>{item["date"]} <b>{item["category"]}</b></span><span style="color:#ff3b30;">-{int(item["amount"])} ₪</span></div>', unsafe_allow_html=True)

st.write("---")

# ФОРМА ВВОДА (БОЛЕЕ ПЛОТНАЯ)
with st.form("add_transaction", clear_on_submit=True):
    cat = st.selectbox("Категория", list(CATEGORIES.keys()))
    amt = st.number_input("Сумма", min_value=0, step=1, value=None, placeholder="₪")
    if st.form_submit_button("ВНЕСТИ ТРАТУ"):
        if amt:
            requests.post(SHEET_URL, json={"category": cat, "amount": amt})
            st.cache_data.clear()
            st.rerun()
