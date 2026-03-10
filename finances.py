import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

# --- 1. НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Кошелёк", page_icon="💳", layout="centered")

# Подключаем иконки
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">', unsafe_allow_html=True)

# --- 2. ЦВЕТОВАЯ ГАММА ---
# Те же сочные цвета, но теперь они будут и в фоне карточек
rich_colors = {
    "Продукты и Хозтовары": "#FF5733",
    "Доп. уроки": "#33CFFF",
    "Лео": "#FF33F6",
    "Здоровье и Аптека": "#33FF57",
    "Машина": "#FFD700", # Золотистый
    "Арина": "#FF3383",
    "Натан": "#5733FF",
    "Онлайн и Подписки": "#8333FF",
    "Разное": "#6C757D"
}

# --- 3. ПРЕМИУМ ДИЗАЙН (CSS) ---
st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
    .block-container {{padding-top: 1rem; padding-bottom: 2rem;}}
    
    .kpi-container {{
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(128, 128, 128, 0.1); border-radius: 12px; padding: 10px 15px; margin-bottom: 15px;
    }}
    .kpi-item {{ text-align: center; flex: 1; }}
    .kpi-value {{ font-size: 18px; font-weight: 800; }}

    /* ПАСТЕЛЬНЫЕ КАРТОЧКИ */
    .envelope-card {{
        border-radius: 16px; padding: 12px 16px; margin-bottom: 12px;
        border: 1px solid rgba(128, 128, 128, 0.1);
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }}
    
    .env-row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
    .env-name {{ font-size: 16px; font-weight: 700; }}
    .env-spent {{ font-size: 20px; font-weight: 800; }}
    
    .custom-progress-bg {{ width: 100%; height: 6px; background: rgba(0, 0, 0, 0.1); border-radius: 10px; }}
    .custom-progress-fill {{ height: 100%; border-radius: 10px; transition: width 0.4s ease; }}
    .env-footer {{ font-size: 12px; color: #666; margin-top: 5px; font-weight: 500; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. ПОДКЛЮЧЕНИЕ К ГУГЛ ТАБЛИЦЕ ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Читаем данные. worksheet="Data" - убедись, что лист в таблице называется именно так!
    df_gsheet = conn.read(worksheet="Data", ttl="0m")
    # Допустим, в таблице две колонки: Category и Spent
    gsheet_data = dict(zip(df_gsheet['Category'], df_gsheet['Spent']))
except:
    gsheet_data = {{}}

# --- 5. ЛОГИКА ДАННЫХ ---
envelopes = {{
    "Продукты и Хозтовары": {{"limit": 4000, "icon": "shopping_cart"}},
    "Доп. уроки": {{"limit": 2254, "icon": "menu_book"}},
    "Лео": {{"limit": 1000, "icon": "child_care"}},
    "Здоровье и Аптека": {{"limit": 500, "icon": "medical_services"}},
    "Машина": {{"limit": 350, "icon": "directions_car"}},
    "Арина": {{"limit": 100, "icon": "person"}},
    "Натан": {{"limit": 100, "icon": "person"}},
    "Онлайн и Подписки": {{"limit": 100, "icon": "devices"}},
    "Разное": {{"limit": 100, "icon": "more_horiz"}}
}}

if 'spent_data' not in st.session_state:
    # Приоритет данным из Google Таблицы, если их нет - ставим 0
    st.session_state.spent_data = {{cat: gsheet_data.get(cat, 0) for cat in envelopes}}
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 6. ШАПКА ---
total_limit = sum(e['limit'] for e in envelopes.values())
total_spent = sum(st.session_state.spent_data.values())
remaining = total_limit - total_spent

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-item"><div class="kpi-value">{total_limit} ₪</div></div>
    <div class="kpi-item" style="border-left:1px solid #ccc; border-right:1px solid #ccc;"><div class="kpi-value" style="color:#ff3b30;">{total_spent} ₪</div></div>
    <div class="kpi-item"><div class="kpi-value" style="color:#34c759;">{remaining} ₪</div></div>
</div>
""", unsafe_allow_html=True)

# --- 7. КОЛЬЦО (ШИРЕ + ДАТА) ---
col_in, col_ch = st.columns([1, 1])

with col_in:
    with st.form("add_exp", clear_on_submit=True):
        st.write("➕ **Новая трата**")
        cat_select = st.selectbox("Категория", list(envelopes.keys()), label_visibility="collapsed")
        amt_input = st.number_input("Сумма", min_value=0, step=10, format="%d")
        if st.form_submit_button("Записать", use_container_width=True, type="primary"):
            if amt_input > 0:
                st.session_state.spent_data[cat_select] += amt_input
                st.session_state.history.insert(0, f"➖ {{cat_select}}: {{amt_input}} ₪")
                # Обновляем таблицу (если подключена)
                try:
                    new_df = pd.DataFrame([{{'Category': k, 'Spent': v}} for k,v in st.session_state.spent_data.items()])
                    conn.update(worksheet="Data", data=new_df)
                except: pass
                st.rerun()

with col_ch:
    df_chart = pd.DataFrame([{"cat": k, "val": v} for k, v in st.session_state.spent_data.items() if v > 0])
    today_str = date.today().strftime("%d.%m")
    
    if not df_chart.empty:
        # hole=0.7 делает кольцо шире
        fig = px.pie(df_chart, values='val', names='cat', hole=0.7, 
                     color='cat', color_discrete_map=rich_colors)
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=200)
        fig.update_traces(textinfo='none')
        # Дата и сумма в центре
        fig.add_annotation(text=f"<span style='font-size:14px; color:grey;'>{{today_str}}</span><br><b>{{total_spent}} ₪</b>", 
                           x=0.5, y=0.5, showarrow=False)
        st.plotly_chart(fig, use_container_width=True, config={{'displayModeBar': False}})
    else:
        st.markdown(f"<div style='height:200px; display:flex; align-items:center; justify-content:center; flex-direction:column;'><span style='color:grey;'>{{today_str}}</span><b>0 ₪</b></div>", unsafe_allow_html=True)

st.divider()

# --- 8. КАРТОЧКИ (ПАСТЕЛЬНЫЕ) ---
for name, info in envelopes.items():
    spent = st.session_state.spent_data[name]
    limit = info['limit']
    perc = min(int((spent / limit) * 100), 100) if limit > 0 else 0
    main_color = rich_colors.get(name, "#8e8e93")
    
    # HTML карточки с пастельным фоном (rgba)
    st.markdown(f"""
    <div class="envelope-card" style="background: {main_color}1A;">
        <div class="env-row">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="material-symbols-outlined" style="color:{main_color};">{{info['icon']}}</span>
                <span class="env-name">{{name}}</span>
            </div>
            <div class="env-spent" style="color:{main_color if spent > 0 else '#ccc'};">{{spent} ₪</div>
        </div>
        <div class="custom-progress-bg">
            <div class="custom-progress-fill" style="width: {perc}%; background-color: {main_color};"></div>
        </div>
        <div class="env-footer">Лимит: {limit} ₪ | Осталось: {limit-spent} ₪</div>
    </div>
    """, unsafe_allow_html=True)

# Обязательные платежи (База)
with st.expander("🔒 Обязательные платежи"):
    st.write("🏠 Машканта: 5700 | 💳 Кредиты: 2540")
    st.write("⚡ Счета: 916 | 🏋️ Спорт: 1000")
