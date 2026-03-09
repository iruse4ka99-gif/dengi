import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ДИЗАЙН: APPLE DARK (БЕЗ БЕЛОГО СВЕТА)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="stApp"] { background-color: #000; font-family: 'Inter', sans-serif; color: #fff; }

    /* Поля ввода (ТЕМНЫЕ) */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: #1c1c1e !important; border: 1px solid #333 !important; color: white !important;
    }
    input { color: white !important; }

    .fixed-panel {
        background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(25px);
        border-radius: 20px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .fixed-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #111; font-size: 13px; cursor: pointer; }

    .apple-card {
        background: rgba(28, 28, 30, 0.6); backdrop-filter: blur(20px);
        border-radius: 24px; padding: 20px; text-align: center;
        border-top: 4px solid var(--status); cursor: pointer;
    }
    .card-title { font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 1px; }
    .card-val { font-size: 30px; font-weight: 600; margin-top: 5px; }
    .card-pct { font-size: 12px; color: var(--status); }
    
    .history-text { font-size: 11px; color: #555; margin-top: 10px; text-align: left; }
    </style>
    """, unsafe_allow_html=True)

# ИНИЦИАЛИЗАЦИЯ (С зарплатой 18500)
if 'db' not in st.session_state:
    st.session_state.db = {
        "income": 18500,
        "fixed": {"Машканта": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1400, "Здоровье": 350},
        "envs": {
            "Еда": {"b": 4000, "l": 4000, "h": []},
            "Доп. уроки": {"b": 1850, "l": 1850, "h": []},
            "Машина": {"b": 1365, "l": 1365, "h": []},
            "Красота": {"b": 335, "l": 335, "h": []},
            "Разное": {"b": 1300, "l": 1300, "h": []}
        }
    }

side, main = st.columns([1, 3.5])

with side:
    st.markdown('<div class="fixed-panel">', unsafe_allow_html=True)
    st.write("🔒 **FIXED**")
    for name, val in st.session_state.db['fixed'].items():
        st.markdown(f'<div class="fixed-row"><span>{name}</span><span>{val} ₪</span></div>', unsafe_allow_html=True)
    
    if st.button("Изменить счета"): st.session_state.edit_f = True
    
    # Редактирование фиксированных
    if st.session_state.get('edit_f'):
        for k in st.session_state.db['fixed']:
            st.session_state.db['fixed'][k] = st.number_input(f"Сумма {k}", value=int(st.session_state.db['fixed'][k]))
        if st.button("Сохранить счета"): del st.session_state.edit_f; st.rerun()

    now = datetime.datetime.now()
    st.markdown(f'<div style="text-align:center; margin-top:30px;"><div style="color:#ff3b30; font-size:12px;">{now.strftime("%B")}</div><div style="font-size:40px;">{now.day}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with main:
    # ОБЩИЙ ОСТАТОК (от 18500)
    total_spent_fixed = sum(st.session_state.db['fixed'].values())
    current_envs_total = sum(v['b'] for v in st.session_state.db['envs'].values())
    # Считаем остаток: Зарплата - потраченное в конвертах - фиксированные
    actual_left = st.session_state.db['income'] - (sum(v['l'] - v['b'] for v in st.session_state.db['envs'].values())) - total_spent_fixed
    pct_total = int((actual_left / st.session_state.db['income']) * 100)
    
    st.markdown(f"""
        <div style="display:flex; justify-content:center; margin-bottom:40px;">
            <div style="width:130px; height:130px; border-radius:50%; background:radial-gradient(closest-side, black 86%, transparent 87% 100%), conic-gradient(#30d158 {pct_total}%, #1c1c1e 0); display:flex; align-items:center; justify-content:center; box-shadow: 0 0 30px rgba(48,209,88,0.15);">
                <div style="text-align:center;"><span style="font-size:24px; font-weight:600;">{int(actual_left)} ₪</span><br><span style="font-size:14px;color:#30d158;">{pct_total}%</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (name, d) in enumerate(st.session_state.db['envs'].items()):
        usage_pct = int((d['b'] / d['l']) * 100) if d['l'] > 0 else 0
        color = "#30d158" if usage_pct > 50 else ("#ff9f0a" if usage_pct > 20 else "#ff453a")
        with cols[i]:
            # Клик по карточке открывает историю
            if st.button(f"{name}", key=f"btn_{name}", use_container_width=True):
                st.session_state.active_h = name
            
            st.markdown(f"""
                <div class="apple-card" style="--status: {color}">
                    <div class="card-title">{name}</div>
                    <div class="card-val">{int(d['b'])} ₪</div>
                    <div class="card-pct">{usage_pct}%</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("⚙️", key=f"ed_{name}"): st.session_state.edit_cat = name

# РЕДАКТИРОВАНИЕ КОНВЕРТА
if 'edit_cat' in st.session_state:
    cat = st.session_state.edit_cat
    with st.sidebar:
        st.write(f"### Редактор: {cat}")
        new_lim = st.number_input("Новый лимит", value=int(st.session_state.db['envs'][cat]['l']))
        if st.button("Применить"):
            diff = new_lim - st.session_state.db['envs'][cat]['l']
            st.session_state.db['envs'][cat]['l'] = new_lim
            st.session_state.db['envs'][cat]['b'] += diff
            del st.session_state.edit_cat
            st.rerun()

# ИСТОРИЯ ВНУТРИ (ПОД КАРТОЧКАМИ)
if 'active_h' in st.session_state:
    cat = st.session_state.active_h
    st.markdown(f"<div class='history-text'>Последние траты {cat}:</div>", unsafe_allow_html=True)
    for log in st.session_state.db['envs'][cat]['h'][:3]:
        st.caption(f"• {log}")

# ВВОД (ТЕМНЫЙ)
st.write("---")
with st.form("input_form", clear_on_submit=True):
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: cat_choice = st.selectbox("Куда списываем?", list(st.session_state.db['envs'].keys()))
    with c2: amount = st.number_input("Сумма ₪", min_value=0, step=1, value=0)
    with c3: 
        st.write("<br>", unsafe_allow_html=True)
        if st.form_submit_button("ВНЕСТИ"):
            if amount > 0:
                st.session_state.db['envs'][cat_choice]['b'] -= amount
                st.session_state.db['envs'][cat_choice]['h'].insert(0, f"-{amount} ₪ ({datetime.datetime.now().strftime('%H:%M')})")
                st.rerun()
