import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ГЛУБОКИЙ APPLE BLACK ДИЗАЙН (ЧИСТЫЙ PYTHON)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    html, body, [class*="stApp"] { background-color: #000000 !important; color: #ffffff !important; font-family: 'Inter', sans-serif; }

    header, footer {visibility: hidden;}

    /* Поля ввода: полное слияние с фоном */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #080808 !important; border: 1px solid #1a1a1a !important; border-radius: 14px !important;
    }
    input { color: #ffffff !important; font-size: 16px !important; }

    /* Конверты с мягким свечением и анимацией */
    .apple-card {
        background: rgba(25, 25, 25, 0.4); backdrop-filter: blur(10px);
        border-radius: 24px; padding: 22px; text-align: center;
        border-top: 3px solid var(--status); margin-bottom: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .apple-card:hover { transform: translateY(-3px); box-shadow: 0 15px 35px rgba(0,0,0,0.8); }
    
    .card-title { font-size: 10px; color: #666; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; }
    .card-val { font-size: 32px; font-weight: 300; color: #fff; margin: 2px 0; }
    .card-pct { font-size: 11px; color: var(--status); font-weight: 600; letter-spacing: 0.5px; }

    /* Кнопка записи */
    .stButton>button {
        background: #0a0a0a !important; color: #30d158 !important;
        border: 1px solid rgba(48, 209, 88, 0.2) !important; border-radius: 14px !important;
        height: 48px; width: 100%; transition: 0.3s; font-weight: 500; font-size: 14px !important;
    }
    .stButton>button:hover { border-color: #30d158 !important; background: rgba(48, 209, 88, 0.05) !important; }

    .fixed-box { background: #050505; border-radius: 24px; padding: 25px; border: 1px solid #111; }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #0a0a0a; font-size: 13px; color: #444; }
    
    /* Скрываем рамки кнопок для названий конвертов */
    button[title="History"] { background: transparent !important; border: none !important; color: #555 !important; }
    </style>
    """, unsafe_allow_html=True)

# ЛОГИКА И ДАННЫЕ
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
days_in_month = 30 
month_progress = day_of_month / days_in_month

st.markdown(f'<div style="text-align:center; padding-top:10px; font-size:18px; font-weight:400; letter-spacing:4px; color:#555;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3.5, 1])

with main_c:
    # ГЛАВНЫЙ КРУГ
    total_left = sum(v['b'] for v in st.session_state.db['envs'].values())
    total_limit = sum(v['l'] for v in st.session_state.db['envs'].values())
    pct = int((total_left / total_limit) * 100) if total_limit > 0 else 0
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding: 30px 0;">
            <div style="width:170px; height:170px; border-radius:50%; background:radial-gradient(closest-side, black 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #111 0); display:flex; align-items:center; justify-content:center; border: 1px solid #1a1a1a;">
                <div style="text-align:center;">
                    <span style="font-size:36px; font-weight:300;">{int(total_left)} ₪</span><br>
                    <span style="font-size:10px;color:#30d158;opacity:0.6;letter-spacing:2px;">ОСТАТОК</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # СЕТКА КОНВЕРТОВ (Умный прогноз включен)
    envs = list(st.session_state.db['envs'].items())
    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            with cols[j]:
                if idx < 7:
                    name, d = envs[idx]
                    money_left_pct = d['b'] / d['l'] if d['l'] > 0 else 0
                    
                    # Умный прогноз: подсвечиваем красным, если траты идут слишком быстро
                    is_warning = money_left_pct < (1 - month_progress)
                    color = "#ff453a" if is_warning else ("#30d158" if money_left_pct > 0.3 else "#ff9f0a")
                    
                    if st.button(name.upper(), key=f"btn_{name}", help="Нажми, чтобы увидеть историю"):
                        st.session_state.active = name if st.session_state.get('active') != name else None
                        
                    st.markdown(f"""
                        <div class="apple-card" style="--status:{color}">
                            <div class="card-val">{int(d["b"])}</div>
                            <div class="card-pct">{int(money_left_pct*100)}% от {int(d["l"])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.session_state.get('active') == name:
                        st.markdown(f'<div style="font-size:11px; color:#666; padding-top:8px; text-align:center;">{" | ".join(d["h"][:2]) if d["h"] else "Пока нет трат"}</div>', unsafe_allow_html=True)
                
                elif idx == 7:
                    days_to_go = 31 - now.day
                    st.markdown(f"""
                        <div style="margin-top:42px;">
                            <div class="apple-card" style="--status:#222; opacity:0.4;">
                                <div class="card-val" style="color:#666;">{days_to_go}</div>
                                <div style="font-size:10px; color:#444; margin-top:5px; letter-spacing:1px;">ДНЕЙ ДО 1-ГО</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

with side_c:
    st.markdown('<div class="fixed-box">', unsafe_allow_html=True)
    st.write("🔒 **ФИКСИРОВАНО**")
    for n, v in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; margin-top:40px;"><div style="color:#ff3b30; font-size:12px; letter-spacing:2px;">{now.strftime("%B").upper()}</div><div style="font-size:56px; font-weight:200;">{now.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ПАНЕЛЬ ВВОДА (Максимально чистая)
st.write("---")
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat = st.selectbox("", list(st.session_state.db['envs'].keys()), label_visibility="collapsed")
    with c2: val = st.number_input("", min_value=0, step=1, value=0, label_visibility="collapsed")
    with c3:
        if st.form_submit_button("ВНЕСТИ ТРАТУ"):
            if val > 0:
                st.session_state.db['envs'][cat]['b'] -= val
                st.session_state.db['envs'][cat]['h'].insert(0, f"-{val}")
                st.rerun()

# НАСТРОЙКИ СПРЯТАНЫ ВНИЗУ
with st.expander("⚙️ НАСТРОЙКИ СУММ"):
    for k in st.session_state.db['fixed']:
        st.session_state.db['fixed'][k] = st.number_input(f"{k}", value=st.session_state.db['fixed'][k], key=f"set_{k}")
    if st.button("Сохранить"): st.rerun()
