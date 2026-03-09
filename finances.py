import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# СТИЛИ: APPLE GLASS + СВЕТОФОР
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="stApp"] { background-color: #000; font-family: 'Inter', sans-serif; color: #fff; }

    /* Боковая панель для фиксированных */
    .fixed-panel {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px);
        border-radius: 20px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .fixed-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1a1a1a; font-size: 13px; color: #888; }

    /* Конверты-Светофоры */
    .apple-card {
        background: rgba(28, 28, 30, 0.6); backdrop-filter: blur(20px);
        border-radius: 24px; padding: 20px; text-align: center;
        border-top: 5px solid var(--status); margin-bottom: 10px;
        transition: 0.3s;
    }
    .card-title { font-size: 12px; color: #8e8e93; text-transform: uppercase; }
    .card-val { font-size: 28px; font-weight: 600; margin: 5px 0; }
    
    /* Кастомная кнопка ввода (неброская) */
    .stButton>button {
        background: rgba(255,255,255,0.05) !important; color: #aaa !important;
        border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important;
        width: 100%; height: 35px;
    }
    .stButton>button:hover { border-color: #007aff !important; color: #fff !important; }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ (Твои 5 основных конвертов)
if 'db' not in st.session_state:
    st.session_state.db = {
        "fixed": {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1400, "Здоровье": 350},
        "envs": {
            "Еда": {"b": 4000, "l": 4000, "h": []},
            "Доп. уроки": {"b": 1850, "l": 1850, "h": []},
            "Машина": {"b": 1365, "l": 1365, "h": []},
            "Красота": {"b": 335, "l": 335, "h": []},
            "Разное": {"b": 1300, "l": 1300, "h": []}
        }
    }

side, main = st.columns([1, 3])

with side:
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    st.write("🔒 **ФИКСИРОВАНО**")
    for name, val in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{name}</span><span>{val} ₪</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with main:
    # Центральный круг остатка (Деньги)
    total_left = sum(v['b'] for v in st.session_state.db['envs'].values())
    pct_total = int((total_left / 8850) * 100)
    st.markdown(f"""
        <div style="display:flex; justify-content:center; margin-bottom:30px;">
            <div style="width:150px; height:150px; border-radius:50%; background:radial-gradient(closest-side, black 86%, transparent 87% 100%), conic-gradient(#30d158 {pct_total}%, #1c1c1e 0); display:flex; align-items:center; justify-content:center;">
                <div style="text-align:center;"><span style="font-size:24px; font-weight:600;">{int(total_left)} ₪</span><br><span style="font-size:10px;color:#666;">ОСТАТОК</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Конверты со Светофором
    cols = st.columns(5)
    items = list(st.session_state.db['envs'].items())
    for i, (name, d) in enumerate(items):
        usage = d['b'] / d['l']
        color = "#30d158" if usage > 0.5 else ("#ff9f0a" if usage > 0.15 else "#ff453a") # Светофор
        with cols[i]:
            st.markdown(f"""
                <div class="apple-card" style="--status: {color}">
                    <div class="card-title">{name}</div>
                    <div class="card-val">{int(d['b'])} ₪</div>
                    <div style="font-size:10px; color:#444;">ЛИМИТ {int(d['l'])}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("📜 История", key=f"h_{name}"): st.session_state.view_h = name
            if st.button("⋮ Опции", key=f"s_{name}"): st.session_state.edit_cat = name

# ПОКАЗ ИСТОРИИ (Если нажата кнопка)
if 'view_h' in st.session_state:
    cat = st.session_state.view_h
    with st.expander(f"📜 История: {cat}", expanded=True):
        if not st.session_state.db['envs'][cat]['h']: st.write("Трат еще нет")
        for log in st.session_state.db['envs'][cat]['h']: st.write(log)
        if st.button("Закрыть"): del st.session_state.view_h; st.rerun()

# ВВОД (НАДЕЖНЫЙ)
st.write("---")
with st.container():
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat_choice = st.selectbox("Куда списываем?", list(st.session_state.db['envs'].keys()))
    with c2: amount = st.number_input("Сумма ₪", min_value=0, step=1)
    with c3: 
        st.write(" ") # отступ
        if st.button("ДОБАВИТЬ ТРАТУ"):
            if amount > 0:
                st.session_state.db['envs'][cat_choice]['b'] -= amount
                time = datetime.datetime.now().strftime("%H:%M")
                st.session_state.db['envs'][cat_choice]['h'].insert(0, f"{time} | -{amount} ₪")
                st.success(f"Записано в {cat_choice}")
                st.rerun()
