import streamlit as st
import datetime
import requests

# ТВОЯ АКТИВНАЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbyrvgESsKjWIaw0gVohS3reEOV_kvinEoEQpbC09Fnihq-fn88FigvDJWdW8tGa2TmA/exec"

# СУММА КВАРТИРЫ
TOTAL_DEBT_START = 200000 

st.set_page_config(page_title="Выход в Ноль", layout="centered")

# КАТЕГОРИИ
CATEGORIES = {
    "Продукты": {"limit": 4000, "icon": "🛒", "icon_bg": "#FFB74D", "card_bg": "#FFF8E1"}, 
    "Машина": {"limit": 500, "icon": "🚗", "icon_bg": "#64B5F6", "card_bg": "#E3F2FD"}, 
    "Лео": {"limit": 300, "icon": "🍼", "icon_bg": "#4DB6AC", "card_bg": "#E0F2F1"}, 
    "Арина": {"limit": 100, "icon": "👧", "icon_bg": "#BA68C8", "card_bg": "#F3E5F5"}, 
    "Натан": {"limit": 100, "icon": "👦", "icon_bg": "#4DD0E1", "card_bg": "#E0F7FA"}, 
    "Доп. уроки": {"limit": 2254, "icon": "📚", "icon_bg": "#FF8A65", "card_bg": "#FBE9E7"}, 
    "Одежда": {"limit": 200, "icon": "👕", "icon_bg": "#F06292", "card_bg": "#FCE4EC"}, 
    "Разное": {"limit": 256, "icon": "📦", "icon_bg": "#AED581", "card_bg": "#F1F8E9"},
    "Квартира": {"limit": 0, "icon": "🏠", "icon_bg": "#795548", "card_bg": "#EFEBE9"}, 
    "Работа (Артём)": {"limit": 0, "icon": "💼", "icon_bg": "#90A4AE", "card_bg": "#ECEFF1"}
}

