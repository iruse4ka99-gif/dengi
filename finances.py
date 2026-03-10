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
    "Натан": "#9F89FF", "Онлайн и Подписки": "#B289FF", "Разное": "#B0B0B0",
    "Счета": "#D1D1D6"
}

# --- 2. LIQUID GLASS CSS ---
st.markdown(f"""
    <style>
    #MainMenu {{ visibility: hidden; }} footer {{ visibility: hidden; }} header {{ visibility: hidden; }}
    .stApp {{ background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); }}

    .top-metrics {{ display: flex; justify-content: space-around; margin-top: -30px; margin-bottom: 25px; }}
    .m-item {{ text-align: center; }}
    .m-label {{ font-size: 11px; color: #6e6e73; text-transform: uppercase; font-weight: 700; }}
    .m-val {{ font-size: 22px; font-weight: 800; color: #1d1d1f; }}

    .glass-card {{
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 30px; padding: 24px; margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.08);
    }}
    .rem-main {{ font-size: 28px; font-weight: 900; color: #1d1d1f; }}
    .p-bar-bg {{ width: 100%; height: 7px; background: rgba(0,0,0,0.04); border-radius: 10px; margin: 15px 0; }}
    .p-bar-fill {{ height: 100%; border-radius: 10px; transition: width 0.8s ease; }}

    .bottom-nav {{
        position: fixed; bottom: 0; left: 0; right: 0;
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(25px);
        display: flex; justify-content: space-around;
        padding: 15px 10px 35px 10px;
        border-top: 1px solid rgba(255, 255, 255, 0.3);
        z-index: 1000;
    }}
    .main-content {{ padding-bottom: 120px; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA & CONNECTION ---
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
fixed_bills = ["Аренда", "Арнона", "Электричество", "Вода", "Газ", "Интернет", "Страховки"]

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_raw = conn.read(worksheet="Data", ttl="0m")
    # Принудительно заполняем отсутствующие категории нулями
    full_cats = list(envelopes.keys()) + fixed_bills
    gsheet_spent = {c: 0.0 for c in full_cats}
    gsheet_carry = {c: 0.0 for c in full_cats}
    for _, row in df_raw.iterrows():
        cat = str(row['Category'])
        if cat in gsheet_spent:
            gsheet_spent[cat] = float(row['Spent'])
            gsheet_carry[cat] = float(row['Carryover'])
except:
    gsheet_spent = {k: 0.0 for k in list(envelopes.keys()) + fixed_bills}
    gsheet_carry = {k: 0.0 for k in list(envelopes.keys()) + fixed_bills}

if 'spent' not in st.session_state: st.session_state.spent = gsheet_spent
if 'carry' not in st.session_state: st.session_state.carry = gsheet_carry
if 'page' not in st.session_state: st.session_state.page = "wallet"

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# --- 4. NAVIGATION ---
if st.session_state.page == "wallet":
    total_l = sum(e['limit'] for e in envelopes.values()) + sum(st.session_state.carry.get(k,0) for k in envelopes)
    total_s = sum(st.session_state.spent.get(k,0) for k in envelopes)
    total_r = total_l - total_s

    st.markdown(f"""
    <div class="top-metrics">
        <div class="m-item"><div class="m-label">Лимит</div><div class="m-val">{total_l}₪</div></div>
        <div class="m-item"><div class="m-label">Траты</div><div class="m-val" style="color:#ff3b30;">{total_s}₪</div></div>
        <div class="m-item"><div class="m-label">Остаток</div><div class="m-val" style="color:#34c759;">{total_r}₪</div></div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("➕ Новая трата"):
        with st.form("add_form", clear_on_submit=True):
            target = st.selectbox("Куда?", list(envelopes.keys()) + fixed_bills)
            val = st.number_input("Сколько ₪", min_value=0.0, step=10.0)
            if st.form_submit_button("ЗАПИСАТЬ"):
                st.session_state.spent[target] += val
                all_cats = list(envelopes.keys()) + fixed_bills
                upd_data = pd.DataFrame([{'Category': k, 'Spent': float(st.session_state.spent[k]), 'Carryover': float(st.session_state.carry[k])} for k in all_cats])
                conn.update(worksheet="Data", data=upd_data)
                st.rerun()

    st.write("🗓 **Фиксированные счета**")
    f_cols = st.columns(2)
    for i, f_n in enumerate(fixed_bills):
        with f_cols[i % 2]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.2); padding:10px; border-radius:15px; margin-bottom:8px; border:1px solid rgba(255,255,255,0.3);">
                <span style="font-size:10px; color:#86868b;">{f_n}</span><br><b>{st.session_state.spent.get(f_n,0)}₪</b>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.write("👛 **Ежедневные конверты**")
    for name, info in envelopes.items():
        s, c = st.session_state.spent.get(name,0), st.session_state.carry.get(name,0)
        lim = info['limit'] + c
        rem = lim - s
        p = min(int((s / lim) * 100), 100) if lim > 0 else 100
        clr = colors.get(name, "#8e8e93")

        st.markdown(f"""
        <div class="glass-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span class="material-symbols-outlined" style="color:{clr}; font-size:35px;">{info['icon']}</span>
                    <span style="font-size:18px; font-weight:700;">{name}</span>
                </div>
                <div style="text-align:right;">
                    <div class="m-label" style="font-size:9px;">Осталось</div>
                    <div class="rem-main" style="color:{'#34c759' if rem >= 0 else '#ff3b30'};">{rem}₪</div>
                </div>
            </div>
            <div class="p-bar-bg"><div class="p-bar-fill" style="width:{p}%; background:{clr}; box-shadow: 0 0 12px {clr}44;"></div></div>
            <div style="font-size:11px; color:#86868b;">Траты: {s}₪ | Порог: {lim}₪ (Копилка: {c}₪)</div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == "transfer":
    st.subheader("🔁 Перевод")
    with st.form("tr_form"):
        f_cat, t_cat = st.selectbox("Откуда?", list(envelopes.keys())), st.selectbox("Куда?", list(envelopes.keys()))
        v_tr = st.number_input("Сумма ₪", min_value=1.0)
        if st.form_submit_button("ПЕРЕВЕСТИ"):
            st.session_state.carry[f_cat] -= v_tr
            st.session_state.carry[t_cat] += v_tr
            all_cats = list(envelopes.keys()) + fixed_bills
            u_df = pd.DataFrame([{'Category': k, 'Spent': float(st.session_state.spent[k]), 'Carryover': float(st.session_state.carry[k])} for k in all_cats])
            conn.update(worksheet="Data", data=u_df)
            st.success("Готово!")

elif st.session_state.page == "history":
    st.subheader("📜 История")
    if st.button("🏁 ЗАКРЫТЬ МЕСЯЦ"):
        all_cats = list(envelopes.keys()) + fixed_bills
        new_c = {k: (envelopes[k]['limit'] if k in envelopes else 0) + st.session_state.carry.get(k,0) - st.session_state.spent.get(k,0) for k in all_cats}
        f_df = pd.DataFrame([{'Category': k, 'Spent': 0.0, 'Carryover': float(new_c[k])} for k in all_cats])
        conn.update(worksheet="Data", data=f_df)
        st.balloons(); st.rerun()
    st.dataframe(df_raw, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 5. BOTTOM NAVIGATION ---
st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("💎 Кошелёк", use_container_width=True): st.session_state.page = "wallet"; st.rerun()
with c2:
    if st.button("🔁 Перевод", use_container_width=True): st.session_state.page = "transfer"; st.rerun()
with c3:
    if st.button("📜 История", use_container_width=True): st.session_state.page = "history"; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
