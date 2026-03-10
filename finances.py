import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- 1. НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Кошелёк", page_icon="💳", layout="centered")

# Подключаем стильные иконки Google Material Symbols
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">', unsafe_allow_html=True)

# --- 2. ПРЕМИУМ ДИЗАЙН (CSS) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    
    /* Компактная шапка с метриками */
    .kpi-container {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(128, 128, 128, 0.1); border-radius: 12px; padding: 10px 15px; margin-bottom: 15px;
    }
    .kpi-item { text-align: center; flex: 1; }
    .kpi-label { font-size: 11px; color: #8e8e93; text-transform: uppercase; font-weight: 600; }
    .kpi-value { font-size: 18px; font-weight: 800; }

    /* Карточки конвертов (Стиль Max) */
    .envelope-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 16px; padding: 12px 16px; margin-bottom: 10px;
    }
    .env-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .env-title-box { display: flex; align-items: center; gap: 10px; }
    .env-icon { color: #8e8e93; font-size: 24px !important; }
    .env-name { font-size: 16px; font-weight: 600; }
    .env-spent { font-size: 20px; font-weight: 800; }
    .env-spent.active { color: #ff3b30; }
    .env-spent.empty { color: #8e8e93; }
    
    /* Тонкий прогресс-бар */
    .custom-progress-bg { width: 100%; height: 6px; background: rgba(128, 128, 128, 0.2); border-radius: 10px; }
    .custom-progress-fill { height: 100%; border-radius: 10px; transition: width 0.4s ease; }
    .env-footer { font-size: 12px; color: #8e8e93; margin-top: 5px; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# --- 3. ПОДКЛЮЧЕНИЕ К ГУГЛ ТАБЛИЦЕ ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Здесь 'Data' - название листа в твоей вчерашней таблице
    df = conn.read(worksheet="Data", ttl="0m")
except:
    # Если таблица еще не настроена в Secrets, создаем временную структуру
    df = pd.DataFrame()

# --- 4. ЛОГИКА ДАННЫХ ---
# Фиксированные платежи (База)
fixed_payments = {
    "🏠 Машканта": 5700,
    "💳 Кредиты": 2540,
    "⚡ Счета и Связь": 916,
    "🏋️ Спорт и Кружки": 1000
}
total_fixed = sum(fixed_payments.values())

# Наши конверты и их лимиты
envelopes = {
    "Продукты и Хозтовары": {"limit": 4000, "icon": "shopping_cart", "color": "#FF5733"},
    "Доп. уроки": {"limit": 2254, "icon": "menu_book", "color": "#33CFFF"},
    "Лео": {"limit": 1000, "icon": "child_care", "color": "#FF33F6"},
    "Здоровье и Аптека": {"limit": 500, "icon": "medical_services", "color": "#33FF57"},
    "Машина": {"limit": 350, "icon": "directions_car", "color": "#FFF633"},
    "Арина": {"limit": 100, "icon": "person", "color": "#5733FF"},
    "Натан": {"limit": 100, "icon": "person", "color": "#FF3383"},
    "Онлайн и Подписки": {"limit": 100, "icon": "devices", "color": "#8333FF"},
    "Разное": {"limit": 100, "icon": "more_horiz", "color": "#FFB833"}
}

# Инициализация трат (если нет данных из таблицы)
if 'spent_data' not in st.session_state:
    st.session_state.spent_data = {cat: 0 for cat in envelopes}
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 5. ВЕРХНИЙ KPI БАР (3 в ряд) ---
total_limit = sum(e['limit'] for e in envelopes.values())
total_spent = sum(st.session_state.spent_data.values())
remaining = total_limit - total_spent

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-item">
        <div class="kpi-label">Лимит</div>
        <div class="kpi-value">{total_limit} ₪</div>
    </div>
    <div class="kpi-item" style="border-left: 1px solid rgba(128,128,128,0.3); border-right: 1px solid rgba(128,128,128,0.3);">
        <div class="kpi-label">Траты</div>
        <div class="kpi-value" style="color:#ff3b30;">{total_spent} ₪</div>
    </div>
    <div class="kpi-item">
        <div class="kpi-label">Остаток</div>
        <div class="kpi-value" style="color:#34c759;">{remaining} ₪</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 6. КОМПАКТНОЕ КОЛЬЦО И ВВОД ---
col_in, col_ch = st.columns([1, 1])

with col_in:
    with st.form("add_exp", clear_on_submit=True):
        st.write("➕ **Новая трата**")
        cat_select = st.selectbox("Категория", list(envelopes.keys()), label_visibility="collapsed")
        amt_input = st.number_input("Сумма", min_value=0, step=10, format="%d")
        if st.form_submit_button("Записать", use_container_width=True, type="primary"):
            if amt_input > 0:
                st.session_state.spent_data[cat_select] += amt_input
                st.session_state.history.insert(0, f"➖ {cat_select}: {amt_input} ₪")
                # Тут будет код сохранения в Таблицу (conn.update)
                st.rerun()

with col_ch:
    df_chart = pd.DataFrame([{"cat": k, "val": v} for k, v in st.session_state.spent_data.items() if v > 0])
    if not df_chart.empty:
        fig = px.pie(df_chart, values='val', names='cat', hole=0.8, 
                     color='cat', color_discrete_map={k: v['color'] for k, v in envelopes.items()})
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=180)
        fig.update_traces(textinfo='none', hovertemplate="%{label}: %{value} ₪")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.markdown("<div style='height:180px; display:flex; align-items:center; justify-content:center; color:grey; font-size:12px;'>Кольцо оживет после трат</div>", unsafe_allow_html=True)

st.divider()

# --- 7. КАРТОЧКИ КОНВЕРТОВ (Дизайн Max) ---
for name, info in envelopes.items():
    spent = st.session_state.spent_data[name]
    limit = info['limit']
    perc = min(int((spent / limit) * 100), 100) if limit > 0 else 0
    color = info['color']
    
    st.markdown(f"""
    <div class="envelope-card">
        <div class="env-row">
            <div class="env-title-box">
                <span class="material-symbols-outlined env-icon">{info['icon']}</span>
                <span class="env-name">{name}</span>
            </div>
            <div class="env-spent {'active' if spent > 0 else 'empty'}">{spent} ₪</div>
        </div>
        <div class="custom-progress-bg">
            <div class="custom-progress-fill" style="width: {perc}%; background-color: {color};"></div>
        </div>
        <div class="env-footer">Потрачено {spent} из {limit} ₪ ({perc}%)</div>
    </div>
    """, unsafe_allow_html=True)

# --- 8. ПОДВАЛ (Скрытые зоны) ---
st.write("")
col_b1, col_b2 = st.columns(2)

with col_b1:
    with st.expander("📜 История"):
        for item in st.session_state.history[:10]:
            st.write(item)

with col_b2:
    with st.expander("🔄 Перевод"):
        with st.form("transfer", clear_on_submit=True):
            f = st.selectbox("Из:", list(envelopes.keys()))
            t = st.selectbox("В:", list(envelopes.keys()))
            a = st.number_input("Сумма", min_value=0, format="%d")
            if st.form_submit_button("ОК"):
                st.session_state.spent_data[f] -= a
                # Логика изменения лимита в таблице будет тут
                st.rerun()

with st.expander("🔒 Обязательные платежи (База)"):
    for k, v in fixed_payments.items():
        st.write(f"{k}: **{v} ₪**")
    st.markdown(f"--- \n**ИТОГО: {total_fixed} ₪**")
