import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ДИЗАЙН: APPLE TRUE BLACK
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');
    
    html, body, [class*="stApp"], [data-testid="stAppViewContainer"] { 
        background-color: #000000 !important; 
        color: #ffffff !important; 
        font-family: 'Inter', sans-serif;
    }

    /* Принудительный черный для полей ввода */
    div[data-baseweb="input"], div[data-baseweb="select"], div[role="listbox"] {
        background-color: #080808 !important;
        border-radius: 12px !important;
    }
    
    input, div[data-baseweb="select"] span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #080808 !important;
        border: 1px solid #1a1a1a !important;
    }

    .apple-card {
        background: rgba(28, 28, 30, 0.4); backdrop-filter: blur(20px);
        border-radius: 24px; padding: 22px; text-align: center;
        border-top: 3px solid var(--status); margin-bottom: 10px;
    }
    .card-title { font-size: 10px; color: #444; text-transform: uppercase; letter-spacing: 1.5px; }
    .card-val { font-size: 28px; font-weight: 500; margin: 5px 0; }
    .card-pct { font-size: 11px; color: var(--status); font-weight: 600; }
    .card-limit { font-size: 9px; color: #222; }

    .fixed-panel { padding: 20px; border-left: 1px solid #111; }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #080808; font-size: 12px; color: #333; }
    
    .stButton>button { background: transparent !important; border: 1px solid #111 !important; color: #444 !important; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ И АВТОМАТИЗАЦИЯ
now = datetime.datetime.now()
current_month_key = now.strftime("%Y-%m")

if 'db' not in st.session_state:
    st.session_state.db = {
        "last_reset": current_month_key,
        "income": 18500,
        "fixed": {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1200, "Здоровье": 350},
        "envs": {
            "Продукты": {"b": 4000, "l": 4000},
            "Доп. уроки": {"b": 2254, "l": 2254},
            "Машина": {"b": 500, "l": 500},
            "Одежда": {"b": 200, "l": 200},
            "Арина": {"b": 100, "l": 100},
            "Натан": {"b": 100, "l": 100},
            "Разное": {"b": 556, "l": 556}
        }
    }

# АВТО-СПИСАНИЕ 1-ГО ЧИСЛА
if st.session_state.db["last_reset"] != current_month_key:
    for k in st.session_state.db['envs']:
        st.session_state.db['envs'][k]['b'] = st.session_state.db['envs'][k]['l']
    st.session_state.db["last_reset"] = current_month_key
    st.toast("Новый месяц! Фиксированные платежи списаны, конверты обновлены.")

# РАСЧЕТЫ
total_fixed = sum(st.session_state.db["fixed"].values())
current_envs_sum = sum(v['b'] for v in st.session_state.db['envs'].values())
total_available = current_envs_sum + total_fixed # Для визуализации "всей зарплаты" в начале

st.markdown(f'<div style="text-align:center; padding:15px 0; font-size:18px; letter-spacing:3px; font-weight:300; color:#555;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3.5, 1])

with main_c:
    # ГЛАВНЫЙ КРУГ (Вся зарплата)
    # Показываем сколько осталось от 18500 с учетом уже потраченного в конвертах
    grand_total_left = current_envs_sum 
    pct = int((grand_total_left / st.session_state.db["income"]) * 100)
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding-bottom: 25px;">
            <div style="width:150px; height:150px; border-radius:50%; background:radial-gradient(closest-side, black 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #111 0); display:flex; align-items:center; justify-content:center;">
                <div style="text-align:center;"><span style="font-size:28px; font-weight:300;">{int(grand_total_left)} ₪</span><br><span style="font-size:10px;color:#30d158;opacity:0.5;">ОСТАТОК ОТ {st.session_state.db['income']}</span></div>
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

with side_c:
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    st.write("🔒 **АВТОСПИСАНИЕ**")
    for n, v in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row" style="opacity:0.6;"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; margin-top:40px;"><div style="color:#ff3b30; font-size:11px;">{now.strftime("%A").upper()}</div><div style="font-size:45px;">{now.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat = st.selectbox("Category", list(st.session_state.db['envs'].keys()), label_visibility="collapsed")
    with c2: val = st.number_input("Amount", min_value=0, step=1, value=0, label_visibility="collapsed")
    with c3:
        if st.form_submit_button("ВНЕСТИ ТРАТУ", use_container_width=True):
            if val > 0:
                st.session_state.db['envs'][cat]['b'] -= val
                st.rerun()

with st.expander("Management"):
    if st.button("🚀 СБРОСИТЬ МЕСЯЦ ВРУЧНУЮ"):
        for k in st.session_state.db['envs']: st.session_state.db['envs'][k]['b'] = st.session_state.db['envs'][k]['l']
        st.rerun()
