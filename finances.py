import streamlit as st
import datetime
import requests

# Твоя ссылка (Проверена)
SHEET_URL = "https://script.google.com/macros/s/AKfycbyAGMqKyFvKhWWVy2taQr-i5dqfvdif3sFr6elhini9USrk1NqqA7y9weIcGhIKuhim/exec"

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# СТИЛИ (Чистый белый интерфейс)
st.markdown("""
    <style>
    html, body, [class*="stApp"] { background-color: #ffffff !important; color: #1a1a1a !important; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}
    /* Поля ввода */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #f8f9fa !important; border: 1px solid #e0e0e0 !important; border-radius: 12px !important;
    }
    input { color: #1a1a1a !important; }
    /* Кнопка */
    .stButton>button {
        background-color: #30d158 !important; color: white !important; border-radius: 12px !important;
        height: 48px; width: 100%; font-weight: 600; border: none !important;
    }
    .fixed-box { background: #fdfdfd; border-radius: 20px; padding: 25px; border: 1px solid #f0f0f0; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f0f0f0; font-size: 13px; color: #666; }
    </style>
    """, unsafe_allow_html=True)

# ГЛАВНЫЕ ДАННЫЕ (Лимиты)
LIMITS = {
    "Продукты": 4000, "Доп. уроки": 2254, "Машина": 500, 
    "Одежда": 200, "Арина": 100, "Натан": 100, "Разное": 556
}

# ИНИЦИАЛИЗАЦИЯ (Память сессии)
if 'db' not in st.session_state:
    st.session_state.db = {name: {"b": val, "h": []} for name, val in LIMITS.items()}
    st.session_state.fixed = {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350}

now = datetime.datetime.now()
st.markdown(f'<div style="text-align:center; padding-top:10px; font-size:16px; font-weight:400; color:#999;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3.5, 1])

with main_c:
    # РАСЧЕТ ОБЩЕГО ОСТАТКА
    total_left = sum(v['b'] for v in st.session_state.db.values())
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

    # КАРТОЧКИ КАТЕГОРИЙ
    envs_list = list(st.session_state.db.items())
    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            with cols[j]:
                if idx < len(envs_list):
                    name, d = envs_list[idx]
                    limit = LIMITS[name]
                    money_left_pct = d['b'] / limit if limit > 0 else 0
                    color = "#30d158" if money_left_pct > 0.3 else "#ff9f0a"
                    st.markdown(f"""
                    <div style="background-color: #fdfdfd; border-radius: 20px; padding: 20px; border: 1px solid #f0f0f0; margin-bottom: 15px; text-align: center;">
                        <div style="color: #999; font-size: 10px; text-transform: uppercase;">{name}</div>
                        <div style="color: #1a1a1a; font-size: 26px; font-weight: 400;">{int(d['b'])}</div>
                        <div style="color: {color}; font-size: 11px; font-weight: 600;">{int(money_left_pct*100)}%</div>
                    </div>
                    """, unsafe_allow_html=True)

with side_c:
    st.markdown('<div class="fixed-box">', unsafe_allow_html=True)
    st.write("🔒 **ФИКСИРОВАНО**")
    for n, v in st.session_state.fixed.items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# ФОРМА ВВОДА (Очищается сама)
with st.form("my_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        category = st.selectbox("Категория", list(LIMITS.keys()), label_visibility="collapsed")
    with c2:
        # value=0 здесь НЕ БУДЕТ мешать, так как clear_on_submit очистит поле
        amount = st.number_input("Сумма", min_value=0, step=1, value=None, placeholder="Сумма", label_visibility="collapsed")
    with c3:
        submitted = st.form_submit_button("ВНЕСТИ ТРАТУ")
        if submitted and amount:
            # 1. Считаем остаток
            st.session_state.db[category]['b'] -= amount
            
            # 2. Отправляем в Google
            try:
                payload = f"Дата: {now.strftime('%d.%m %H:%M')}, {category}: -{amount} ₪"
                requests.post(SHEET_URL, data=payload, timeout=5)
                st.toast(f"Добавлено: {amount} ₪", icon="✅")
            except:
                st.toast("Ошибка связи с таблицей", icon="⚠️")
            
            st.rerun()
