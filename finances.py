import streamlit as st
import datetime
import requests

# ТВОЯ АКТИВНАЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbyrvgESsKjWIaw0gVohS3reEOV_kvinEoEQpbC09Fnihq-fn88FigvDJWdW8tGa2TmA/exec"

st.set_page_config(page_title="Выход в Ноль", layout="centered")

# ЦВЕТА (Работа Артема - просто счетчик без лимита)
CATEGORIES = {
    "Продукты": {"limit": 4000, "icon": "🛒", "icon_bg": "#FFB74D", "card_bg": "#FFF8E1"}, 
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
    html, body, [class*="stApp"] { background-color: #FDFBF7 !important; }
    .hero-widget { background: #FFFFFF; border-radius: 24px; padding: 25px; text-align: center; box-shadow: 0 8px 20px rgba(0,0,0,0.04); margin-bottom: 15px; }
    [data-testid="stForm"] { background: #FFFFFF; border-radius: 20px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid rgba(0,0,0,0.02); margin-bottom: 12px;}
    .budget-card { border-radius: 20px; padding: 18px; margin-bottom: 12px; display: flex; flex-direction: column; align-items: center; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(0,0,0,0.02);}
    .cat-name { color: #8E8E93; font-size: 13px; font-weight: 800; text-transform: uppercase; margin-bottom: 6px; }
    .cat-amount { font-size: 26px; font-weight: 800; margin-bottom: 8px; }
    .progress-track { width: 100%; height: 6px; background: rgba(0,0,0,0.05); border-radius: 3px; }
    .progress-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease, background-color 0.3s ease; }
    .stButton>button { background: #2D3142 !important; color: white !important; border-radius: 18px !important; height: 55px; font-size: 16px; font-weight: 700; width: 100%; }
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

# Считаем общий расход ТОЛЬКО по личным конвертам
total_spent = sum(v for k, v in spent_dict.items() if k in CATEGORIES and CATEGORIES[k]['limit'] > 0)
total_limit = sum(c['limit'] * months_passed for c in CATEGORIES.values())
total_left = total_limit - total_spent

# 1. ГЛАВНЫЙ ВИДЖЕТ
st.markdown(f'<div class="hero-widget"><div style="font-size:14px; font-weight:700; color:#8E8E93;">{now.strftime("%d.%m.%Y")}</div><div style="font-size:48px; font-weight:800; color:#2D3142;">{int(total_left)} ₪</div><div style="color:#34D399; font-weight:700; font-size:14px;">ОСТАТОК В КОНВЕРТАХ</div></div>', unsafe_allow_html=True)

# 2. ФОРМА ВВОДА
with st.form("add_transaction", clear_on_submit=True):
    st.markdown('<div style="font-size:14px; font-weight:800; color:#8E8E93; text-transform:uppercase; margin-bottom:10px; text-align:center;">Быстрое внесение</div>', unsafe_allow_html=True)
    cat = st.selectbox("Куда тратим?", list(CATEGORIES.keys()))
    amt = st.number_input("Сколько?", min_value=0, step=1, value=None, placeholder="₪")
    if st.form_submit_button("ВНЕСТИ ТРАТУ") and amt:
        requests.post(SHEET_URL, json={"category": cat, "amount": amt})
        st.rerun()

# 3. СЕТКА КОНВЕРТОВ
cols = st.columns(2)
for i, (name, info) in enumerate(CATEGORIES.items()):
    spent = spent_dict.get(name, 0)
    
    # КАРТОЧКА РАБОТЫ (СЧЕТЧИК)
    if info['limit'] == 0:
        card_bg = info['card_bg']
        icon_bg = info['icon_bg']
        html_card = f'<div class="budget-card" style="background-color:{card_bg}; border: 1px solid #CFD8DC;"><div style="width:52px; height:52px; border-radius:50%; background:{icon_bg}; color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:26px; margin-bottom:12px;">{info["icon"]}</div><div class="cat-name">{name}</div><div style="font-size:11px; font-weight:700; color:#8E8E93; margin-bottom:2px;">ТРАТЫ ЗА МЕСЯЦ</div><div class="cat-amount" style="color:#2D3142;">{int(spent)}</div></div>'
    
    # ОБЫЧНЫЕ КОНВЕРТЫ
    else:
        current_val = (info['limit'] * months_passed) - spent
        pct = max(0, min(1, current_val / info['limit'])) if info['limit'] > 0 else 0
        if current_val < 0 or pct <= 0.10:
            card_bg = "#FFEBEB"; icon_bg = "#FF5252"; text_color = "#FF5252"; bar_color = "#FF5252"
        elif pct <= 0.30:
            card_bg = "#FFF8E1"; icon_bg = "#FFB300"; text_color = "#2D3142"; bar_color = "#FFB300"
        else:
            card_bg = info['card_bg']; icon_bg = info['icon_bg']; text_color = "#2D3142"; bar_color = "#34D399"
        
        html_card = f'<div class="budget-card" style="background-color:{card_bg};"><div style="width:52px; height:52px; border-radius:50%; background:{icon_bg}; color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:26px; margin-bottom:12px;">{info["icon"]}</div><div class="cat-name">{name}</div><div class="cat-amount" style="color:{text_color};">{int(current_val)}</div><div style="width:100%; text-align:right; font-size:12px; font-weight:700; color:#8E8E93; opacity:0.6; margin-bottom:4px; letter-spacing:0.5px;">{int(pct*100)}%</div><div class="progress-track"><div class="progress-fill" style="width:{int(pct*100)}%; background-color:{bar_color};"></div></div></div>'
    
    with cols[i % 2]:
        st.markdown(html_card.replace('\n', ''), unsafe_allow_html=True)

# 4. ИСТОРИЯ, ПЛАТЕЖИ, ПЕРЕВОД (без изменений)
if history:
    with st.expander("🕒 ИСТОРИЯ ОПЕРАЦИЙ", expanded=False):
        for item in history:
            st.markdown(f'<div style="display:flex; justify-content:space-between; padding:12px 0; border-bottom:1px solid rgba(0,0,0,0.05); font-size:14px;"><span>{item["date"]} <b>{item["category"]}</b></span><span style="color:#FF3B30; font-weight:700;">-{int(item["amount"])} ₪</span></div>', unsafe_allow_html=True)

with st.expander("🔒 ОБЯЗАТЕЛЬНЫЕ ПЛАТЕЖИ (10 790 ₪)"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.write(f"**{n}**: {v} ₪")

with st.expander("🔄 ПЕРЕВОД МЕЖДУ КОНВЕРТАМИ"):
    with st.form("transfer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1: cat_from = st.selectbox("Откуда забираем?", [k for k in CATEGORIES.keys() if CATEGORIES[k]['limit'] > 0], index=5)
        with col2: cat_to = st.selectbox("Куда добавляем?", [k for k in CATEGORIES.keys() if CATEGORIES[k]['limit'] > 0], index=0)
        transfer_amt = st.number_input("Сумма перевода", min_value=1, step=1, value=None, placeholder="₪")
        if st.form_submit_button("СДЕЛАТЬ ПЕРЕВОД") and transfer_amt:
            if cat_from != cat_to:
                requests.post(SHEET_URL, json={"category": cat_from, "amount": transfer_amt})
                requests.post(SHEET_URL, json={"category": cat_to, "amount": -transfer_amt})
                st.rerun()
