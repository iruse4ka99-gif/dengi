import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ДИЗАЙН: APPLE TRUE BLACK + МЕСЯЦЫ
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');
    html, body, [class*="stApp"] { background-color: #000; font-family: 'Inter', sans-serif; color: #fff; }
    
    /* Ультра-черные поля ввода */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #050505 !important; border: 1px solid #111 !important; color: white !important;
    }
    input { color: white !important; }

    .fixed-panel { padding: 20px; border-left: 1px solid #111; }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #0a0a0a; font-size: 13px; color: #444; }

    .apple-card {
        background: rgba(28, 28, 30, 0.4); backdrop-filter: blur(20px);
        border-radius: 24px; padding: 25px; text-align: center;
        border-top: 3px solid var(--status); margin-bottom: 10px;
    }
    .card-title { font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 2px; }
    .card-val { font-size: 32px; font-weight: 500; margin: 10px 0; }
    .card-pct { font-size: 11px; color: var(--status); font-weight: 600; }
    
    .stButton>button { background: transparent !important; border: 1px solid #111 !important; color: #222 !important; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# ЛОГИКА
if 'db' not in st.session_state:
    st.session_state.db = {
        "current_month": datetime.datetime.now().strftime("%B %Y"),
        "history": {},
        "income": 18500,
        "fixed": {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1400, "Здоровье": 350},
        "envs": {
            "Еда": {"b": 3500, "l": 3500, "h": []},
            "Доп. уроки": {"b": 1850, "l": 1850, "h": []},
            "Машина": {"b": 1000, "l": 1000, "h": []},
            "Красота": {"b": 335, "l": 335, "h": []},
            "Разное": {"b": 825, "l": 825, "h": []}
        }
    }

# ШАПКА С МЕСЯЦЕМ
st.markdown(f'<div style="text-align:center; padding-top:20px; font-size:20px; letter-spacing:3px; font-weight:300;">{st.session_state.db["current_month"].upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3, 1])

with main_c:
    # КРУГ
    current_sum = sum(v['b'] for v in st.session_state.db['envs'].values())
    pct = int((current_sum / st.session_state.db['income']) * 100)
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding: 30px 0;">
            <div style="width:140px; height:140px; border-radius:50%; background:radial-gradient(closest-side, black 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #111 0); display:flex; align-items:center; justify-content:center;">
                <div style="text-align:center;"><span style="font-size:26px; font-weight:300;">{int(current_sum)} ₪</span><br><span style="font-size:12px;color:#30d158;opacity:0.5;">{pct}%</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (name, d) in enumerate(st.session_state.db['envs'].items()):
        usage = int((d['b'] / d['l']) * 100) if d['l'] > 0 else 0
        color = "#30d158" if usage > 50 else ("#ff9f0a" if usage > 20 else "#ff453a")
        with cols[i]:
            st.markdown(f'<div class="apple-card" style="--status:{color}"><div class="card-title">{name}</div><div class="card-val">{int(d["b"])} ₪</div><div class="card-pct">{usage}%</div></div>', unsafe_allow_html=True)

with side_c:
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    st.write("🔒 **FIXED**")
    for n, v in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    dt = datetime.datetime.now()
    st.markdown(f'<div style="text-align:center; margin-top:40px;"><div style="color:#ff3b30; font-size:11px;">{dt.strftime("%A").upper()}</div><div style="font-size:50px;">{dt.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ВВОД (АВТО-ОЧИСТКА)
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

# АРХИВ
with st.expander("Archive & Month Management"):
    if st.button("🏁 CLOSE MONTH (SAVE TO ARCHIVE)"):
        m = st.session_state.db['current_month']
        st.session_state.db['history'][m] = {k: v['b'] for k, v in st.session_state.db['envs'].items()}
        for k in st.session_state.db['envs']: st.session_state.db['envs'][k]['b'] = st.session_state.db['envs'][k]['l']
        st.success(f"Month {m} archived!")
        st.rerun()
    
    if st.session_state.db['history']:
        st.write("### Past Months History")
        for m_name, data in st.session_state.db['history'].items():
            st.write(f"📁 {m_name}: Остаток был {int(sum(data.values()))} ₪")
