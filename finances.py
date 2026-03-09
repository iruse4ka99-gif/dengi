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

# 2. УЛУЧШЕННЫЙ ДИЗАЙН СО "СВЕТОФОРОМ"
st.markdown("""
    <style>
    header, footer, #MainMenu, [data-testid="stSidebar"] {visibility: hidden !important; display: none !important;}
    .block-container {padding-top: 1rem !important;}
    html, body, [class*="stApp"] { background-color: #ffffff !important; }

    .item-card {
        border-radius: 24px; padding: 20px; margin-bottom: 12px;
        border: 1px solid rgba(0,0,0,0.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .item-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
    .item-name { font-size: 10px; font-weight: 800; color: #8e8e93; text-transform: uppercase; }
    
    /* Линия под цифрой */
    .p-bar-bg { height: 4px; background: rgba(0,0,0,0.05); border-radius: 2px; margin-top: 12px; }
    .p-bar-fill { height: 100%; border-radius: 2px; transition: all 0.5s ease; }
    </style>
    """, unsafe_allow_html=True)

# Функция для определения цвета (Зеленый -> Оранжевый -> Красный)
def get_status_color(pct):
    if pct > 0.5: return "#30d158" # Зеленый
    if pct > 0.15: return "#ff9f0a" # Оранжевый
    return "#ff3b30" # Красный

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

# 4. ГЛАВНЫЙ ЭКРАН
total_left = sum(c['limit'] for c in CATEGORIES.values()) - sum(spent.values())
main_color = get_status_color(total_left / sum(c['limit'] for c in CATEGORIES.values()))

st.markdown(f"""
    <div style="text-align:center; padding: 30px 0;">
        <h1 style="font-size:52px; font-weight:200; margin:0; color:{main_color};">{int(total_left)} ₪</h1>
        <p style="color:#8e8e93; font-weight:800; font-size:11px; margin:0; letter-spacing:1px;">ОСТАТОК В МАРТЕ</p>
    </div>
""", unsafe_allow_html=True)

# СЕТКА КОНВЕРТОВ
cols = st.columns(2)
for i, (name, info) in enumerate(CATEGORIES.items()):
    val = info['limit'] - spent.get(name, 0)
    pct = max(0, min(1, val / info['limit']))
    color = get_status_color(pct)
    
    # Если баланс отрицательный - делаем число красным
    val_color = color if pct < 0.3 else "#1c1c1e"
    if val < 0: val_color = "#ff3b30"

    with cols[i % 2]:
        st.markdown(f"""
            <div class="item-card" style="background-color: {info['color']};">
                <div class="item-header">
                    <span class="item-name">{name}</span>
                    <span>{info['icon']}</span>
                </div>
                <div style="font-size:26px; font-weight:600; color:{val_color};">
                    {int(val)}
                </div>
                <div class="p-bar-bg">
                    <div class="p-bar-fill" style="width: {int(pct*100)}%; background: {color};"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ИСТОРИЯ
if history:
    with st.expander("🕒 ПОСЛЕДНИЕ ТРАТЫ"):
        for item in history:
            st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #f2f2f7; font-size:13px;">
                    <span>{item['date']} <b>{item['category']}</b></span>
                    <span style="color:#ff3b30; font-weight:600;">-{int(item['amount'])} ₪</span>
                </div>
            """, unsafe_allow_html=True)

st.write("---")

# ФОРМА ВВОДА
with st.form("add_transaction", clear_on_submit=True):
    cat = st.selectbox("Что купили?", list(CATEGORIES.keys()))
    amt = st.number_input("Сколько потратили?", min_value=0, step=1, value=None, placeholder="₪")
    if st.form_submit_button("ВНЕСТИ В ТАБЛИЦУ"):
        if amt:
            requests.post(SHEET_URL, json={"category": cat, "amount": amt})
            st.cache_data.clear()
            st.rerun()

# ФИКСИРОВАННЫЕ ВНИЗУ
with st.expander("🔒 Обязательные платежи (10 790 ₪)"):
    fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}
    for n, v in fixed.items():
        st.write(f"**{n}**: {v} ₪")
