import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# УЛЬТРА-ЧЕРНЫЙ APPLE (БЕЗ БЕЛЫХ ПЯТЕН)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');
    
    html, body, [class*="stApp"], [data-testid="stAppViewContainer"] { 
        background-color: #000000 !important; 
        color: #ffffff !important; 
    }

    /* Убираем белые рамки и фон полей */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #050505 !important; 
        border: 1px solid #1a1a1a !important;
    }
    input { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    
    /* Конверты */
    .apple-card {
        background: rgba(28, 28, 30, 0.4); backdrop-filter: blur(20px);
        border-radius: 24px; padding: 20px; text-align: center;
        border-top: 3px solid var(--status); margin-bottom: 10px;
    }
    .card-title { font-size: 10px; color: #444; text-transform: uppercase; letter-spacing: 1.5px; }
    .card-val { font-size: 26px; font-weight: 500; margin: 5px 0; }
    .card-pct { font-size: 11px; color: var(--status); font-weight: 600; }
    .card-limit { font-size: 9px; color: #222; }

    /* Боковая панель */
    .fixed-panel { padding: 20px; border-left: 1px solid #111; }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #080808; font-size: 12px; color: #333; }
    
    /* Кнопки */
    .stButton>button { background: transparent !important; border: 1px solid #111 !important; color: #222 !important; border-radius: 10px; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# ИНИЦИАЛИЗАЦИЯ ДАННЫХ (18 500 ₪)
if 'db' not in st.session_state:
    st.session_state.db = {
        "income": 18500,
        "fixed": {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1400, "Здоровье": 350},
        "envs": {
            "Продукты": {"b": 4000, "l": 4000}, # Вернули 4000
            "Доп. уроки": {"b": 1850, "l": 1850},
            "Машина": {"b": 1000, "l": 1000},
            "Одежда": {"b": 200, "l": 200}, # Уменьшили, чтобы влезла еда
            "Арина": {"b": 100, "l": 100},
            "Натан": {"b": 100, "l": 100},
            "Красота": {"b": 200, "l": 200},
            "Разное": {"b": 60, "l": 60}
        }
    }

now = datetime.datetime.now()
st.markdown(f'<div style="text-align:center; padding:15px 0; font-size:18px; letter-spacing:3px; font-weight:300; color:#555;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

main_col, side_col = st.columns([3.5, 1])

with main_col:
    # КРУГ (Остаток от 7,510)
    current_money = sum(v['b'] for v in st.session_state.db['envs'].values())
    pct = int((current_money / 7510) * 100) if current_money > 0 else 0
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding-bottom: 25px;">
            <div style="width:130px; height:130px; border-radius:50%; background:radial-gradient(closest-side, black 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #111 0); display:flex; align-items:center; justify-content:center;">
                <div style="text-align:center;"><span style="font-size:24px; font-weight:300;">{int(current_money)} ₪</span><br><span style="font-size:10px;color:#30d158;opacity:0.5;">{pct}%</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # КОНВЕРТЫ
    envs_list = list(st.session_state.db['envs'].items())
    for i in range(0, len(envs_list), 4):
        cols = st.columns(4)
        for j, (name, d) in enumerate(envs_list[i:i+4]):
            usage = int((d['b'] / d['l']) * 100) if d['l'] > 0 else 0
            color = "#30d158" if usage > 50 else ("#ff9f0a" if usage > 20 else "#ff453a")
            with cols[j]:
                st.markdown(f"""
                    <div class="apple-card" style="--status:{color}">
                        <div class="card-title">{name}</div>
                        <div class="card-val">{int(d["b"])} ₪</div>
                        <div class="card-pct">{usage}%</div>
                        <div class="card-limit">из {int(d["l"])}</div>
                    </div>
                """, unsafe_allow_html=True)

with side_col:
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    st.write("🔒 **FIXED**")
    for n, v in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; margin-top:40px;"><div style="color:#ff3b30; font-size:11px;">{now.strftime("%A").upper()}</div><div style="font-size:45px;">{now.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ВВОД
st.write("---")
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat = st.selectbox("", list(st.session_state.db['envs'].keys()), label_visibility="collapsed")
    with c2: val = st.number_input("", min_value=0, step=1, value=0, label_visibility="collapsed")
    with c3:
        if st.form_submit_button("ADD", use_container_width=True):
            if val > 0:
                st.session_state.db['envs'][cat]['b'] -= val
                st.rerun()

# НАСТРОЙКИ
with st.expander("Settings"):
    if st.button("🚀 START NEW MONTH"):
        for k in st.session_state.db['envs']: st.session_state.db['envs'][k]['b'] = st.session_state.db['envs'][k]['l']
        st.rerun()
