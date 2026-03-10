import streamlit as st
import datetime
import requests

# ТВОЯ АКТИВНАЯ ССЫЛКА
SHEET_URL = "https://script.google.com/macros/s/AKfycbyrvgESsKjWIaw0gVohS3reEOV_kvinEoEQpbC09Fnihq-fn88FigvDJWdW8tGa2TmA/exec"

st.set_page_config(page_title="Выход в Ноль", layout="centered")

# 1. ТВОИ КОНВЕРТЫ 
CATEGORIES = {
    "Продукты": {"limit": 4000, "icon": "🛒", "bg": "#FFCC80", "color": "#F5A623"}, 
    "Машина": {"limit": 500, "icon": "🚗", "bg": "#81D4FA", "color": "#38BDF8"}, 
    "Лео": {"limit": 300, "icon": "🍼", "bg": "#A5D6A7", "color": "#34D399"}, 
    "Арина": {"limit": 100, "icon": "👧", "bg": "#CE93D8", "color": "#A78BFA"}, 
    "Натан": {"limit": 100, "icon": "👦", "bg": "#90CAF9", "color": "#38BDF8"}, 
    "Доп. уроки": {"limit": 2254, "icon": "📚", "bg": "#FFF176", "color": "#FBBF24"}, 
    "Одежда": {"limit": 200, "icon": "👕", "bg": "#F48FB1", "color": "#E879F9"}, 
    "Разное": {"limit": 256, "icon": "📦", "bg": "#EF9A9A", "color": "#FB7185"} 
}

st.markdown("""
    <style>
    header, footer, #MainMenu, [data-testid="stSidebar"] {visibility: hidden !important; display: none !important;}
    html, body, [class*="stApp"] { background-color: #F2F2F7 !important; }
    
    .hero-widget { background: #FFFFFF; border-radius: 24px; padding: 25px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.06); margin-bottom: 15px; }
    
    [data-testid="stForm"] { background: #FFFFFF; border-radius: 20px; padding: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.04); border: 1px solid #E5E5EA; margin-bottom: 20px;}
    
    .budget-card { background: #FFFFFF; border-radius: 20px; padding: 18px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #E5E5EA; display: flex; flex-direction: column; align-items: center; position: relative;}
    
    .cat-name { color: #8E8E93; font-size: 13px; font-weight: 800; text-transform: uppercase; margin-bottom: 6px; }
    .cat-amount { color: #2D3142; font-size: 28px; font-weight: 800; margin-bottom: 8px; }
    
    /* Стили для полоски прогресса */
    .progress-track { width: 100%; height: 6px; background: #E5E5EA; border-radius: 3px; }
    .progress-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease, background-color 0.3s ease; }
    
    /* Стили для аккуратных процентов */
    .percent-text { width: 100%; text-align: right; font-size: 11px; font-weight: 700; color: #8E8E93; opacity: 0.6; margin-bottom: 4px; letter-spacing: 0.5px; }
    
    .stButton>button { background: #2D3142 !important; color: white !important; border-radius: 18px !important; height: 55px; font-size: 16px; font-weight: 700; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# ЛОГИКА СВЕТОФОРА
def get_traffic_light_color(pct):
    if pct > 0.4: return "#34D399" 
    if pct > 0.15: return "#FF9F0A" 
    return "#FF3B30" 

@st.cache_data(ttl=0)
def load_data():
    try:
        r = requests.get(SHEET_URL, timeout=10)
        return r.json()
    except: return {"spent": {}, "history": []}

data = load_data()
spent_dict = data.get("spent", {})
history = data.get("history", [])

total_spent = sum(spent_dict.values())
total_limit = sum(c['limit'] for c in CATEGORIES.values())
total_left = total_limit - total_spent

# 1. ГЛАВНЫЙ ВИДЖЕТ
st.markdown(f'<div class="hero-widget"><div style="font-size:14px; font-weight:700; color:#8E8E93;">{datetime.datetime.now().strftime("%d.%m.%Y")}</div><div style="font-size:48px; font-weight:800; color:#2D3142;">{int(total_left)} ₪</div><div style="color:#34D399; font-weight:700; font-size:14px;">ОСТАТОК В КОНВЕРТАХ</div></div>', unsafe_allow_html=True)

# 2. ФОРМА ВВОДА (НАВЕРХУ)
with st.form("add_transaction", clear_on_submit=True):
    st.markdown('<div style="font-size:14px; font-weight:800; color:#8E8E93; text-transform:uppercase; margin-bottom:10px; text-align:center;">Быстрое внесение</div>', unsafe_allow_html=True)
    cat = st.selectbox("Куда тратим?", list(CATEGORIES.keys()))
    amt = st.number_input("Сколько?", min_value=0, step=1, value=None, placeholder="₪")
    if st.form_submit_button("ВНЕСТИ ТРАТУ") and amt:
        requests.post(SHEET_URL, json={"category": cat, "amount": amt})
        st.cache_data.clear()
        st.rerun()

# 3. СЕТКА КОНВЕРТОВ С ПРОЦЕНТАМИ
cols = st.columns(2)
for i, (name, info) in enumerate(CATEGORIES.items()):
    spent = spent_dict.get(name, 0)
    current_val = info['limit'] - spent
    pct = max(0, min(1, current_val / info['limit'])) if info['limit'] > 0 else 0
    
    bar_color = get_traffic_light_color(pct)
    text_color = "#FF3B30" if current_val < 0 else "#2D3142"
    
    with cols[i % 2]:
        st.markdown(f"""
            <div class="budget-card">
                <div style="width:52px; height:52px; border-radius:50%; background:{info['bg']}; display:flex; align-items:center; justify-content:center; font-size:26px; margin-bottom:12px;">{info['icon']}</div>
                <div class="cat-name">{name}</div>
                <div class="cat-amount" style="color:{text_color};">{int(current_val)}</div>
                
                <div class="percent-text">{int(pct*100)}%</div>
                
                <div class="progress-track"><div class="progress-fill" style="width:{int(pct*100)}%; background-color:{bar_color};"></div></div>
            </div>
        """, unsafe_allow_html=True)

# 4. ИСТОРИЯ
if history:
    with st.expander("🕒 ИСТОРИЯ ОПЕРАЦИЙ", expanded=False):
        for item in history:
            st.markdown(f'<div style="display:flex; justify-content:space-between; padding:12px 0; border-bottom:1px solid #E5E5EA; font-size:14px;"><span>{item["date"]} <b>{item["category"]}</b></span><span style="color:#FF3B30; font-weight:700;">-{int(item["amount"])} ₪</span></div>', unsafe_allow_html=True)

st.write("---")

# 5. ФИКСИРОВАННЫЕ ВНИЗУ
with st.expander("🔒 ОБЯЗАТЕЛЬНЫЕ ПЛАТЕЖИ (10 790 ₪)"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.write(f"**{n}**: {v} ₪")
