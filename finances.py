import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# УЛЬТРА-ЧЕРНЫЙ ДИЗАЙН (ФИКСАЦИЯ ЦВЕТА)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');
    
    /* Базовый черный фон везде */
    html, body, [class*="stApp"], [data-testid="stAppViewContainer"] { 
        background-color: #000000 !important; 
        font-family: 'Inter', sans-serif; 
        color: #ffffff !important; 
    }

    /* ПРИНУДИТЕЛЬНОЕ ЗАТЕМНЕНИЕ ПОЛЕЙ ВВОДА (убираем белое) */
    div[data-baseweb="select"], div[data-baseweb="input"], [data-testid="stWidgetLabel"] {
        background-color: #000000 !important;
    }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #0a0a0a !important;
        border: 1px solid #1a1a1a !important;
        color: #ffffff !important;
        border-radius: 12px !important;
    }
    input { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    
    /* Убираем белую рамку вокруг активного поля */
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
        border-color: #333333 !important;
    }

    /* Карточки конвертов */
    .apple-card {
        background: rgba(28, 28, 30, 0.4); backdrop-filter: blur(20px);
        border-radius: 24px; padding: 20px; text-align: center;
        border-top: 3px solid var(--status); margin-bottom: 10px;
    }
    .card-title { font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 2px; }
    .card-val { font-size: 28px; font-weight: 500; margin: 5px 0; }
    .card-pct { font-size: 11px; color: var(--status); font-weight: 600; }
    
    /* Панель счетов */
    .fixed-panel { padding: 20px; border-left: 1px solid #111; }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #0a0a0a; font-size: 13px; color: #444; }
    
    /* Кнопки */
    .stButton>button { background: #0a0a0a !important; border: 1px solid #1a1a1a !important; color: #555 !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ (18,500 с учетом Арины и Натана)
if 'db' not in st.session_state:
    st.session_state.db = {
        "current_month": datetime.datetime.now().strftime("%B %Y"),
        "income": 18500,
        "fixed": {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1400, "Здоровье": 350},
        "envs": {
            "Еда": {"b": 3500, "l": 3500},
            "Доп. уроки": {"b": 1850, "l": 1850},
            "Машина": {"b": 1000, "l": 1000},
            "Арина": {"b": 100, "l": 100},
            "Натан": {"b": 100, "l": 100},
            "Красота": {"b": 335, "l": 335},
            "Разное": {"b": 625, "l": 625}
        }
    }

# МЕСЯЦ СВЕРХУ
st.markdown(f'<div style="text-align:center; padding:20px 0; font-size:20px; letter-spacing:4px; font-weight:300;">{st.session_state.db["current_month"].upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3.5, 1])

with main_c:
    # КРУГ ОСТАТКА
    current_sum = sum(v['b'] for v in st.session_state.db['envs'].values())
    pct = int((current_sum / st.session_state.db['income']) * 100)
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding: 20px 0;">
            <div style="width:130px; height:130px; border-radius:50%; background:radial-gradient(closest-side, black 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #111 0); display:flex; align-items:center; justify-content:center;">
                <div style="text-align:center;"><span style="font-size:24px; font-weight:300;">{int(current_sum)} ₪</span><br><span style="font-size:11px;color:#30d158;opacity:0.5;">{pct}%</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # КОНВЕРТЫ (Теперь их 7)
    rows = [st.columns(4), st.columns(3)]
    all_names = list(st.session_state.db['envs'].keys())
    
    for i, name in enumerate(all_names):
        d = st.session_state.db['envs'][name]
        usage = int((d['b'] / d['l']) * 100) if d['l'] > 0 else 0
        color = "#30d158" if usage > 50 else ("#ff9f0a" if usage > 20 else "#ff453a")
        col_idx = i if i < 4 else i - 4
        row_idx = 0 if i < 4 else 1
        with rows[row_idx][col_idx]:
            st.markdown(f"""
                <div class="apple-card" style="--status:{color}">
                    <div class="card-title">{name}</div>
                    <div class="card-val">{int(d["b"])} ₪</div>
                    <div class="card-pct">{usage}%</div>
                </div>
            """, unsafe_allow_html=True)

with side_c:
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    st.write("🔒 **FIXED**")
    for n, v in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    dt = datetime.datetime.now()
    st.markdown(f'<div style="text-align:center; margin-top:40px;"><div style="color:#ff3b30; font-size:11px;">{dt.strftime("%A").upper()}</div><div style="font-size:45px;">{dt.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ВВОД (МАКСИМАЛЬНО ТЕМНЫЙ)
st.write("---")
with st.form("main_input", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat = st.selectbox("", list(st.session_state.db['envs'].keys()), label_visibility="collapsed")
    with c2: val = st.number_input("", min_value=0, step=1, value=0, label_visibility="collapsed")
    with c3:
        if st.form_submit_button("ADD", use_container_width=True):
            if val > 0:
                st.session_state.db['envs'][cat]['b'] -= val
                st.rerun()

# НАСТРОЙКИ
with st.expander("Management"):
    if st.button("🚀 NEW MONTH (RESET)"):
        for k in st.session_state.db['envs']: st.session_state.db['envs'][k]['b'] = st.session_state.db['envs'][k]['l']
        st.rerun()
    st.write("---")
    for k in st.session_state.db['envs']:
        st.session_state.db['envs'][k]['l'] = st.number_input(f"Лимит {k}", value=st.session_state.db['envs'][k]['l'])
