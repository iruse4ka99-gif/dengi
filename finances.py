import streamlit as st

# Настройка страницы
st.set_page_config(page_title="Ира: Макс-Бюджет", page_icon="💎", layout="centered")

# Инициализация данных (чтобы они не стирались при обновлении страницы)
if 'budget' not in st.session_state:
    st.session_state.budget = {
        "🛒 Продукты и Хозтовары": {"limit": 4000, "spent": 0},
        "📚 Дополнительные уроки": {"limit": 2254, "spent": 0},
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

# Заголовок
st.title("💳 Мой Макс-Бюджет")
st.write("Твоё личное приложение для контроля расходов.")

# Блок 1: Обязательные платежи
st.header("🔒 Обязательные платежи (Фикс)")
st.info("""
**Списываются автоматически:**
* 🏠 **Машканта:** 5 700 ₪
* 💳 **Кредиты:** 2 540 ₪
* ⚡ **Счета и Связь:** 916 ₪
---
**Итого заблокировано:** 9 156 ₪
""")

# Блок 2: Твои конверты со Светофором
st.header("📂 Мои конверты")

for cat, data in st.session_state.budget.items():
    limit = data['limit']
    spent = data['spent']
    
    # Считаем процент
    percent = (spent / limit) * 100 if limit > 0 else 0
    
    # Логика "Светофора"
    if percent < 50:
        color_emoji = "🟢"
    elif percent < 85:
        color_emoji = "🟡"
    else:
        color_emoji = "🔴"
        
    # Вывод категории
    st.subheader(f"{color_emoji} {cat}")
    st.write(f"Потрачено: **{spent}** ₪ из **{limit}** ₪")
    
    # Визуальный градусник (Streamlit progress bar)
    progress_val = min(percent / 100, 1.0)
    st.progress(progress_val)

st.divider()

# Блок 3: Внесение трат и переводы
st.header("🛠 Управление бюджетом")

col1, col2 = st.columns(2)

with col1:
    st.subheader("➕ Внести расход")
    expense_cat = st.selectbox("Куда потратили?", list(st.session_state.budget.keys()), key="exp_cat")
    expense_amount = st.number_input("Сумма (₪)", min_value=0.0, step=10.0, key="exp_amt")
    if st.button("Записать трату"):
        if expense_amount > 0:
            st.session_state.budget[expense_cat]['spent'] += expense_amount
            st.session_state.history.insert(0, f"➖ {expense_amount} ₪ ({expense_cat})")
            st.rerun()

with col2:
    st.subheader("🔄 Перевод между папками")
    from_cat = st.selectbox("Откуда забрать?", list(st.session_state.budget.keys()), key="from_cat")
    to_cat = st.selectbox("Куда добавить?", list(st.session_state.budget.keys()), key="to_cat")
    transfer_amount = st.number_input("Сумма перевода (₪)", min_value=0.0, step=10.0, key="trans_amt")
    if st.button("Перевести"):
        if transfer_amount > 0 and from_cat != to_cat:
            st.session_state.budget[from_cat]['limit'] -= transfer_amount
            st.session_state.budget[to_cat]['limit'] += transfer_amount
            st.session_state.history.insert(0, f"🔄 {transfer_amount} ₪ из {from_cat} в {to_cat}")
            st.rerun()

st.divider()

# Блок 4: История операций
st.header("📜 История операций")
if st.session_state.history:
    for item in st.session_state.history[:10]: # Показываем последние 10
        st.write(item)
else:
    st.write("Пока пусто. Сделай первую запись!")
