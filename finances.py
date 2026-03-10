import streamlit as st
import plotly.express as px
import pandas as pd

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Max-Бюджет PRO", page_icon="💎", layout="wide")

# --- ПРЕМИУМ ДИЗАЙН (Скрываем лишнее, делаем шрифты красивыми) ---
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

# --- ВЕРХНЯЯ ПАНЕЛЬ (ДАШБОРД) ---
st.title("💎 Бюджет Ирины: Управление капиталом")

# Считаем общие суммы
total_limit = sum(data['limit'] for data in st.session_state.budget.values())
total_spent = sum(data['spent'] for data in st.session_state.budget.values())
total_left = total_limit - total_spent

# Красивые метрики в ряд
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric(label="Доступно на месяц (без фиксов)", value=f"{total_limit} ₪")
col_m2.metric(label="Уже потрачено", value=f"{total_spent} ₪")
col_m3.metric(label="Остаток", value=f"{total_left} ₪", delta=f"{total_left} ₪ свободны" if total_left >=0 else "Перерасход!", delta_color="normal")

st.divider()

# --- ЦЕНТРАЛЬНЫЙ БЛОК: ГРАФИК И СПИСОК ---
col_chart, col_list = st.columns([1.2, 1])

with col_chart:
    st.subheader("📊 Аналитика расходов")
    # Подготовка данных для "Бублика"
    df_data = []
    for cat, data in st.session_state.budget.items():
        if data['spent'] > 0:
            df_data.append({"Категория": cat, "Сумма": data['spent']})
    
    # Если еще нет трат, показываем красивую заглушку
    if not df_data:
        st.info("💡 Трат пока нет. Внеси первый расход, чтобы график ожил!")
        # Пустой бублик для красоты
        df_data.append({"Категория": "Ждем первые траты...", "Сумма": 1})
        fig = px.pie(df_data, values='Сумма', names='Категория', hole=0.7, color_discrete_sequence=['#e0e0e0'])
    else:
        # Настоящий интерактивный бублик
        df = pd.DataFrame(df_data)
        fig = px.pie(df, values='Сумма', names='Категория', hole=0.6, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig.update_traces(textinfo='percent', hoverinfo='label+value', textfont_size=14)
    fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), 
                      margin=dict(t=0, b=0, l=0, r=0), height=400)
    
    # Текст в центре бублика
    fig.add_annotation(text=f"Траты:<br><b>{total_spent} ₪</b>", x=0.5, y=0.5, font_size=20, showarrow=False)
    
    st.plotly_chart(fig, use_container_width=True)

with col_list:
    st.subheader("⚡ Быстрое внесение")
    with st.container(border=True):
        expense_cat = st.selectbox("Куда потратили?", list(st.session_state.budget.keys()))
        expense_amount = st.number_input("Сумма (₪)", min_value=0, step=10, format="%d")
        if st.button("➕ Записать расход", use_container_width=True, type="primary"):
            if expense_amount > 0:
                st.session_state.budget[expense_cat]['spent'] += expense_amount
                st.session_state.history.insert(0, f"✅ {expense_cat}: {expense_amount} ₪")
                st.rerun()

    st.subheader("📂 Состояние конвертов")
    # Компактный список папок со светофором
    for cat, data in st.session_state.budget.items():
        limit = data['limit']
        spent = data['spent']
        percent = int((spent / limit) * 100) if limit > 0 else 0
        
        # Индикатор (🟢 🟡 🔴)
        emoji = "🟢" if percent < 50 else "🟡" if percent < 85 else "🔴"
        
        st.markdown(f"**{emoji} {cat}**")
        st.progress(min(percent / 100, 1.0))
        st.caption(f"Потрачено: {spent} из {limit} ₪")

st.divider()

# --- ПОДВАЛ (История и Фиксы) ---
col_hist, col_fix = st.columns(2)
with col_hist:
    with st.expander("📝 Последние операции (История)"):
        if st.session_state.history:
            for item in st.session_state.history[:10]:
                st.write(item)
        else:
            st.write("История чиста.")

with col_fix:
    with st.expander("🔒 Обязательные платежи (База)"):
        st.write("Твои заблокированные деньги на месяц:")
        st.write("🏠 **Машканта:** 5 700 ₪")
        st.write("💳 **Кредиты:** 2 540 ₪")
        st.write("⚡ **Счета:** 916 ₪")
        st.write("---")
        st.write("**ИТОГО:** 9 156 ₪")
