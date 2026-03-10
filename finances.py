import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

# --- 1. НАСТРОЙКИ ---
st.set_page_config(page_title="Мой Кошелёк", layout="centered")
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">', unsafe_allow_html=True)

# Палитра
colors = {
    "Продукты и Хозтовары": "#FF9F89", "Доп. уроки": "#89E3FF", "Лео": "#FF89F6",
    "Здоровье и Аптека": "#89FF9F", "Машина": "#FFEC89", "Арина": "#FF89B2",
    "Натан": "#9F89FF", "Онлайн и Подписки": "#B289FF", "Разное": "#B0B0B0"
}

# --- 2. СТИЛЬ "ЖИДКОЕ СТЕКЛО" ---
st.markdown(f"""
    <style>
    #MainMenu {{ visibility: hidden; }} footer {{ visibility: hidden; }} header {{ visibility: hidden; }}
    .stApp {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }}
    /* Стеклянные метрики */
    .glass-metrics {{
        display: flex; justify-content: space-around;
        background: rgba(255, 255, 255, 0.35);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    }}
    .m-item {{ text-align: center; }}
    .m-label {{ font-size: 11px; color: #777; text-transform: uppercase; font-weight: 600; }}
    .m-val {{ font-size: 20px; font-weight: 900; color: #222; }}

    /* Стеклянные карточки */
    .glass-card {{
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 28px;
        padding: 22px;
        margin-bottom: 18px;
        border: 1px solid rgba(255, 255, 255, 0.6);
    }}
    .card-top {{ display: flex; justify-content: space-between; align-items: center; }}
    .cat-title {{ font-size: 16px; font-weight: 700; color: #333; }}
    .rem-huge {{ font-size: 24px; font-weight: 900; letter-spacing: -1px; }}
    .rem-sub {{ font-size: 9px; color: #888; text-transform: uppercase; text-align: right; }}

    .p-bar-bg {{ width: 100%; height: 8px; background: rgba(0,0,0,0.05); border-radius: 10px; margin: 12px 0; }}
    .p-bar-fill {{ height: 100%; border-radius: 10px; transition: width 0.8s ease; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. ПОДКЛЮЧЕНИЕ ---
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

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Data", ttl="0m")
    gsheet_spent = dict(zip(df['Category'], df['Spent']))
    gsheet_carry = dict(zip(df['Category'], df['Carryover']))
except:
    gsheet_spent = {k: 0 for k in envelopes}
    gsheet_carry = {k: 0 for k in envelopes}

if 'spent' not in st.session_state: st.session_state.spent = gsheet_spent
if 'carry' not in st.session_state: st.session_state.carry = gsheet_carry

# --- 4. ВКЛАДКИ ---
tab_home, tab_move, tab_hist = st.tabs(["💎 Кошелёк", "🔁 Перевод", "📜 История"])

with tab_home:
    total_l = sum(e['limit'] for e in envelopes.values()) + sum(st.session_state.carry.values())
    total_s = sum(st.session_state.spent.values())
    total_r = total_l - total_s

    # Жидкие метрики без домиков
    st.markdown(f"""
    <div class="glass-metrics">
        <div class="m-item"><div class="m-label">Лимит</div><div class="m-val">{total_l}₪</div></div>
        <div class="m-item"><div class="m-label">Траты</div><div class="m-val" style="color:#FF5252;">{total_s}₪</div></div>
        <div class="m-item"><div class="m-label">Остаток</div><div class="m-val" style="color:#27AE60;">{total_r}₪</div></div>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_chart = st.columns([1, 1.2])
    with col_input:
        with st.form("add_exp", clear_on_submit=True):
            target = st.selectbox("Куда?", list(envelopes.keys()))
            sum_val = st.number_input("Сколько ₪", min_value=0, step=10)
            if st.form_submit_button("ЗАПИСАТЬ", use_container_width=True):
                st.session_state.spent[target] += sum_val
                new_df = pd.DataFrame([{'Category': k, 'Spent': st.session_state.spent[k], 'Carryover': st.session_state.carry[k]} for k in envelopes])
                conn.update(worksheet="Data", data=new_df)
                st.rerun()

    with col_chart:
        active_data = pd.DataFrame([{"c": k, "v": v} for k, v in st.session_state.spent.items() if v > 0])
        fig = px.pie(active_data if not active_data.empty else pd.DataFrame([{"c":"-","v":1}]), 
                     values='v', names='c', hole=0.75, color='c', color_discrete_map=colors if not active_data.empty else {"-":"#eee"})
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=160, paper_bgcolor='rgba(0,0,0,0)')
        fig.add_annotation(text=f"<b>{date.today().strftime('%d.%m')}</b>", x=0.5, y=0.5, showarrow=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Карточки конвертов
    for name, info in envelopes.items():
        s = st.session_state.spent[name]
        c = st.session_state.carry[name]
        lim = info['limit'] + c
        rem = lim - s
        p = min(int((s / lim) * 100), 100) if lim > 0 else 100
        clr = colors.get(name, "#888")

        st.markdown(f"""
        <div class="glass-card">
            <div class="card-top">
                <div style="display:flex; align-items:center; gap:12px;">
                    <span class="material-symbols-outlined" style="color:{clr}; font-size:32px;">{info['icon']}</span>
                    <span class="cat-title">{name}</span>
                </div>
                <div>
                    <div class="rem-sub">Осталось</div>
                    <div class="rem-huge" style="color:{'#27AE60' if rem >= 0 else '#FF5252'};">{rem}₪</div>
                </div>
            </div>
            <div class="p-bar-bg"><div class="p-bar-fill" style="width:{p}%; background:{clr}; box-shadow: 0 0 15px {clr}44;"></div></div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#666; font-weight:500;">
                <span>Потрачено: {s}₪</span>
                <span>Лимит месяца: {info['limit']}₪ ({" " if c < 0 else "+"}{c} в копилке)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab_move:
    st.subheader("🔁 Перебросить деньги")
    st.info("Закончились деньги в одном конверте? Перенеси из другого!")
    with st.form("transfer"):
        f_cat = st.selectbox("Откуда забрать?", list(envelopes.keys()))
        t_cat = st.selectbox("Куда добавить?", list(envelopes.keys()))
        t_sum = st.number_input("Сумма перевода ₪", min_value=1, step=5)
        if st.form_submit_button("ВЫПОЛНИТЬ ПЕРЕВОД", use_container_width=True):
            st.session_state.carry[f_cat] -= t_sum
            st.session_state.carry[t_cat] += t_sum
            upd_df = pd.DataFrame([{'Category': k, 'Spent': st.session_state.spent[k], 'Carryover': st.session_state.carry[k]} for k in envelopes])
            conn.update(worksheet="Data", data=upd_df)
            st.success(f"Готово! Перевели {t_sum}₪ из {f_cat} в {t_cat}")
            st.rerun()

with tab_hist:
    st.subheader("📜 Управление периодом")
    if st.button("🏁 ЗАКРЫТЬ МЕСЯЦ И СОХРАНИТЬ ОСТАТКИ", use_container_width=True):
        new_c = {n: (info['limit'] + st.session_state.carry[n]) - st.session_state.spent[n] for n, info in envelopes.items()}
        final_df = pd.DataFrame([{'Category': k, 'Spent': 0, 'Carryover': new_c[k]} for k in envelopes])
        conn.update(worksheet="Data", data=final_df)
        st.balloons()
        st.success("Месяц закрыт. Все остатки ушли в копилку!")
        st.rerun()
    st.divider()
    st.write("📊 Текущие данные в таблице:")
    st.dataframe(df, use_container_width=True)
