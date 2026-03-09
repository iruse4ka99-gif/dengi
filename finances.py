import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ДИЗАЙН: ЧЕРНЫЙ ПРЕМИУМ (APPLE STYLE)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');
    html, body, [class*="stApp"] { background-color: #000; font-family: 'Inter', sans-serif; color: #fff; }

    /* Чистим интерфейс от мусора Streamlit */
    header, footer {visibility: hidden;}
    .stSelectbox div, .stNumberInput div { background-color: #0a0a0a !important; border: 1px solid #1a1a1a !important; color: white !important; border-radius: 12px !important; }
    
    .fixed-panel { padding: 20px; border-left: 1px solid #1a1a1a; }
    .fixed-row { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #0f0f0f; font-size: 13px; color: #444; }

    .apple-card {
        background: rgba(28, 28, 30, 0.4); backdrop-filter: blur(20px);
        border-radius: 24px; padding: 25px; text-align: center;
        border-top: 3px solid var(--status); cursor: pointer;
    }
    .card-title { font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 2px; }
    .card-val { font-size: 32px; font-weight: 500; margin: 10px 0; }
    .card-pct { font-size: 12px; color: var(--status); font-weight: 600; }
    
    /* Скрытая кнопка-невидимка для открытия истории */
    .stButton>button { background: transparent !important; border: none !important; color: #444 !important; font-size: 10px !important; }
    .stButton>button:hover { color: #fff !important; }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ (ЧИСТЫЕ 18,500)
if 'db' not in st.session_state:
    st.session_state.db = {
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

main_col, side_col = st.columns([3, 1])

with main_col:
    # КРУГ ОСТАТКА (ОТ 18,500)
    total_fixed = sum(st.session_state.db['fixed'].values())
    current_envs_sum = sum(v['b'] for v in st.session_state.db['envs'].values())
    actual_left = current_envs_sum # По сути, это и есть наш свободный остаток
    pct = int((actual_left / st.session_state.db['income']) * 100)

    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding: 40px 0;">
            <div style="width:160px; height:160px; border-radius:50%; background:radial-gradient(closest-side, black 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #111 0); display:flex; align-items:center; justify-content:center; box-shadow: 0 0 40px rgba(48,209,88,0.1);">
                <div style="text-align:center;"><span style="font-size:30px; font-weight:300;">{int(actual_left)} ₪</span><br><span style="font-size:12px;color:#30d158;opacity:0.6;">{pct}%</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # КОНВЕРТЫ
    cols = st.columns(5)
    for i, (name, d) in enumerate(st.session_state.db['envs'].items()):
        usage = int((d['b'] / d['l']) * 100) if d['l'] > 0 else 0
        color = "#30d158" if usage > 50 else ("#ff9f0a" if usage > 20 else "#ff453a")
        with cols[i]:
            st.markdown(f"""
                <div class="apple-card" style="--status: {color}">
                    <div class="card-title">{name}</div>
                    <div class="card-val">{int(d['b'])} ₪</div>
                    <div class="card-pct">{usage}%</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("HISTORY", key=f"h_{name}"): st.session_state.view_h = name

# ИСТОРИЯ (ПОЯВЛЯЕТСЯ ТОЛЬКО ПРИ НАЖАТИИ)
if 'view_h' in st.session_state:
    cat = st.session_state.view_h
    st.markdown(f"<div style='color:#666; font-size:12px; padding:10px;'>Последние траты {cat}:</div>", unsafe_allow_html=True)
    for log in st.session_state.db['envs'][cat]['h'][:3]:
        st.write(f"• {log}")
    if st.button("Close history", key="close"): del st.session_state.view_h; st.rerun()

with side_col:
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    st.write("🔒 **FIXED**")
    for n, v in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    
    # Календарь
    dt = datetime.datetime.now()
    st.markdown(f'<div style="text-align:center; margin-top:40px;"><div style="color:#ff3b30; font-size:11px; letter-spacing:2px;">{dt.strftime("%B").upper()}</div><div style="font-size:50px; font-weight:300;">{dt.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ВВОД (ТЕМНЫЙ И АККУРАТНЫЙ)
st.write("---")
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat_choice = st.selectbox("", list(st.session_state.db['envs'].keys()), label_visibility="collapsed")
    with c2: amount = st.number_input("", min_value=0, step=1, value=0, label_visibility="collapsed")
    with c3: 
        if st.form_submit_button("ADD TRANSACTION"):
            if amount > 0:
                st.session_state.db['envs'][cat_choice]['b'] -= amount
                st.session_state.db['envs'][cat_choice]['h'].insert(0, f"-{amount} ₪ ({datetime.datetime.now().strftime('%H:%M')})")
                st.rerun()

# СЕКЦИЯ РЕДАКТИРОВАНИЯ (СПРЯТАНА ВНИЗУ)
with st.expander("Settings / Edit Balances"):
    for k in st.session_state.db['envs']:
        st.session_state.db['envs'][k]['l'] = st.number_input(f"Limit {k}", value=st.session_state.db['envs'][k]['l'])
    for k in st.session_state.db['fixed']:
        st.session_state.db['fixed'][k] = st.number_input(f"Fixed {k}", value=st.session_state.db['fixed'][k])
    if st.button("Save Changes"): st.rerun()
