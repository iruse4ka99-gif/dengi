import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

# --- 1. НАСТРОЙКИ ---
st.set_page_config(page_title="Кошелёк", layout="centered")
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">', unsafe_allow_html=True)

# Пастельная палитра
colors = {
    "Продукты и Хозтовары": "#FF9F89", "Доп. уроки": "#89E3FF", "Лео": "#FF89F6",
    "Здоровье и Аптека": "#89FF9F", "Машина": "#FFEC89", "Арина": "#FF89B2",
    "Натан": "#9F89FF", "Онлайн и Подписки": "#B289FF", "Разное": "#B0B0B0"
}

# --- 2. СТИЛЬ "ЖИДКОЕ СТЕКЛО" (Glassmorphism) ---
st.markdown(f"""
    <style>
    /* Прячем лишнее */
    #MainMenu {{ visibility: hidden; }} footer {{ visibility: hidden; }} header {{ visibility: hidden; }}
    
    /* Фон страницы (мягкий градиент) */
    .stApp {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }}

    /* Стеклянные метрики сверху */
    .glass-metrics {{
        display: flex; justify-content: space-around;
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }}
    .m-item {{ text-align: center; }}
    .m-label {{ font-size: 10px; color: #666; text-transform: uppercase; letter-spacing: 1px; }}
    .m-val {{ font-size: 18px; font-weight: 800; color: #333; }}

    /* Стеклянные карточки конвертов */
    .glass-card {{
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.7);
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .card-head {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
    .cat-name {{ font-size: 16px; font-weight: 700; color: #444; }}
    .rem-val {{ font-size: 20px; font-weight: 900; color: #1C1C1E; }}
    .rem-label {{ font-size: 9px; color: #888; text-align: right; text-transform: uppercase; }}

    /* Прогресс-бар */
    .p-bg {{ width: 100%; height: 6px; background: rgba(0,0,0,0.05); border-radius: 10px; margin: 10px 0; }}
    .p-fill {{ height: 100%; border-radius: 10px; transition: width 0.6s ease-in-out; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. ДАННЫЕ ---
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
    gsheet_carryover = dict(zip(df['Category'], df['Carryover']))
except:
    gsheet_spent = {cat: 0 for cat in envelopes}
    gsheet_carryover = {cat: 0 for cat in envelopes}

if 'spent' not in st.session_state: st.session_state.spent = gsheet_spent
if 'carryover' not in st.session_state: st.session_state.carryover = gsheet_carryover

# --- 4. НАВИГАЦИЯ (Вкладки) ---
tab1, tab2, tab3 = st.tabs(["💎 Кошелёк", "🔁 Перевод", "📜 История"])

# --- ВКЛАДКА 1: ГЛАВНАЯ ---
with tab1:
    total_l = sum(e['limit'] for e in envelopes.values()) + sum(st.session_state.carryover.values())
    total_s = sum(st.session_state.spent.values())
    total_r = total_l - total_s

    # Жидкие метрики
    st.markdown(f"""
    <div class="glass-metrics">
        <div class="m-item"><div class="m-label">Лимит</div><div class="m-val">{total_l}₪</div></div>
        <div class="m-item"><div class="m-label">Траты</div><div class="m-val" style="color:#FF4B4B;">{total_s}₪</div></div>
        <div class="m-item"><div class="m-label">Остаток</div><div class="m-val" style="color:#2ECC71;">{total_r}₪</div></div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.2])
    with c1:
        with st.form("quick_add", clear_on_submit=True):
            cat = st.selectbox("Куда?", list(envelopes.keys()))
            val = st.number_input("Сколько ₪", min_value=0, step=10)
            if st.form_submit_button("ЗАПИСАТЬ", use_container_width=True):
                st.session_state.spent[cat] += val
                new_df = pd.DataFrame([{'Category': k, 'Spent': st.session_state.spent[k], 'Carryover': st.session_state.carryover[k]} for k in envelopes])
                conn.update(worksheet="Data", data=new_df)
                st.rerun()
    
    with c2:
        chart_df = pd.DataFrame([{"c": k, "v": v} for k, v in st.session_state.spent.items() if v > 0])
        fig = px.pie(chart_df if not chart_df.empty else pd.DataFrame([{"c":"-","v":1}]), 
                     values='v', names='c', hole=0.75, color='c', color_discrete_map=colors if not chart_df.empty else {"-":"#EEE"})
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=160, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        fig.add_annotation(text=f"<b>{date.today().strftime('%d.%m')}</b>", x=0.5, y=0.5, showarrow=False, font_size=14)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Карточки конвертов
    for name, info in envelopes.items():
        spent = st.session_state.spent[name]
        carry = st.session_state.carryover[name]
        limit = info['limit'] + carry
        rem = limit - spent
        perc = min(int((spent / limit) * 100), 100) if limit > 0 else 100
        clr = colors.get(name, "#888")

        st.markdown(f"""
        <div class="glass-card">
            <div class="card-head">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span class="material-symbols-outlined" style="color:{clr}; font-size:28px;">{info['icon']}</span>
                    <span class="cat-name">{name}</span>
                </div>
                <div>
                    <div class="rem-label">Осталось</div>
                    <div class="rem-val" style="color:{'#2ECC71' if rem >= 0 else '#FF4B4B'};">{rem}₪</div>
                </div>
            </div>
            <div class="p-bg"><div class="p-fill" style="width:{perc}%; background:{clr}; box-shadow: 0 0 10px {clr}66;"></div></div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#777;">
                <span>Потрачено: {spent}₪</span>
                <span>Лимит: {limit}₪</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- ВКЛАДКА 2: ПЕРЕВОД ---
with tab2:
    st.subheader("🔁 Перебросить деньги")
    st.info("Если в одном конверте минус, а в другом остались деньги — можно их перевести.")
    with st.form("transfer_form"):
        col1, col2 = st.columns(2)
        with col1: from_cat = st.selectbox("Откуда забрать?", list(envelopes.keys()))
        with col2: to_cat = st.selectbox("Куда добавить?", list(envelopes.keys()))
        t_amt = st.number_input("Сумма перевода ₪", min_value=1, step=5)
        
        if st.form_submit_button("ВЫПОЛНИТЬ ПЕРЕВОД", use_container_width=True):
            # Перевод работает через Carryover (Копилку)
            st.session_state.carryover[from_cat] -= t_amt
            st.session_state.carryover[to_cat] += t_amt
            new_df = pd.DataFrame([{'Category': k, 'Spent': st.session_state.spent[k], 'Carryover': st.session_state.carryover[k]} for k in envelopes])
            conn.update(worksheet="Data", data=new_df)
            st.success(f"Перевели {t_amt}₪ из {from_cat} в {to_cat}")
            st.rerun()

# --- ВКЛАДКА 3: ИСТОРИЯ И ЗАКРЫТИЕ ---
with tab3:
    st.subheader("📜 Управление месяцем")
    if st.button("🏁 ЗАКРЫТЬ МЕСЯЦ И СОХРАНИТЬ КОПИЛКУ", use_container_width=True):
        new_c = {}
        for n, i in envelopes.items():
            new_c[n] = (i['limit'] + st.session_state.carryover[n]) - st.session_state.spent[n]
        
        final_df = pd.DataFrame([{'Category': k, 'Spent': 0, 'Carryover': new_c[k]} for k in envelopes])
        conn.update(worksheet="Data", data=final_df)
        st.balloons()
        st.success("Все остатки перенесены в копилку, траты обнулены!")
        st.rerun()

    st.divider()
    st.write("📊 Твоя текущая таблица (сырые данные):")
    st.dataframe(df, use_container_width=True)
