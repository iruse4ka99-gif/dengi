import streamlit as st
import plotly.express as px
import pandas as pd

# --- 1. НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Электронный кошелёк", page_icon="💳", layout="wide")

# --- 2. ПРЕМИУМ ДИЗАЙН (CSS) ---
# Здесь зашита магия "живого" интерфейса: тени, анимации, скругления
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container {padding-top: 1.5rem; padding-bottom: 3rem;}
    
    /* Стили для метрик (KPI) */
    div[data-testid="metric-container"] {
        background-color: rgba(128, 128, 128, 0.05);
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Стили для ЖИВЫХ КАРТОЧЕК конвертов */
    .wallet-card {
        background-color: rgba(128, 128, 128, 0.05);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 14px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .wallet-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
    }
    .card-header {
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;
    }
    .card-title-box {
        display: flex; align-items: center; gap: 12px;
    }
    .card-icon {
        width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; 
        justify-content: center; color: white; font-weight: bold; font-size: 18px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.15);
    }
    .card-name { font-size: 18px; font-weight: 700; letter-spacing: 0.5px;}
    .card-amount-red { font-size: 24px; font-weight: 800; color: #ff3b30; }
    .card-amount-grey { font-size: 24px; font-weight: 800; color: #8e8e93; }
    
    /* Изящный прогресс-бар */
    .progress-track {
        width: 100%; height: 6px; background-color: rgba(128, 128, 128, 0.2); border-radius: 10px; overflow: hidden;
    }
    .progress-fill { height: 100%; border-radius: 10px; transition: width 0.5s ease; }
    .card-footer { font-size: 13px; color: #8e8e93; margin-top: 8px; font-weight: 500;}
    
    /* Тексты для истории */
    .history-minus { color: #ff3b30; font-weight: 600; }
    .history-plus { color: #34c759; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# Глубокие, дорогие цвета для графика и иконок
rich_colors = {
    "Продукты и Хозтовары": "#E63946", # Насыщенный рубиновый
    "Доп. уроки": "#1D3557",           # Глубокий сапфировый
    "Лео": "#F4A261",                  # Теплый апельсиновый
    "Здоровье и Аптека": "#2A9D8F",    # Изумрудный
    "Машина": "#7209B7",               # Сочный фиолетовый
    "Арина": "#D90429",                # Ярко-красный
    "Натан": "#4361EE",                # Насыщенный синий
    "Онлайн и Подписки": "#4EA8DE",    # Лазурный
    "Разное": "#6C757D"                # Графитовый
}

# --- 3. ИНИЦИАЛИЗАЦИЯ ДАННЫХ ---
if 'budget' not in st.session_state:
    st.session_state.budget = {
        "Продукты и Хозтовары": {"limit": 4000, "spent": 0},
        "Доп. уроки": {"limit": 2254, "spent": 0},
        "Лео": {"limit": 1000, "spent": 0},
        "Здоровье и Аптека": {"limit": 500, "spent": 0},
        "Машина": {"limit": 350, "spent": 0},
        "Арина": {"limit": 100, "spent": 0},
        "Натан": {"limit": 100, "spent": 0},
        "Онлайн и Подписки": {"limit": 100, "spent": 0},
        "Разное": {"limit": 100, "spent": 0},
    }
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 4. ВЕРХНЯЯ ПАНЕЛЬ (KPI) ---
st.title("💳 Электронный кошелёк")

total_limit = sum(data['limit'] for data in st.session_state.budget.values())
total_spent = sum(data['spent'] for data in st.session_state.budget.values())
total_left = total_limit - total_spent

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Свободные деньги (Лимит)", f"{total_limit} ₪")
col_m2.metric("Уже потрачено", f"{total_spent} ₪")
col_m3.metric("Доступный остаток", f"{total_left} ₪", delta=f"{total_left} ₪" if total_left >= 0 else "Перерасход", delta_color="normal" if total_left >= 0 else "inverse")

st.divider()

# --- 5. ЦЕНТРАЛЬНЫЙ БЛОК: ГРАФИК И БЫСТРЫЙ ВВОД ---
col_chart, col_input = st.columns([1.2, 1])

with col_chart:
    st.subheader("📊 Аналитика (Насыщенное кольцо)")
    df_data = [{"Категория": cat, "Сумма": data['spent']} for cat, data in st.session_state.budget.items() if data['spent'] > 0]
    
    if not df_data:
        st.info("Кольцо оживёт, как только ты внесешь первую сумму.")
        fig = px.pie(values=[1], names=["Пусто"], hole=0.65, color_discrete_sequence=['#e0e0e0'])
    else:
        df = pd.DataFrame(df_data)
        # Применяем нашу глубокую палитру к графику
        fig = px.pie(df, values='Сумма', names='Категория', hole=0.65, color='Категория', color_discrete_map=rich_colors)
    
    fig.update_traces(textinfo='percent', hoverinfo='label+value', textfont_size=15, hovertemplate="<b>%{label}</b><br>%{value} ₪ (%{percent})")
    fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), margin=dict(t=0, b=0, l=0, r=0), height=420)
    fig.add_annotation(text=f"Траты:<br><b style='color:#ff3b30;'>{total_spent} ₪</b>", x=0.5, y=0.5, font_size=22, showarrow=False)
    st.plotly_chart(fig, use_container_width=True)

with col_input:
    # Идеальная форма: нули стирать не нужно, очищается сама
    with st.form("quick_expense", clear_on_submit=True):
        st.subheader("⚡ Записать покупку")
        expense_cat = st.selectbox("Куда потратили?", list(st.session_state.budget.keys()))
        expense_amount = st.number_input("Сумма (₪)", min_value=0, step=10, format="%d")
        
        submitted = st.form_submit_button("➕ Внести", type="primary", use_container_width=True)
        if submitted and expense_amount > 0:
            st.session_state.budget[expense_cat]['spent'] += expense_amount
            st.session_state.history.insert(0, f"<span class='history-minus'>➖ {expense_cat}: {expense_amount} ₪</span>")
            st.rerun()

st.divider()

# --- 6. СОСТОЯНИЕ КОНВЕРТОВ (ЖИВЫЕ КАРТОЧКИ) ---
st.subheader("📂 Твои конверты")

# Выводим конверты красивой сеткой (по 2 в ряд)
cols = st.columns(2)
for index, (cat, data) in enumerate(st.session_state.budget.items()):
    limit = data['limit']
    spent = data['spent']
    percent = int((spent / limit) * 100) if limit > 0 else 0
    clamped_percent = min(percent, 100) # Чтобы полоска не вылезала за края при перерасходе
    
    color = rich_colors.get(cat, "#333333")
    first_letter = cat[0].upper()
    amount_class = "card-amount-red" if spent > 0 else "card-amount-grey"
    
    # HTML-код самой карточки
    card_html = f"""
    <div class="wallet-card">
        <div class="card-header">
            <div class="card-title-box">
                <div class="card-icon" style="background-color: {color};">{first_letter}</div>
                <div class="card-name">{cat}</div>
            </div>
            <div class="{amount_class}">{spent} ₪</div>
        </div>
        <div class="progress-track">
            <div class="progress-fill" style="width: {clamped_percent}%; background-color: {color};"></div>
        </div>
        <div class="card-footer">Потрачено {spent} из {limit} ₪ ({percent}%)</div>
    </div>
    """
    # Раскидываем карточки по двум колонкам
    with cols[index % 2]:
        st.markdown(card_html, unsafe_allow_html=True)

st.divider()

# --- 7. ПОДВАЛ (Скрытые технические зоны) ---
col_bot1, col_bot2 = st.columns(2)

with col_bot1:
    with st.expander("📝 История операций", expanded=False):
        if st.session_state.history:
            for item in st.session_state.history[:15]:
                st.markdown(item, unsafe_allow_html=True)
        else:
            st.write("Пока пусто.")

    with st.expander("🔄 Перевод между конвертами"):
        with st.form("transfer_form", clear_on_submit=True):
            f_cat = st.selectbox("Из конверта:", list(st.session_state.budget.keys()), key="tf")
            t_cat = st.selectbox("В конверт:", list(st.session_state.budget.keys()), key="tt")
            t_amt = st.number_input("Сумма (₪)", min_value=0, step=10, format="%d")
            if st.form_submit_button("Перевести") and t_amt > 0 and f_cat != t_cat:
                st.session_state.budget[f_cat]['limit'] -= t_amt
                st.session_state.budget[t_cat]['limit'] += t_amt
                st.session_state.history.insert(0, f"<span class='history-plus'>🔄 Перевод: {t_amt} ₪ из {f_cat} в {t_cat}</span>")
                st.rerun()

with col_bot2:
    with st.expander("🔒 База (Фиксированные платежи)", expanded=False):
        st.info("Эти деньги списываются сами, мы ими не управляем:")
        st.markdown("**🏠 Машканта:** 5 700 ₪")
        st.markdown("**💳 Кредиты:** 2 540 ₪")
        st.markdown("**⚡ Счета и Связь:** 916 ₪")
        st.markdown("**🏋️ Спорт и Секции:** 1 000 ₪")
        st.markdown("---")
        st.markdown("<b>ИТОГО ЗАБЛОКИРОВАНО: <span style='color:#ff3b30;'>10 156 ₪</span></b>", unsafe_allow_html=True)
