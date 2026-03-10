import streamlit as st

st.set_page_config(page_title="Мой Бюджет", page_icon="💎", layout="centered")

# Убиваем стандартный скучный дизайн Streamlit и делаем красиво
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 0rem; max-width: 600px;}
    
    /* Делаем поле ввода суммы огромным и удобным (никаких лишних нулей) */
    .stNumberInput input {
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        font-size: 18px !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# База данных (только целые числа, никаких дробей!)
if 'budget' not in st.session_state:
    st.session_state.budget = {
        "🛒 Продукты": {"limit": 4000, "spent": 0},
        "📚 Доп. уроки": {"limit": 2254, "spent": 0},
        "🏋️ Спорт и Секции": {"limit": 1000, "spent": 0},
        "👶 Лео (Малыш)": {"limit": 1000, "spent": 0},
        "🏥 Здоровье": {"limit": 500, "spent": 0},
        "🚗 Машина": {"limit": 350, "spent": 0},
        "👧 Арина": {"limit": 100, "spent": 0},
        "👦 Натан": {"limit": 100, "spent": 0},
        "🎮 Досуг": {"limit": 40, "spent": 0},
    }
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown("<h2 style='text-align: center; color: #1f2937; margin-bottom: 20px;'>💎 Мой Бюджет</h2>", unsafe_allow_html=True)

# --- БЛОК 1: БЫСТРЫЙ ВВОД ---
st.markdown("<h4 style='color: #4b5563; margin-bottom: 10px;'>⚡ Внести расход</h4>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    cat = st.selectbox("Категория", list(st.session_state.budget.keys()), label_visibility="collapsed")
with col2:
    # format="%d" и step=10 гарантируют, что будут только целые числа
    amt = st.number_input("Сумма", min_value=0, step=10, format="%d", value=0, label_visibility="collapsed")

if st.button("➕ ДОБАВИТЬ ТРАТУ", use_container_width=True):
    if amt > 0:
        st.session_state.budget[cat]['spent'] += int(amt)
        st.session_state.history.insert(0, f"✅ {cat}: потрачено {int(amt)} ₪")
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- БЛОК 2: КРАСИВЫЕ КАРТОЧКИ (КАК НА ТВОЕМ СКРИНЕ) ---
for name, data in st.session_state.budget.items():
    limit = int(data['limit'])
    spent = int(data['spent'])
    remain = limit - spent
    
    # Логика цветов: Зеленый -> Желтый -> Красный
    if remain > (limit * 0.2):
        bg_color = "#f0fdf4" # светло-зеленый фон
        border_color = "#4ade80" # зеленая полоска
        text_color = "#166534"
    elif remain >= 0:
        bg_color = "#fefce8" # светло-желтый фон
        border_color = "#facc15" # желтая полоска
        text_color = "#854d0e"
    else:
        bg_color = "#fef2f2" # светло-красный фон
        border_color = "#f87171" # красная полоска
        text_color = "#991b1b"
        
    # Рисуем саму карточку HTML-кодом
    card_html = f"""
    <div style="
        background-color: {bg_color}; 
        padding: 15px 20px; 
        border-radius: 12px; 
        margin-bottom: 12px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        border-bottom: 4px solid {border_color};
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    ">
        <div style="display: flex; flex-direction: column;">
            <span style="font-size: 18px; font-
