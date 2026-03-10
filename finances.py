import streamlit as st
import datetime
import requests

# ТВОЯ АКТИВНАЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbyrvgESsKjWIaw0gVohS3reEOV_kvinEoEQpbC09Fnihq-fn88FigvDJWdW8tGa2TmA/exec"

# ТВОЙ ДОЛГ ЗА КВАРТИРУ
TOTAL_DEBT_START = 450000 

st.set_page_config(page_title="Выход в Ноль", layout="centered")

# КАТЕГОРИИ
CATEGORIES = {
    "Продукты": {"limit": 4000, "icon": "🛒", "icon_bg": "#FFB74D", "card_bg": "#FFF8E1"}, 
    "Квартира": {"limit": 6000, "icon": "🏠", "icon_bg": "#795548", "card_bg": "#EFEBE9"}, 
    "Машина": {"limit": 500, "icon": "🚗", "icon_bg": "#64B5F6", "card_bg": "#E3F2FD"}, 
    "Лео": {"limit": 300, "icon": "🍼", "icon_bg": "#4DB6AC", "card_bg": "#E0F2F1"}, 
    "Арина": {"limit": 100, "icon": "👧", "icon_bg": "#BA68C8", "card_bg": "#F3E5F5"}, 
    "Натан": {"limit": 100, "icon": "👦", "icon_bg": "#4DD0E1", "card_bg": "#E0F7FA"}, 
    "Доп. уроки": {"limit": 2254, "icon": "📚", "icon_bg": "#FF8A65", "card_bg": "#FBE9E7"}, 
    "Одежда": {"limit": 200, "icon": "👕", "icon_bg": "#F06292", "card_bg": "#FCE4EC"}, 
    "Разное": {"limit": 256, "icon": "📦", "icon_bg": "#AED581", "card_bg": "#F1F8E9"},
    "Работа (Артём)": {"limit": 0, "icon": "💼", "icon_bg": "#90A4AE", "card_bg": "#ECEFF1"}
}

