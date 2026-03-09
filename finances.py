import streamlit as st
import datetime

# Твоя база данных
SHEET_URL = "https://script.google.com/macros/s/AKfycbyOHizCE2-_pjAbPhlImMW_KbTQmHDX4zheunapHU_WOFgn3qFS0PYbOC-7ed1QYUw3/exec"

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ЖЕСТКИЙ ФИКС ДЛЯ iPAD/SAFARI (Абсолютная темнота)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    html, body, [class*="stApp"] { background-color: #000000 !important; color: #ffffff !important; font-family: 'Inter', sans-serif; }
    header, footer {visibility: hidden;}

    /* Жесткое подавление белых стилей Apple/iOS */
    input, select, textarea, div[data-baseweb="input"], div[data-baseweb="select"] > div {
        -webkit-appearance: none !important;
        background-color: #0a0a0a !important;
        border: 1px solid #222 !important;
        color: #ffffff !important;
        border-radius: 12px !important;
    }
    
    /* Кнопка записи */
    .stButton>button {
        -webkit-appearance: none !important;
        background-color: #111 !important; color: #30d158 !important;
        border: 1px solid rgba(48, 209, 88, 0.3) !important; border-radius: 12px !important;
        height: 48px; width: 100%; font-weight: 500;
    }

    .fixed-box { background: #050505; border-radius: 20px; padding: 25px; border: 1px solid #111; }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #0a0a0a; font-size: 13px; color: #555; }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ
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
day_of_month = now.day
month_progress = day_of_month / 30.0

st.markdown(f'<div style="text-align:center; padding-top:10px; font-size:16px; font-weight:400; letter-spacing:4px; color:#666;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3.5, 1])

with main_c:
    total_left = sum(v['b'] for v in st.session_state.db['envs'].values())
    total_limit = sum(v['l'] for v in st.session_state.db['envs'].values())
    pct = int((total_left / total_limit) * 100) if total_limit > 0 else 0
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding: 30px 0;">
            <div style="width:160px; height:160px; border-radius:50%; background:radial-gradient(closest-side, black 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #111 0); display:flex; align-items:center; justify-content:center;">
                <div style="text-align:center;">
                    <span style="font-size:34px; font-weight:300;">{int(total_left)} ₪</span><br>
                    <span style="font-size:10px;color:#30d158;opacity:0.6;letter-spacing:2px;">ОСТАТОК</span>
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
                    is_warning = money_left_pct < (1 - month_progress)
                    color = "#ff453a" if is_warning else ("#30d158" if money_left_pct > 0.3 else "#ff9f0a")
                    history_text = " | ".join(d["h"][:2]) if d["h"] else "Трат пока нет"
                    
                    html_card = f"""
                    <div style="background-color: #0c0c0e; border-radius: 20px; padding: 20px; border-top: 2px solid {color}; margin-bottom: 15px; text-align: center;">
                        <div style="color: #666; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;">{name}</div>
                        <div style="color: #fff; font-size: 30px; font-weight: 300;">{int(d['b'])}</div>
                        <div style="color: {color}; font-size: 10px; font-weight: 600; margin-top: 4px;">{int(money_left_pct*100)}% от {int(d['l'])}</div>
                        <div style="margin-top: 15px; border-top: 1px solid #1a1a1a; padding-top: 10px; color: #444; font-size: 10px;">
                            {history_text}
                        </div>
                    </div>
                    """
                    st.markdown(html_card, unsafe_allow_html=True)
                
                elif idx == 7:
                    days_to_go = 31 - now.day
                    html_card_days = f"""
                    <div style="background-color: transparent; border-radius: 20px; padding: 20px; margin-bottom: 15px; text-align: center; border: 1px dashed #222;">
                        <div style="color: #444; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;">Дней до 1-го</div>
                        <div style="color: #666; font-size: 30px; font-weight: 300;">{days_to_go}</div>
                    </div>
                    """
                    st.markdown(html_card_days, unsafe_allow_html=True)

with side_c:
    st.markdown('<div class="fixed-box">', unsafe_allow_html=True)
    st.write("🔒 **ФИКСИРОВАНО**")
    for n, v in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; margin-top:40px;"><div style="color:#ff3b30; font-size:12px; letter-spacing:2px;">{now.strftime("%B").upper()}</div><div style="font-size:56px; font-weight:200; color:#fff;">{now.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat = st.selectbox("", list(st.session_state.db['envs'].keys()), label_visibility="collapsed")
    with c2: val = st.number_input("", min_value=0, step=1, value=0, label_visibility="collapsed")
    with c3:
        if st.form_submit_button("ВНЕСТИ ТРАТУ (СИНХР.)"):
            if val > 0:
                st.session_state.db['envs'][cat]['b'] -= val
                st.session_state.db['envs'][cat]['h'].insert(0, f"-{val}₪")
                st.rerun()

with st.expander("⚙️ НАСТРОЙКИ СУММ"):
    for k in st.session_state.db['fixed']:
        st.session_state.db['fixed'][k] = st.number_input(f"{k}", value=st.session_state.db['fixed'][k], key=f"set_{k}")
    if st.button("Сохранить"): st.rerun()
