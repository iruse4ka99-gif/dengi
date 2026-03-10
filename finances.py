import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

# --- 1. НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Кошелёк", layout="centered")
# Подключаем красивые иконки от Google
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">', unsafe_allow_html=True)

# Палитра: Нежные пастельные цвета для категорий
colors = {
    "Продукты и Хозтовары": "#FF9F89", "Доп. уроки": "#89E3FF", "Лео": "#FF89F6",
    "Здоровье и Аптека": "#89FF9F", "Машина": "#FFEC89", "Арина": "#FF89B2",
    "Натан": "#9F89FF", "Онлайн и Подписки": "#B289FF", "Разное": "#B0B0B0"
}

# --- 2. ДИЗАЙН (CSS) ---
st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    .block-container {{padding-top: 1rem;}}
    
    /* Три метрики в одну строку сверху */
    .kpi-row {{ display: flex; justify-content: space-between; gap: 8px; margin-bottom: 15px; }}
    .kpi-box {{ flex: 1; background: rgba(128,128,128,0.08); padding: 12px; border-radius: 14px; text-align: center; border: 1px solid rgba(0,0,0,0.03); }}
    .kpi-label {{ font-size: 10px; color: #8E8E93; text-transform: uppercase; font-weight: 600; }}
    .kpi-val {{ font-size: 17px; font-weight: 800; color: #1C1C1E; }}

    /* Стиль пастельных карточек */
    .card {{ border-radius: 18px; padding: 14px 18px; margin-bottom: 12px; border: 1px solid rgba(128,128,128,0.1); box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
    .card-row {{ display: flex; justify-content: space-between; align-items: center; }}
    .card-name {{ font-size: 15px; font-weight: 700; color: #2C2C2E; }}
    .card-amt {{ font-size: 19px; font-weight: 800; }}
    
    /* Тонкий прогресс-бар */
    .prog-bg {{ width: 100%; height: 5px; background: rgba(0,0,0,0.04); border-radius: 10px; margin: 10px 0; }}
    .prog-fill {{ height: 100%; border-radius: 10px; transition: width 0.5s ease; }}
    </style>
""", unsafe_allow_html=True)

# --- 3. ПОДКЛЮЧЕНИЕ К GOOGLE ТАБЛИЦЕ ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Читаем данные из листа "Data" (убедись, что лист в таблице называется так)
    df_gsheet = conn.read(worksheet="Data", ttl="0m")
    gsheet_data = dict(zip(df_gsheet['Category'], df_gsheet['Spent']))
except Exception as e:
    gsheet_data = {}

# --- 4. КАТЕГОРИИ И ПРАВИЛА ---
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

# Если в таблице пусто, начинаем с 0
if 'spent' not in st.session_state:
    st.session_state.spent = {cat: gsheet_data.get(cat, 0) for cat in envelopes}

# --- 5. ВЕРХНЯЯ ПАНЕЛЬ С ЦИФРАМИ ---
total_spent = sum(st.session_state.spent.values())
total_limit = sum(e['limit'] for e in envelopes.values())
rem = total_limit - total_spent

st.markdown(f"""
<div class="kpi-row">
    <div class="kpi-box"><div class="kpi-label">Лимит</div><div class="kpi-val">{total_limit}₪</div></div>
    <div class="kpi-box"><div class="kpi-label">Траты</div><div class="kpi-val" style="color:#FF3B30;">{total_spent}₪</div></div>
    <div class="kpi-box"><div class="kpi-label">Остаток</div><div class="kpi-val" style="color:#34C759;">{rem}₪</div></div>
</div>
""", unsafe_allow_html=True)

# --- 6. КОЛЬЦО И ФОРМА ВВОДА ---
c1, c2 = st.columns([1, 1.1])

with c1:
    with st.form("add_transaction", clear_on_submit=True):
        st.write("➕ **Новая трата**")
        cat_choice = st.selectbox("Куда?", list(envelopes.keys()), label_visibility="collapsed")
        amount = st.number_input("Сколько ₪", min_value=0, step=10, format="%d")
        if st.form_submit_button("ЗАПИСАТЬ", use_container_width=True, type="primary") and amount > 0:
            st.session_state.spent[cat_choice] += amount
            try:
                # Отправляем обновленные данные в Google Таблицу
                new_df = pd.DataFrame([{'Category': k, 'Spent': v} for k,v in st.session_state.spent.items()])
                conn.update(worksheet="Data", data=new_df)
            except: pass
            st.rerun()

with c2:
    # Данные для диаграммы (только те, где траты > 0)
    df_chart = pd.DataFrame([{"c": k, "v": v} for k, v in st.session_state.spent.items() if v > 0])
    today_str = date.today().strftime("%d.%m")
    
    # Рисуем кольцо
    fig = px.pie(df_chart if not df_chart.empty else pd.DataFrame([{"c":"-","v":1}]), 
                 values='v', names='c', hole=0.65, 
                 color='c', color_discrete_map=colors if not df_chart.empty else {"-":"#F2F2F7"})
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=170)
    fig.update_traces(textinfo='none', hovertemplate=None)
    # Добавляем дату и сумму в центр
    fig.add_annotation(text=f"<span style='font-size:13px; color:#8E8E93;'>{today_str}</span><br><b style='font-size:18px;'>{total_spent}₪</b>", 
                       x=0.5, y=0.5, showarrow=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()

# --- 7. ПАСТЕЛЬНЫЕ КАРТОЧКИ КАТЕГОРИЙ ---
for name, info in envelopes.items():
    spent_val = st.session_state.spent[name]
    limit_val = info['limit']
    percentage = min(int((spent_val / limit_val) * 100), 100) if limit_val > 0 else 0
    main_color = colors.get(name, "#8e8e93")
    
    st.markdown(f"""
    <div class="card" style="background: {main_color}1F;">
        <div class="card-row">
            <div style="display:flex; align-items:center; gap:10px;">
                <span class="material-symbols-outlined" style="color:{main_color}; font-size:24px;">{info['icon']}</span>
                <span class="card-name">{name}</span>
            </div>
            <div class="card-amt" style="color:{main_color if spent_val > 0 else '#C7C7CC'};">-{spent_val}₪</div>
        </div>
        <div class="prog-bg"><div class="prog-fill" style="width:{percentage}%; background:{main_color};"></div></div>
        <div style="display:flex; justify-content:space-between; font-size:11px; color:#8E8E93; font-weight:500;">
            <span>{percentage}% потрачено</span>
            <span>Свободно {limit_val - spent_val}₪</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
