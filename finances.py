import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

# --- 1. CONFIG ---
st.set_page_config(page_title="My Wallet", layout="centered")
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">', unsafe_allow_html=True)

# Apple-style pastel palette
colors = {
    "Продукты и Хозтовары": "#FF9F89", "Доп. уроки": "#89E3FF", "Лео": "#FF89F6",
    "Здоровье и Аптека": "#89FF9F", "Машина": "#FFEC89", "Арина": "#FF89B2",
    "Натан": "#9F89FF", "Онлайн и Подписки": "#B289FF", "Разное": "#B0B0B0"
}

# --- 2. LIQUID GLASS CSS ---
st.markdown(f"""
    <style>
    #MainMenu {{ visibility: hidden; }} footer {{ visibility: hidden; }} header {{ visibility: hidden; }}
    .stApp {{ background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); }}

    /* Прозрачные метрики сверху */
    .top-metrics {{
        display: flex; justify-content: space-around; margin-bottom: 25px;
        background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px);
        border-radius: 20px; padding: 15px; border: 1px solid rgba(255, 255, 255, 0.4);
    }}
    .m-item {{ text-align: center; }}
    .m-label {{ font-size: 11px; color: #6e6e73; text-transform: uppercase; font-weight: 600; }}
    .m-val {{ font-size: 20px; font-weight: 700; color: #1d1d1f; }}

    /* Карточки Liquid Glass */
    .glass-card {{
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border-radius: 30px; padding: 25px; margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.45);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.08);
    }}
    .rem-main {{ font-size: 30px; font-weight: 800; color: #1d1d1f; letter-spacing: -1.5px; }}
    .rem-label {{ font-size: 10px; color: #6e6e73; text-transform: uppercase; text-align: right; }}

    .p-bar-bg {{ width: 100%; height: 7px; background: rgba(0,0,0,0.06); border-radius: 10px; margin: 15px 0; }}
    .p-bar-fill {{ height: 100%; border-radius: 10px; transition: width 0.8s ease-in-out; }}

    /* ПРИЖИМАЕМ КНОПКИ К НИЗУ (Меню) */
    div[data-testid="stHorizontalBlock"]:last-child {{
        position: fixed; bottom: 0; left: 0; right: 0;
        background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(20px);
        padding: 15px 10px 30px 10px; z-index: 1000;
        border-top: 1px solid rgba(255, 255, 255, 0.3);
    }}
    .main-content {{ padding-bottom: 110px; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. CONNECTION & DATA ---
envelopes = {
    "Продукты и Хозтовары": {"limit": 4000, "icon": "shopping_cart"},
    "Доп. уроки": {"limit": 2254, "icon": "menu_book"},
    "Лео": {"limit": 1000, "icon": "child_care"},
    "Здоровье и Аптека": {"limit": 500, "icon": "medical_services"},
    "Машина": {"limit": 350, "icon": "directions_car"},
    "Арина": {"limit": 100, "icon": "person"},
    "Натан": {"limit": 100, "icon": "person"},
    "Онлайн и Подписки": {"limit": 100, "icon": "devices"},
    "Разное": {"limit": 100, "icon": "more_horiz"}
}

# Инициализируем df заранее, чтобы не было ошибок NameError
df = pd.DataFrame() 

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Data", ttl="0m")
    gsheet_spent = dict(zip(df['Category'], df['Spent']))
    gsheet_carry = dict(zip(df['Category'], df['Carryover']))
except Exception as e:
    gsheet_spent = {k: 0 for k in envelopes}
    gsheet_carry = {k: 0 for k in envelopes}

if 'spent' not in st.session_state: st.session_state.spent = gsheet_spent
if 'carry' not in st.session_state: st.session_state.carry = gsheet_carry
if 'page' not in st.session_state: st.session_state.page = "wallet"

# --- 4. NAVIGATION LOGIC ---
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if st.session_state.page == "wallet":
    total_l = sum(e['limit'] for e in envelopes.values()) + sum(st.session_state.carry.values())
    total_s = sum(st.session_state.spent.values())
    total_r = total_l - total_s

    st.markdown(f"""
    <div class="top-metrics">
        <div class="m-item"><div class="m-label">Лимит</div><div class="m-val">{total_l}₪</div></div>
        <div class="m-item"><div class="m-label">Траты</div><div class="m-val" style="color:#ff3b30;">{total_s}₪</div></div>
        <div class="m-item"><div class="m-label">Остаток</div><div class="m-val" style="color:#34c759;">{total_r}₪</div></div>
    </div>
    """, unsafe_allow_html=True)

    c_f, c_p = st.columns([1, 1.2])
    with c_f:
        with st.form("add", clear_on_submit=True):
            cat_choice = st.selectbox("Куда?", list(envelopes.keys()), label_visibility="collapsed")
            amt = st.number_input("Сколько ₪", min_value=0, step=10)
            if st.form_submit_button("ЗАПИСАТЬ", use_container_width=True):
                st.session_state.spent[cat_choice] += amt
                new_df = pd.DataFrame([{'Category': k, 'Spent': float(st.session_state.spent[k]), 'Carryover': float(st.session_state.carry[k])} for k in envelopes])
                conn.update(worksheet="Data", data=new_df)
                st.rerun()
    with c_p:
        active_df = pd.DataFrame([{"c": k, "v": v} for k, v in st.session_state.spent.items() if v > 0])
        fig = px.pie(active_df if not active_df.empty else pd.DataFrame([{"c":"-","v":1}]), 
                     values='v', names='c', hole=0.82, color='c', 
                     color_discrete_map=colors if not active_df.empty else {"-":"#f2f2f7"})
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=130, paper_bgcolor='rgba(0,0,0,0)')
        fig.add_annotation(text=f"<b>{date.today().strftime('%d.%m')}</b>", x=0.5, y=0.5, showarrow=False, font_size=14)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.divider()

    for name, info in envelopes.items():
        s = st.session_state.spent[name]
        c = st.session_state.carry[name]
        lim = info['limit'] + c
        rem = lim - s
        p = min(int((s / lim) * 100), 100) if lim > 0 else 100
        clr = colors.get(name, "#8e8e93")

        st.markdown(f"""
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div style="display:flex; align-items:center; gap:15px;">
                    <span class="material-symbols-outlined" style="color:{clr}; font-size:40px;">{info['icon']}</span>
                    <span style="font-size:19px; font-weight:700; color:#1d1d1f;">{name}</span>
                </div>
                <div>
                    <div class="rem-label">Осталось</div>
                    <div class="rem-main" style="color:{'#34c759' if rem >= 0 else '#ff3b30'};">{rem}₪</div>
                </div>
            </div>
            <div class="p-bar-bg"><div class="p-bar-fill" style="width:{p}%; background:{clr}; box-shadow: 0 0 15px {clr}66;"></div></div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#6e6e73; font-weight:600;">
                <span>Траты: {s}₪</span>
                <span>Лимит: {lim}₪ ({" " if c < 0 else "+"}{c} копилка)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == "transfer":
    st.subheader("🔁 Перевод")
    with st.form("transfer"):
        f = st.selectbox("Откуда?", list(envelopes.keys()))
        t = st.selectbox("Куда?", list(envelopes.keys()))
        v = st.number_input("Сумма ₪", min_value=1)
        if st.form_submit_button("ВЫПОЛНИТЬ"):
            st.session_state.carry[f] -= v
            st.session_state.carry[t] += v
            u_df = pd.DataFrame([{'Category': k, 'Spent': float(st.session_state.spent[k]), 'Carryover': float(st.session_state.carry[k])} for k in envelopes])
            conn.update(worksheet="Data", data=u_df)
            st.success("Готово!")
            st.rerun()

elif st.session_state.page == "history":
    st.subheader("📜 История")
    if st.button("🏁 ЗАКРЫТЬ МЕСЯЦ"):
        new_c = {n: (info['limit'] + st.session_state.carry[n]) - st.session_state.spent[n] for n, info in envelopes.items()}
        f_df = pd.DataFrame([{'Category': k, 'Spent': 0.0, 'Carryover': float(new_c[k])} for k in envelopes])
        conn.update(worksheet="Data", data=f_df)
        st.balloons(); st.rerun()
    st.divider()
    if not df.empty: st.dataframe(df, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 5. BOTTOM NAVIGATION BAR (В самом низу) ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("💎 Кошелёк", use_container_width=True): st.session_state.page = "wallet"; st.rerun()
with c2:
    if st.button("🔁 Перевод", use_container_width=True): st.session_state.page = "transfer"; st.rerun()
with c3:
    if st.button("📜 История", use_container_width=True): st.session_state.page = "history"; st.rerun()
