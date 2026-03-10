import streamlit as st

# Настройка страницы (компактный вид)
st.set_page_config(page_title="Макс-Бюджет", page_icon="💎", layout="centered")

# Убираем лишние отступы и делаем шрифт крупнее
st.markdown("""
    <style>
    .stNumberInput input { font-size: 20px !important; font-weight: bold; }
    div[data-baseweb="select"] { font-size: 18px !important; }
    </style>
""", unsafe_allow_html=True)

# Инициализация твоих конвертов
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

st.title("💎 Мой Макс-Бюджет")

# --- БЛОК 1: БЫСТРАЯ ЗАПИСЬ (НА САМОМ ВЕРХУ) ---
st.subheader("⚡ Внести расход")

# format="%d" гарантирует, что не будет никаких .00
col1, col2 = st.columns([2, 1])
with col1:
    expense_cat = st.selectbox("Категория", list(st.session_state.budget.keys()), label_visibility="collapsed")
with col2:
    expense_amount = st.number_input("Сумма (₪)", min_value=0, step=10, format="%d", value=0, label_visibility="collapsed")

if st.button("➕ Записать трату", use_container_width=True):
    if expense_amount > 0:
        st.session_state.budget[expense_cat]['spent'] += expense_amount
        st.session_state.history.insert(0, f"✅ {expense_cat}: потрачено {expense_amount} ₪")
        st.rerun()

st.divider()

# --- БЛОК 2: ТВОИ КОНВЕРТЫ (СВЕТОФОР) ---
st.subheader("📂 Мои конверты")

for cat, data in st.session_state.budget.items():
    limit = data['limit']
    spent = data['spent']
    percent = int((spent / limit) * 100) if limit > 0 else 0
    
    if percent < 50: emoji = "🟢"
    elif percent < 85: emoji = "🟡"
    else: emoji = "🔴"
        
    st.markdown(f"**{emoji} {cat}**")
    st.progress(min(percent / 100, 1.0))
    st.caption(f"Потрачено: **{spent}** из {limit} ₪")

st.divider()

# --- БЛОК 3: СПРЯТАННАЯ ИНФОРМАЦИЯ ---
col_a, col_b = st.columns(2)

with col_a:
    with st.expander("🔒 Обязательные платежи"):
        st.write("**Всего: 9 156 ₪**")
        st.write("🏠 Машканта: 5 700")
        st.write("💳 Кредиты: 2 540")
        st.write("⚡ Счета: 916")

with col_b:
    with st.expander("📝 История операций"):
        if st.session_state.history:
            for item in st.session_state.history[:10]:
                st.write(item)
        else:
            st.write("Пока пусто.")
