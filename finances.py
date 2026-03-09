import streamlit as st
import datetime
import requests

# ТВОЯ ССЫЛКА ИЗ GOOGLE (не меняй её, если она рабочая)
SHEET_URL = "https://script.google.com/macros/s/AKfycbxkvxn-l1zlwpsXV7EsiuOr1xoFQCThBk6KFbeaIUzD7reCD2zoLMo2hdbpKmizEWxf/exec"

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# 1. СТИЛИ
st.markdown("""
    <style>
    html, body, [class*="stApp"] { background-color: #ffffff !important; color: #1a1a1a !important; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #f8f9fa !important; border: 1px solid #e0e0e0 !important; border-radius: 12px !important;
    }
    .stButton>button {
        background-color: #30d158 !important; color: white !important; border-radius: 12px !important;
        height: 48px; width: 100%; font-weight: 600; border: none !important;
    }
    .fixed-box { background: #fdfdfd; border-radius: 20px; padding: 25px; border: 1px solid #f0f0f0; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f0f0f0; font-size: 13px; color: #666; }
    </style>
    """, unsafe_allow_html=True)

# 2. ГЛАВНЫЕ ДАННЫЕ (Ежедневные конверты)
# Я добавила Лео и обновила список категорий
LIMITS = {
    "Продукты": 4000, 
    "Машина": 500, 
    "Одежда": 200, 
    "Арина": 100, 
    "Натан": 100, 
    "Лео": 600,          # Новый конверт для памперсов и питания
    "Доп. уроки": 2254, 
    "Разное": 556         # Сюда вносим стул и прочее
}

# 3. ЗАГРУЗКА ДАННЫХ ИЗ GOOGLE
@st.cache_data(ttl=5)
def get_spent_amounts():
    try:
        response = requests.get(SHEET_URL, timeout=5)
        return response.json() if response.status_code == 200 else {}
    except:
        return {}

spent_db = get_spent_amounts()

# 4. РАСЧЕТ ОСТАТКОВ
current_balances = {name: (limit - spent_db.get(name, 0)) for name, limit in LIMITS.items()}

# 5. ИНТЕРФЕЙС
# Фиксированные траты (они живут отдельно и не вычитаются из круга)
st.session_state.fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}

now = datetime.datetime.now()
st.markdown(f'<div style="text-align:center; padding-top:10px; font-size:16px; color:#999;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3.5, 1])

with main_c:
    # ОБЩИЙ КРУГ ОСТАТКА (только для конвертов)
    total_left = sum(current_balances.values())
    total_limit = sum(LIMITS.values())
    pct = int((total_left / total_limit) * 100) if total_limit > 0 else 0
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding: 30px 0;">
            <div style="width:160px; height:160px; border-radius:50%; background:radial-gradient(closest-side, white 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #f0f0f0 0); display:flex; align-items:center; justify-content:center; box-shadow: 0 10px 20px rgba(0,0,0,0.05);">
                <div style="text-align:center;">
                    <span style="font-size:34px; font-weight:300; color:#1a1a1a;">{int(total_left)} ₪</span><br>
                    <span style="font-size:10px;color:#30d158;font-weight:700;">ОСТАТОК</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # КАРТОЧКИ КАТЕГОРИЙ (теперь их 8)
    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx < len(current_balances):
                name = list(current_balances.keys())[idx]
                balance = current_balances[name]
                limit = LIMITS[name]
                pct_left = balance / limit if limit > 0 else 0
                color = "#30d158" if pct_left > 0.3 else "#ff9f0a"
                with cols[j]:
                    st.markdown(f"""
                    <div style="background-color: #fdfdfd; border-radius: 20px; padding: 15px; border: 1px solid #f0f0f0; margin-bottom: 10px; text-align: center;">
                        <div style="color: #999; font-size: 9px; text-transform: uppercase;">{name}</div>
                        <div style="color: #1a1a1a; font-size: 22px; font-weight: 400;">{int(balance)}</div>
                    </div>
                    """, unsafe_allow_html=True)

with side_c:
    st.markdown('<div class="fixed-box">', unsafe_allow_html=True)
    st.write("🔒 **ФИКСИРОВАНО**")
    for n, v in st.session_state.fixed.items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# ФОРМА ВВОДА
with st.form("my_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        category = st.selectbox("Категория", list(LIMITS.keys()), label_visibility="collapsed")
    with c2:
        amount = st.number_input("Сумма", min_value=0, step=1, value=None, placeholder="Сумма", label_visibility="collapsed")
    with c3:
        if st.form_submit_button("ВНЕСТИ ТРАТУ") and amount:
            try:
                requests.post(SHEET_URL, json={"category": category, "amount": amount}, timeout=5)
                st.toast(f"Добавлено в {category}: {amount} ₪", icon="✅")
                st.cache_data.clear()
                st.rerun()
            except:
                st.toast("Ошибка связи", icon="⚠️")
