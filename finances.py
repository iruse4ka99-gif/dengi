import streamlit as st
import plotly.express as px
import pandas as pd

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Наш электронный кошелёк", page_icon="💳", layout="wide")

# --- ПРЕМИУМ ДИЗАЙН ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .stMetric-value {font-size: 30px !important; font-weight: 800 !important;}
    </style>
""", unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ ДАННЫХ ---
if 'budget' not in st.session_state:
    st.session_state.budget = {
        "🛒 Продукты и Хозтовары": {"limit": 4000, "spent": 0},
        "📚 Доп. уроки": {"limit": 2254, "spent": 0},
        "🏋️ Спорт и Секции": {"limit": 1000, "spent": 0},
        "👶 Лео (Малыш)": {"limit": 1000, "spent": 0},
        "🏥 Здоровье и Аптека": {"limit": 500, "spent": 0},
        "🚗 Машина (Бензин)": {"limit": 350, "spent": 0},
        "👧 Арина (Личное)": {"limit": 100, "spent": 0},
        "👦 Натан (Личное)": {"limit": 100, "spent": 0},
        "🎮 Досуг и мелочи": {"limit": 40, "spent": 0},
    }
if 'history' not in st.session_state:
    st.session_state.history = []

# --- ВЕРХНЯЯ ПАНЕЛЬ ---
st.title("💳 Наш электронный кошелёк")
st.caption("Совместный контроль расходов и поиск финансовых дыр.")

# Считаем общие суммы
total_limit = sum(data['limit'] for data in st.session_state.budget.values())
total_spent = sum(data['spent'] for data in st.session_state.budget.values())
total_left = total_limit - total_spent

# Сводка (KPI)
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric(label="Доступно на месяц (без фиксов)", value=f"{total_limit} ₪")
col_m2.metric(label="Уже потрачено", value=f"{total_spent} ₪")
col_m3.metric(label="Остаток", value=f"{total_left} ₪", delta=f"{total_left} ₪ свободны" if total_left >=0 else "Перерасход!", delta_color="normal")

st.divider()

# --- ЦЕНТРАЛЬНЫЙ БЛОК: ГРАФИК И УПРАВЛЕНИЕ ---
col_chart, col_list = st.columns([1.2, 1])

with col_chart:
    st.subheader("📊 Распределение трат")
    df_data = [{"Категория": cat, "Сумма": data['spent']} for cat, data in st.session_state.budget.items() if data['spent'] > 0]
    
    if not df_data:
        st.info("💡 Трат пока нет. График появится после первой записи.")
        df_data.append({"Категория": "Ждем первые траты...", "Сумма": 1})
        fig = px.pie(df_data, values='Сумма', names='Категория', hole=0.7, color_discrete_sequence=['#2b2b2b'])
    else:
        df = pd.DataFrame(df_data)
        fig = px.pie(df, values='Сумма', names='Категория', hole=0.6, color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig.update_traces(textinfo='percent', hoverinfo='label+value', textfont_size=14)
    fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), margin=dict(t=0, b=0, l=0, r=0), height=400)
    fig.add_annotation(text=f"Траты:<br><b>{total_spent} ₪</b>", x=0.5, y=0.5, font_size=20, showarrow=False)
    st.plotly_chart(fig, use_container_width=True)

with col_list:
    # ИСПОЛЬЗУЕМ st.form ЧТОБЫ ПОЛЯ САМИ ОЧИЩАЛИСЬ
    with st.form("expense_form", clear_on_submit=True):
        st.subheader("⚡ Внести расход")
        expense_cat = st.selectbox("Куда потратили?", list(st.session_state.budget.keys()))
        expense_amount = st.number_input("Сумма (₪)", min_value=0, step=10, format="%d")
        
        # Кнопка отправки формы
        submitted_expense = st.form_submit_button("➕ Записать расход", type="primary", use_container_width=True)
        
        if submitted_expense and expense_amount > 0:
            st.session_state.budget[expense_cat]['spent'] += expense_amount
            # Красный текст для суммы
            st.session_state.history.insert(0, f"➖ {expense_cat}: <span style='color:#ff4b4b; font-weight:bold;'>-{expense_amount} ₪</span>")
            st.rerun()

    # ФОРМА ПЕРЕВОДОВ (ТОЖЕ САМА ОЧИЩАЕТСЯ)
    with st.form("transfer_form", clear_on_submit=True):
        st.subheader("🔄 Перевод между конвертами")
        col_t1, col_t2 = st.columns(2)
        from_cat = col_t1.selectbox("Откуда забрать?", list(st.session_state.budget.keys()))
        to_cat = col_t2.selectbox("Куда добавить?", list(st.session_state.budget.keys()))
        transfer_amount = st.number_input("Сумма перевода (₪)", min_value=0, step=10, format="%d")
        
        submitted_transfer = st.form_submit_button("Выполнить перевод", use_container_width=True)
        
        if submitted_transfer and transfer_amount > 0 and from_cat != to_cat:
            st.session_state.budget[from_cat]['limit'] -= transfer_amount
            st.session_state.budget[to_cat]['limit'] += transfer_amount
            st.session_state.history.insert(0, f"🔄 Перевод: из {from_cat} в {to_cat} <span style='color:#00cc66; font-weight:bold;'>+{transfer_amount} ₪</span>")
            st.rerun()

st.divider()

# --- ПОДВАЛ (Конверты, История и Фиксы) ---
col_env, col_hist_fix = st.columns([1.2, 1])

with col_env:
    st.subheader("📂 Состояние конвертов")
    for cat, data in st.session_state.budget.items():
        limit = data['limit']
        spent = data['spent']
        percent = int((spent / limit) * 100) if limit > 0 else 0
        
        # Строгий стиль без дешевых эмодзи, проценты вернулись
        st.markdown(f"**{cat}**")
        st.progress(min(percent / 100, 1.0))
        st.caption(f"Потрачено: **{spent} ₪** из {limit} ₪ ({percent}%)")

with col_hist_fix:
    with st.expander("📝 История операций", expanded=True):
        if st.session_state.history:
            for item in st.session_state.history[:10]:
                st.markdown(item, unsafe_allow_html=True)
        else:
            st.write("Пока пусто.")

    with st.expander("🔒 Обязательные платежи (База)"):
        st.write("Твои фиксированные счета на месяц:")
        st.write("🏠 **Машканта:** 5 700 ₪")
        st.write("💳 **Кредиты:** 2 540 ₪")
        st.write("⚡ **Счета:** 916 ₪")
        st.write("---")
        st.write("**ИТОГО:** 9 156 ₪")
