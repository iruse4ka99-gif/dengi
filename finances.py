import streamlit as st
import datetime
import requests

# Твоя актуальная ссылка на Google Script (уже вставлена)
SHEET_URL = "https://script.google.com/macros/s/AKfycbyAGMqKyFvKhWWVy2taQr-i5dqfvdif3sFr6elhini9USrk1NqqA7y9weIcGhIKuhim/exec"

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# СВЕТЛАЯ ТЕМА (Настройка внешнего вида)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="stApp"] { 
        background-color: #ffffff !important; 
        color: #1a1a1a !important; 
        font-family: 'Inter', sans-serif; 
    }
    header, footer {visibility: hidden;}

    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #f8f9fa !important;
        border: 1px solid #e0e0e0 !important;
        color: #1a1a1a !important;
        border-radius: 12px !important;
    }
    
    .stButton>button {
        background-color: #30d158 !important; 
        color: white !important;
        border: none !important; 
        border-radius: 12px !important;
        height: 48px; width: 100%; 
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(48, 209, 88, 0.2);
    }

    .fixed-box { 
        background: #fdfdfd; 
        border-radius: 20px; 
        padding: 25px; 
        border: 1px solid #f0f0f0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .fixed-row { 
        display: flex; 
        justify-content: space-between; 
        padding: 10px 0; 
        border-bottom: 1px solid #f0f0f0; 
        font-size: 13px; 
        color: #666; 
    }
    </style>
    """, unsafe_allow_html=True)

# ИНИЦИАЛИЗАЦИЯ ДАННЫХ
if 'db' not in st.session_state:
    st.session_state.db = {
        "income": 18500,
        "fixed": {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350},
        "envs": {
            "Продукты": {"b": 4000, "l": 4000, "h": []},
            "Доп. уроки": {"b": 2254, "l": 2254, "h": []},
            "Машина": {"b": 500, "l": 500, "h": []},
            "Одежда": {"b": 200, "l": 200, "h": []},
            "Арина": {"b": 100, "l": 100, "h": []},
            "Натан": {"b": 100, "l": 100, "h": []},
            "Разное": {"b": 556, "l": 556, "h": []}
        }
    }

now = datetime.datetime.now()
st.markdown(f'<div style="text-align:center; padding-top:10px; font-size:16px; font-weight:400; letter-spacing:4px; color:#999;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3.5, 1])

with main_c:
    total_left = sum(v['b'] for v in st.session_state.db['envs'].values())
    total_limit = sum(v['l'] for v in st.session_state.db['envs'].values())
    pct = int((total_left / total_limit) * 100) if total_limit > 0 else 0
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding: 30px 0;">
            <div style="width:160px; height:160px; border-radius:50%; background:radial-gradient(closest-side, white 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #f0f0f0 0); display:flex; align-items:center; justify-content:center; box-shadow: 0 10px 20px rgba(0,0,0,0.05);">
                <div style="text-align:center;">
                    <span style="font-size:34px; font-weight:300; color:#1a1a1a;">{int(total_left)} ₪</span><br>
                    <span style="font-size:10px;color:#30d158;font-weight:700;letter-spacing:2px;">ОСТАТОК</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    envs = list(st.session_state.db['envs'].items())
    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            with cols[j]:
                if idx < 7:
                    name, d = envs[idx]
                    money_left_pct = d['b'] / d['l'] if d['l'] > 0 else 0
                    color = "#30d158" if money_left_pct > 0.3 else "#ff9f0a"
                    history_text = " | ".join(d["h"][:2]) if d["h"] else "Трат пока нет"
                    
                    st.markdown(f"""
                    <div style="background-color: #fdfdfd; border-radius: 20px; padding: 20px; border: 1px solid #f0f0f0; margin-bottom: 15px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.02);">
                        <div style="color: #999; font-size: 10px; text-transform: uppercase;">{name}</div>
                        <div style="color: #1a1a1a; font-size: 28px; font-weight: 400;">{int(d['b'])}</div>
                        <div style="color: {color}; font-size: 11px; font-weight: 600;">{int(money_left_pct*100)}%</div>
                        <div style="margin-top: 10px; color: #bbb; font-size: 10px;">{history_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif idx == 7:
                    days_to_go = 31 - now.day
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; border-radius: 20px; padding: 20px; text-align: center; border: 1px dashed #e0e0e0;">
                        <div style="color: #999; font-size: 10px; text-transform: uppercase;">Дней до 1-го</div>
                        <div style="color: #1a1a1a; font-size: 28px; font-weight: 300;">{days_to_go}</div>
                    </div>
                    """, unsafe_allow_html=True)

with side_c:
    st.markdown('<div class="fixed-box">', unsafe_allow_html=True)
    st.write("🔒 **ФИКСИРОВАНО**")
    for n, v in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span style="color:#1a1a1a; font-weight:500;">{v} ₪</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; margin-top:30px;"><div style="color:#ff3b30; font-size:12px; font-weight:600;">{now.strftime("%B").upper()}</div><div style="font-size:50px; font-weight:200; color:#1a1a1a;">{now.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# ФОРМА ЗАПИСИ
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat = st.selectbox("", list(st.session_state.db['envs'].keys()), label_visibility="collapsed")
    with c2: val = st.number_input("", min_value=0, step=1, value=0, key="val_input", label_visibility="collapsed")
    with c3:
        if st.form_submit_button("ВНЕСТИ ТРАТУ"):
            if val > 0:
                st.session_state.db['envs'][cat]['b'] -= val
                st.session_state.db['envs'][cat]['h'].insert(0, f"-{val}₪")
                
                # ОТПРАВКА В GOOGLE
                try:
                    payload = f"Дата: {now.strftime('%d.%m %H:%M')}, Категория: {cat}, Сумма: {val}"
                    requests.post(SHEET_URL, data=payload)
                    st.toast("Синхронизировано с таблицей!", icon="✅")
                except:
                    st.error("Ошибка связи")
                
                st.rerun()
