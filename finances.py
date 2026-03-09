import streamlit as st
import datetime
import calendar

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ДИЗАЙН: ЧИСТЫЙ APPLE (БЕЗ СМАЙЛИКОВ)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="stApp"] { background-color: #000; font-family: 'Inter', sans-serif; color: #fff; }

    /* Панель слева */
    .side-panel {
        background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(30px);
        border-radius: 24px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #111; font-size: 13px; color: #666; }
    
    /* Календарь */
    .cal-box { text-align: center; margin-top: 30px; padding-top: 25px; border-top: 1px solid #1a1a1a; }
    .cal-month { font-size: 13px; color: #ff3b30; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 5px; }
    .cal-day { font-size: 48px; font-weight: 600; color: #fff; line-height: 1; }

    /* Конверты */
    .apple-card {
        background: rgba(28, 28, 30, 0.5); backdrop-filter: blur(20px);
        border-radius: 24px; padding: 22px; text-align: center;
        border-top: 4px solid var(--status); margin-bottom: 15px;
        transition: 0.3s ease;
    }
    .card-title { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 1px; }
    .card-val { font-size: 30px; font-weight: 600; margin-top: 8px; color: #fff; }
    .card-pct { font-size: 13px; font-weight: 400; color: var(--status); margin-bottom: 12px; }
    
    /* Кнопка HISTORY (Apple Style) */
    .stButton>button {
        background: rgba(255,255,255,0.03) !important; 
        color: #444 !important;
        border: 1px solid rgba(255,255,255,0.05) !important; 
        border-radius: 10px !important;
        font-size: 10px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        height: 28px !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover { 
        background: rgba(255,255,255,0.08) !important; 
        color: #fff !important; 
        border-color: rgba(255,255,255,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ
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

now = datetime.datetime.now()
side, main = st.columns([1, 3.5])

with side:
    st.markdown('<div class="side-panel">', unsafe_allow_html=True)
    st.write("🔒 **FIXED**")
    for name, val in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{name}</span><span>{val} ₪</span></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="cal-box">
            <div class="cal-month">{now.strftime('%B')}</div>
            <div class="cal-day">{now.day}</div>
            <div style="color:#333; font-size:11px; margin-top:8px;">{now.strftime('%A')}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with main:
    # Центральное кольцо
    total_left = sum(v['b'] for v in st.session_state.db['envs'].values())
    total_limit = sum(v['l'] for v in st.session_state.db['envs'].values())
    pct_total = int((total_left / total_limit) * 100)
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; margin-bottom:40px;">
            <div style="width:130px; height:130px; border-radius:50%; background:radial-gradient(closest-side, black 86%, transparent 87% 100%), conic-gradient(#30d158 {pct_total}%, #1c1c1e 0); display:flex; align-items:center; justify-content:center; box-shadow: 0 0 30px rgba(48,209,88,0.1);">
                <div style="text-align:center;"><span style="font-size:24px; font-weight:600; color:#fff;">{int(total_left)} ₪</span><br><span style="font-size:14px;color:#30d158;opacity:0.8;">{pct_total}%</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Конверты
    cols = st.columns(5)
    for i, (name, d) in enumerate(st.session_state.db['envs'].items()):
        usage_pct = int((d['b'] / d['l']) * 100) if d['l'] > 0 else 0
        color = "#30d158" if usage_pct > 50 else ("#ff9f0a" if usage_pct > 20 else "#ff453a")
        with cols[i]:
            st.markdown(f"""
                <div class="apple-card" style="--status: {color}">
                    <div class="card-title">{name}</div>
                    <div class="card-val">{int(d['b'])} ₪</div>
                    <div class="card-pct">{usage_pct}%</div>
                </div>
            """, unsafe_allow_html=True)
            # Кнопка без смайлика
            if st.button("HISTORY", key=f"h_{name}"): st.session_state.view_h = name

# ВВОД (ОБНУЛЯЕМЫЙ)
st.write("---")
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat_choice = st.selectbox("Category", list(st.session_state.db['envs'].keys()))
    with c2: amount = st.number_input("Amount ₪", min_value=0, step=1, value=0)
    with c3: 
        st.write("<br>", unsafe_allow_html=True)
        if st.form_submit_button("ADD TRANSACTION"):
            if amount > 0:
                st.session_state.db['envs'][cat_choice]['b'] -= amount
                time = datetime.datetime.now().strftime("%H:%M")
                st.session_state.db['envs'][cat_choice]['h'].insert(0, f"{time} | -{amount} ₪")
                st.rerun()

# ПРОСМОТР ИСТОРИИ
if 'view_h' in st.session_state:
    cat = st.session_state.view_h
    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:15px; margin-top:20px;'><b>{cat} History:</b>", unsafe_allow_html=True)
    for log in st.session_state.db['envs'][cat]['h'][:5]:
        st.write(f"• {log}")
    if st.button("Close"): 
        del st.session_state.view_h
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