st.markdown("""
    <style>
    header, footer, #MainMenu, [data-testid="stSidebar"] {visibility: hidden !important; display: none !important;}
    
    /* ЦВЕТ КОЖИ ДЛЯ ФОНА */
    html, body, [class*="stApp"] { background-color: #FDFBF7 !important; }
    
    .hero-widget { background: #FFFFFF; border-radius: 20px; padding: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 10px; }
    [data-testid="stForm"] { background: #FFFFFF; border-radius: 15px; padding: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.02); margin-bottom: 15px;}
    
    /* УМЕНЬШЕННЫЕ ПЛИТКИ */
    .budget-card { 
        border-radius: 18px; padding: 12px; margin-bottom: 10px; 
        display: flex; flex-direction: column; align-items: center; 
        transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    
    .icon-circle { width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 8px; }
    .cat-name { color: #8E8E93; font-size: 11px; font-weight: 800; text-transform: uppercase; margin-bottom: 4px; }
    .cat-amount { font-size: 20px; font-weight: 800; margin-bottom: 6px; }
    
    .progress-track { width: 100%; height: 4px; background: rgba(0,0,0,0.05); border-radius: 2px; }
    .progress-fill { height: 100%; border-radius: 2px; transition: width 0.3s ease; }
    
    .stButton>button { background: #2D3142 !important; color: white !important; border-radius: 15px !important; height: 45px; font-size: 14px; font-weight: 700; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    try:
        r = requests.get(SHEET_URL, timeout=10)
        return r.json()
    except: return {"spent": {}, "history": []}

data = load_data()
spent_dict = data.get("spent", {})
history = data.get("history", [])

now = datetime.datetime.now()
months_passed = (now.year - 2026) * 12 + (now.month - 3) + 1
if months_passed < 1: months_passed = 1

total_spent = sum(v for k, v in spent_dict.items() if k in CATEGORIES and CATEGORIES[k]['limit'] > 0)
total_limit = sum(c['limit'] * months_passed for c in CATEGORIES.values())
total_left = total_limit - total_spent

# ГЛАВНЫЙ ВИДЖЕТ
st.markdown(f'<div class="hero-widget"><div style="font-size:12px; font-weight:700; color:#8E8E93;">{now.strftime("%d.%m.%Y")}</div><div style="font-size:36px; font-weight:800; color:#2D3142;">{int(total_left)} ₪</div><div style="color:#34D399; font-weight:700; font-size:12px;">ОСТАТОК В КОНВЕРТАХ</div></div>', unsafe_allow_html=True)

# ФОРМА
with st.form("add_transaction", clear_on_submit=True):
    cat = st.selectbox("Куда?", list(CATEGORIES.keys()))
    amt = st.number_input("Сколько?", min_value=0, step=1, value=None, placeholder="₪")
    if st.form_submit_button("ВНЕСТИ ТРАТУ") and amt:
        requests.post(SHEET_URL, json={"category": cat, "amount": amt})
        st.rerun()

# СЕТКА ПЛИТОК
cols = st.columns(2)
for i, (name, info) in enumerate(CATEGORIES.items()):
    spent = spent_dict.get(name, 0)
    
    if name == "Квартира":
        val = TOTAL_DEBT_START - spent
        card_bg = info['card_bg']; icon_bg = info['icon_bg']; text_color = "#2D3142"
        pct_text = "🏠"; bar_color = "#34D399"; pct = 1.0
    elif info['limit'] == 0:
        val = spent
        card_bg = info['card_bg']; icon_bg = info['icon_bg']; text_color = "#2D3142"
        pct_text = "💼"; bar_color = "#90A4AE"; pct = 0
    else:
        current_val = (info['limit'] * months_passed) - spent
        val = current_val
        pct = max(0, min(1, current_val / info['limit'])) if info['limit'] > 0 else 0
        pct_text = f"{int(pct*100)}%"
        
        if current_val < 0 or pct <= 0.10:
            card_bg = "#FFEBEB"; icon_bg = "#FF5252"; text_color = "#FF5252"; bar_color = "#FF5252"
        elif pct <= 0.30:
            card_bg = "#FFF8E1"; icon_bg = "#FFB300"; text_color = "#2D3142"; bar_color = "#FFB300"
        else:
            card_bg = info['card_bg']; icon_bg = info['icon_bg']; text_color = "#2D3142"; bar_color = "#34D399"

    html_card = f"""
    <div class="budget-card" style="background-color:{card_bg};">
        <div class="icon-circle" style="background:{icon_bg}; color:#FFFFFF;">{info['icon']}</div>
        <div class="cat-name">{name}</div>
        <div class="cat-amount" style="color:{text_color};">{int(val)} ₪</div>
        <div style="width:100%; text-align:right; font-size:10px; font-weight:700; color:#8E8E93; opacity:0.6; margin-bottom:2px;">{pct_text}</div>
        <div class="progress-track"><div class="progress-fill" style="width:{int(pct*100)}%; background-color:{bar_color};"></div></div>
    </div>
    """
    with cols[i % 2]:
        st.markdown(html_card.replace('\n', ''), unsafe_allow_html=True)

# ПОДВАЛ
with st.expander("🕒 ИСТОРИЯ"):
    if history:
        for item in history:
            st.markdown(f'<div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(0,0,0,0.05); font-size:13px;"><span>{item["date"]} <b>{item["category"]}</b></span><span style="color:#FF3B30; font-weight:700;">-{int(item["amount"])} ₪</span></div>', unsafe_allow_html=True)

with st.expander("🔒 ОБЯЗАТЕЛЬНЫЕ ПЛАТЕЖИ"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.write(f"**{n}**: {v} ₪")

with st.expander("🔄 ПЕРЕВОД"):
    with st.form("transfer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1: cat_from = st.selectbox("Откуда?", [k for k in CATEGORIES.keys() if CATEGORIES[k]['limit'] > 0], index=5)
        with col2: cat_to = st.selectbox("Куда?", [k for k in CATEGORIES.keys() if CATEGORIES[k]['limit'] > 0], index=0)
        transfer_amt = st.number_input("Сумма", min_value=1, step=1, value=None)
        if st.form_submit_button("OK"):
            if cat_from != cat_to:
                requests.post(SHEET_URL, json={"category": cat_from, "amount": transfer_amt})
                requests.post(SHEET_URL, json={"category": cat_to, "amount": -transfer_amt})
                st.rerun()