st.markdown("""
    <style>
    header, footer, #MainMenu, [data-testid="stSidebar"] {visibility: hidden !important; display: none !important;}
    
    /* ФОН ЦВЕТА КОЖИ */
    html, body, [class*="stApp"] { background-color: #FDFBF7 !important; }
    
    .hero-widget { background: #FFFFFF; border-radius: 20px; padding: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 10px; }
    [data-testid="stForm"] { background: #FFFFFF; border-radius: 18px; padding: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.02); margin-bottom: 15px;}
    
    /* СТРОЧНЫЙ ДИЗАЙН ПЛИТКИ */
    .budget-row { 
        border-radius: 15px; 
        padding: 10px 15px; 
        margin-bottom: 8px; 
        display: flex; 
        flex-direction: row; 
        align-items: center; 
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    
    .left-content { display: flex; align-items: center; gap: 12px; }
    
    .icon-circle { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; }
    
    .cat-name { color: #8E8E93; font-size: 13px; font-weight: 800; text-transform: uppercase; }
    
    /* КРУПНЫЙ ШРИФТ ДЛЯ ДЕНЕГ */
    .cat-amount { font-size: 22px; font-weight: 800; color: #2D3142; }
    
    /* ПОЛОСКА ПРОГРЕССА В САМОМ НИЗУ */
    .row-progress { position: absolute; bottom: 0; left: 0; height: 3px; background: rgba(0,0,0,0.05); width: 100%; }
    .row-fill { height: 100%; transition: width 0.3s ease; }
    
    .stButton>button { background: #2D3142 !important; color: white !important; border-radius: 15px !important; height: 50px; font-size: 16px; font-weight: 700; width: 100%; }
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

# 1. ГЛАВНЫЙ ВИДЖЕТ
st.markdown(f'<div class="hero-widget"><div style="font-size:12px; font-weight:700; color:#8E8E93;">{now.strftime("%d.%m.%Y")}</div><div style="font-size:42px; font-weight:800; color:#2D3142;">{int(total_left)} ₪</div><div style="color:#34D399; font-weight:700; font-size:14px;">ОСТАТОК В КОНВЕРТАХ</div></div>', unsafe_allow_html=True)

# 2. ФОРМА
with st.form("add_transaction", clear_on_submit=True):
    cat = st.selectbox("Что вносим?", list(CATEGORIES.keys()))
    amt = st.number_input("Сколько?", min_value=0, step=1, value=None, placeholder="₪")
    if st.form_submit_button("ВНЕСТИ ЗАПИСЬ") and amt:
        requests.post(SHEET_URL, json={"category": cat, "amount": amt})
        st.rerun()

# 3. СПИСОК СТРОКАМИ (В РЯД)
for name, info in CATEGORIES.items():
    spent = spent_dict.get(name, 0)
    
    if name == "Квартира":
        val = TOTAL_DEBT_START - spent
        card_bg = info['card_bg']; icon_bg = info['icon_bg']; text_color = "#2D3142"
        bar_html = f'<div class="row-progress"><div class="row-fill" style="width:100%; background-color:#34D399;"></div></div>'
    elif info['limit'] == 0: # Работа Артёма
        val = spent
        card_bg = info['card_bg']; icon_bg = info['icon_bg']; text_color = "#2D3142"
        bar_html = ""
    else:
        current_val = (info['limit'] * months_passed) - spent
        val = current_val
        pct = max(0, min(1, current_val / info['limit'])) if info['limit'] > 0 else 0
        
        # Светофор
        if current_val < 0 or pct <= 0.10:
            card_bg = "#FFEBEB"; icon_bg = "#FF5252"; text_color = "#FF5252"; bar_color = "#FF5252"
        elif pct <= 0.30:
            card_bg = "#FFF8E1"; icon_bg = "#FFB300"; text_color = "#2D3142"; bar_color = "#FFB300"
        else:
            card_bg = info['card_bg']; icon_bg = info['icon_bg']; text_color = "#2D3142"; bar_color = "#34D399"
        
        bar_html = f'<div class="row-progress"><div class="row-fill" style="width:{int(pct*100)}%; background-color:{bar_color};"></div></div>'

    html_row = f"""
    <div class="budget-row" style="background-color:{card_bg};">
        <div class="left-content">
            <div class="icon-circle" style="background:{icon_bg}; color:#FFFFFF;">{info['icon']}</div>
            <div class="cat-name">{name}</div>
        </div>
        <div class="cat-amount" style="color:{text_color};">{int(val)} ₪</div>
        {bar_html}
    </div>
    """
    st.markdown(html_row.replace('\n', ''), unsafe_allow_html=True)

# ПОДВАЛ
with st.expander("🕒 ИСТОРИЯ"):
    if history:
        for item in history:
            st.markdown(f'<div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid rgba(0,0,0,0.05); font-size:14px;"><span>{item["date"]} <b>{item["category"]}</b></span><span style="color:#FF3B30; font-weight:700;">-{int(item["amount"])} ₪</span></div>', unsafe_allow_html=True)

with st.expander("🔒 ОБЯЗАТЕЛЬНЫЕ ПЛАТЕЖИ"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.write(f"**{n}**: {v} ₪")

with st.expander("🔄 ПЕРЕВОД МЕЖДУ КОНВЕРТАМИ"):
    with st.form("transfer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1: cat_from = st.selectbox("Откуда?", [k for k in CATEGORIES.keys() if CATEGORIES[k]['limit'] > 0], index=5)
        with col2: cat_to = st.selectbox("Куда?", list(CATEGORIES.keys()), index=8)
        transfer_amt = st.number_input("Сумма", min_value=1, step=1, value=None)
        
        # ИСПРАВЛЕННАЯ ОШИБКА: теперь деньги и списываются, и зачисляются!
        if st.form_submit_button("ОК"):
            if cat_from != cat_to and transfer_amt:
                requests.post(SHEET_URL, json={"category": cat_from, "amount": transfer_amt})
                requests.post(SHEET_URL, json={"category": cat_to, "amount": -transfer_amt})
                st.rerun()
