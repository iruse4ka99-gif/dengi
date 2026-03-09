import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ДИЗАЙН: APPLE DARK MODE
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    html, body, [class*="stApp"] { background-color: #000000 !important; color: #ffffff !important; font-family: 'Inter', sans-serif; }

    /* Поля ввода */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #080808 !important; border: 1px solid #1a1a1a !important; border-radius: 12px !important;
    }
    input { color: #ffffff !important; font-size: 14px !important; }

    /* Кнопка ADD */
    .stButton>button {
        background-color: #0a0a0a !important; color: #30d158 !important;
        border: 1px solid rgba(48, 209, 88, 0.2) !important; border-radius: 14px !important;
        height: 45px; width: 100%; transition: 0.3s; font-weight: 500;
    }
    .stButton>button:hover { border-color: #30d158 !important; background: #111 !important; }

    /* Карточки конвертов */
    .env-card {
        background: rgba(28, 28, 30, 0.5); backdrop-filter: blur(20px);
        border-radius: 24px; padding: 22px; text-align: center;
        border-top: 3px solid var(--status); margin-bottom: 5px;
    }
    .card-val { font-size: 30px; font-weight: 500; margin: 2px 0; color: #fff; }
    .card-pct { font-size: 12px; color: var(--status); font-weight: 600; }

    .fixed-panel { padding: 20px; border-left: 1px solid #111; }
    .fixed-row-edit { display: flex; justify-content: space-between; align-items: center; padding: 5px 0; }
    
    /* Специфический стиль для маленьких инпутов в боковой панели */
    .fixed-panel input { 
        background-color: transparent !important; 
        border: none !important; 
        text-align: right !important; 
        color: #30d158 !important;
        width: 80px !important;
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
st.markdown(f'<div style="text-align:center; padding-top:20px; font-size:18px; font-weight:300; letter-spacing:4px; color:#444;">{now.strftime("%B %Y").upper()}</div>', unsafe_allow_html=True)

main_c, side_c = st.columns([3.5, 1])

# ЛОГИКА БОКОВОЙ ПАНЕЛИ (Сначала считаем FIXED)
with side_c:
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    st.write("⚙️ **FIXED EDIT**")
    
    new_fixed = {}
    for n, v in st.session_state.db['fixed'].items():
        # Создаем поля ввода для каждой фиксированной суммы
        val = st.number_input(f"{n}", value=int(v), step=10, key=f"fix_{n}", label_visibility="visible")
        new_fixed[n] = val
    
    st.session_state.db['fixed'] = new_fixed
    total_fixed = sum(new_fixed.values())
    
    st.markdown(f'<div style="text-align:center; margin-top:30px;"><div style="color:#ff3b30; font-size:11px;">{now.strftime("%A").upper()}</div><div style="font-size:50px; font-weight:200;">{now.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ЛОГИКА ОСНОВНОЙ ПАНЕЛИ
with main_c:
    current_left_envs = sum(v['b'] for v in st.session_state.db['envs'].values())
    # Остаток = Зарплата - Потраченное в конвертах - Фиксированные платежи
    # Но так как конверты уже часть зарплаты, мы показываем реальный остаток в "кошельке"
    pct = int((current_left_envs / (st.session_state.db['income'] - total_fixed)) * 100) if (st.session_state.db['income'] - total_fixed) > 0 else 0
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding: 25px 0;">
            <div style="width:160px; height:160px; border-radius:50%; background:radial-gradient(closest-side, black 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #111 0); display:flex; align-items:center; justify-content:center; border: 1px solid #111;">
                <div style="text-align:center;">
                    <span style="font-size:34px; font-weight:300;">{int(current_left_envs)} ₪</span><br>
                    <span style="font-size:10px;color:#30d158;letter-spacing:1px;">ОСТАТОК</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Конверты
    envs_list = list(st.session_state.db['envs'].items())
    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            if idx < 7:
                name, d = envs_list[idx]
                usage = int((d['b'] / d['l']) * 100) if d['l'] > 0 else 0
                color = "#30d158" if usage > 50 else ("#ff9f0a" if usage > 20 else "#ff453a")
                with cols[j]:
                    if st.button(name, key=f"btn_{name}", use_container_width=True):
                        st.session_state.active_env = name if st.session_state.get('active_env') != name else None
                    st.markdown(f'<div class="env-card" style="--status:{color}"><div class="card-val">{int(d["b"])} ₪</div><div class="card-pct">{usage}%</div></div>', unsafe_allow_html=True)
                    if st.session_state.get('active_env') == name:
                        st.markdown(f'<div style="font-size:11px; color:#555; padding:10px; background:#050505; border-radius:10px;">{"<br>".join(d["h"][:3]) if d["h"] else "Нет трат"}</div>', unsafe_allow_html=True)
            elif idx == 7:
                days_left = (datetime.date(now.year + (now.month // 12), (now.month % 12) + 1, 1) - now.date()).days
                with cols[j]:
                    st.markdown(f'<div class="env-card" style="--status:#222; opacity:0.6;"><div class="card-val" style="color:#444;">{days_left}</div><div style="font-size:10px; color:#333;">ДНЕЙ ДО 1-ГО</div></div>', unsafe_allow_html=True)

# ФОРМА ВВОДА ТРАТЫ
st.write("---")
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat_choice = st.selectbox("", list(st.session_state.db['envs'].keys()), label_visibility="collapsed")
    with c2: amount = st.number_input("", min_value=0, step=1, value=0, label_visibility="collapsed")
    with c3:
        if st.form_submit_button("ADD TRANSACTION"):
            if amount > 0:
                st.session_state.db['envs'][cat_choice]['b'] -= amount
                st.session_state.db['envs'][cat_choice]['h'].insert(0, f"-{amount} ₪ ({now.strftime('%H:%M')})")
                st.rerun()
