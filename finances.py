import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ДИЗАЙН: ULTIMATE APPLE BLACK (ЧИСТАЯ ЭСТЕТИКА)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap');
    html, body, [class*="stApp"] { background-color: #000000 !important; color: #ffffff !important; font-family: 'Inter', sans-serif; }

    /* Убираем лишний декор Streamlit */
    header, footer {visibility: hidden;}
    
    /* Темные поля ввода */
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: #0a0a0a !important; border: 1px solid #1a1a1a !important; border-radius: 14px !important;
    }
    input { color: #ffffff !important; }

    /* Названия конвертов как ссылки */
    .env-label-btn {
        background: none !important; border: none !important; padding: 0 !important;
        color: #444 !important; font-size: 11px !important; text-transform: uppercase !important;
        letter-spacing: 2px !important; cursor: pointer; transition: 0.3s; margin-bottom: 5px;
    }
    .env-label-btn:hover { color: #30d158 !important; }

    /* Карточки Apple */
    .apple-card {
        background: rgba(255, 255, 255, 0.02); border-radius: 24px; padding: 25px;
        border-top: 3px solid var(--status); text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .card-val { font-size: 32px; font-weight: 300; color: #fff; margin: 5px 0; }
    .card-pct { font-size: 12px; color: var(--status); font-weight: 600; opacity: 0.7; }
    
    /* Кнопка записи */
    .stButton>button {
        background: transparent !important; color: #30d158 !important;
        border: 1px solid rgba(48, 209, 88, 0.2) !important; border-radius: 12px !important;
        height: 42px; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { border-color: #30d158 !important; background: rgba(48,209,88,0.05) !important; }

    .fixed-box { background: #050505; border-radius: 24px; padding: 25px; border: 1px solid #111; }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #0a0a0a; font-size: 13px; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ (Твой бюджет 18 500)
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
main_c, side_c = st.columns([3.5, 1])

with main_c:
    # Центральный индикатор
    total_left = sum(v['b'] for v in st.session_state.db['envs'].values())
    pct = int((total_left / 7710) * 100) if total_left > 0 else 0
    st.markdown(f"""
        <div style="display:flex; justify-content:center; padding: 40px 0;">
            <div style="width:150px; height:150px; border-radius:50%; background:radial-gradient(closest-side, black 88%, transparent 89% 100%), conic-gradient(#30d158 {pct}%, #111 0); display:flex; align-items:center; justify-content:center; border: 1px solid #111;">
                <div style="text-align:center;"><span style="font-size:32px; font-weight:300;">{int(total_left)} ₪</span><br><span style="font-size:10px;color:#30d158;opacity:0.4;letter-spacing:1px;">ОСТАТОК</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Сетка конвертов
    envs = list(st.session_state.db['envs'].items())
    for i in range(0, 8, 4):
        cols = st.columns(4)
        for j in range(4):
            idx = i + j
            with cols[j]:
                if idx < 7:
                    name, d = envs[idx]
                    usage = int((d['b'] / d['l']) * 100) if d['l'] > 0 else 0
                    color = "#30d158" if usage > 50 else ("#ff9f0a" if usage > 20 else "#ff453a")
                    
                    # Кнопка-название (вместо уродливой серой кнопки)
                    if st.button(name.upper(), key=f"label_{name}"):
                        st.session_state.active = name if st.session_state.get('active') != name else None
                    
                    st.markdown(f"""
                        <div class="apple-card" style="--status:{color}">
                            <div class="card-val">{int(d["b"])} ₪</div>
                            <div class="card-pct">{usage}% от {int(d["l"])}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.session_state.get('active') == name:
                        st.markdown(f'<div style="font-size:11px; color:#555; padding-top:10px; text-align:center;">{" | ".join(d["h"][:2]) if d["h"] else "Трат нет"}</div>', unsafe_allow_html=True)
                
                elif idx == 7: # 8-я карточка
                    days = (datetime.date(now.year + (now.month // 12), (now.month % 12) + 1, 1) - now.date()).days
                    st.markdown(f"""
                        <div style="margin-top:38px;">
                            <div class="apple-card" style="--status:#222; opacity:0.3;">
                                <div class="card-val" style="color:#444;">{days}</div>
                                <div style="font-size:10px; color:#222;">ДНЕЙ ДО 1-ГО</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

with side_c:
    st.markdown('<div class="fixed-box">', unsafe_allow_html=True)
    st.write("🔒 **ФИКСИРОВАНО**")
    for n, v in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{n}</span><span>{v} ₪</span></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div style="text-align:center; margin-top:40px;"><div style="color:#ff3b30; font-size:12px; letter-spacing:2px;">{now.strftime("%B").upper()}</div><div style="font-size:54px; font-weight:200;">{now.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Нижняя панель ввода
st.write("---")
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat = st.selectbox("", list(st.session_state.db['envs'].keys()), label_visibility="collapsed")
    with c2: val = st.number_input("", min_value=0, step=1, value=0, label_visibility="collapsed")
    with c3:
        if st.form_submit_button("ЗАПИСАТЬ ТРАТУ"):
            if val > 0:
                st.session_state.db['envs'][cat]['b'] -= val
                st.session_state.db['envs'][cat]['h'].insert(0, f"-{val}")
                st.rerun()

with st.expander("⚙️ НАСТРОЙКИ СУММ"):
    for k in st.session_state.db['fixed']:
        st.session_state.db['fixed'][k] = st.number_input(f"Счет {k}", value=st.session_state.db['fixed'][k])
    if st.button("Сохранить изменения"): st.rerun()
