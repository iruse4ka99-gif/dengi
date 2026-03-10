import streamlit as st

# הגדרות עמוד בסיסיות
st.set_page_config(page_title="Бюджет", layout="centered")

# שמירת נתונים כדי שההוצאות לא יתאפסו
if 'spent' not in st.session_state:
    st.session_state.spent = 0

START_LIMIT = 8504

# --- פאנל עליון: יתרה ---
clean_spent = round(st.session_state.spent)
clean_left = round(START_LIMIT - clean_spent)

col1, col2, col3 = st.columns(3)
col1.metric("ЛИМИТ", f"{START_LIMIT} ₪")
col2.metric("ТРАТЫ", f"{clean_spent} ₪")
col3.metric("ОСТАТОК", f"{clean_left} ₪")

# --- מקום לגלגל (Колесо Бюджета) ---
st.markdown("---")
st.markdown("<h4 style='text-align: center; color: #888;'>Здесь твое Колесо Бюджета</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- הזנת הוצאה חדשה (תמיד פתוח) ---
st.subheader("+ Новая трата")
category = st.selectbox("Куда?", ["Продукты и Хозтовары", "Аптека", "Прочее"])

# format="%d" מבטיח שיהיו רק מספרים שלמים
amount = st.number_input("Сколько ₪ (только целые числа)", min_value=0, step=1, format="%d")

if st.button("ЗАПИСАТЬ", use_container_width=True):
    if amount > 0:
        st.session_state.spent += round(amount)
        st.rerun()

# --- חשבונות קבועים (תמיד למטה) ---
st.markdown("---")
st.subheader("Фиксированные счета")

st.number_input("Машканта", min_value=0, step=1, format="%d", key="mashkanta")
st.number_input("Арнона", min_value=0, step=1, format="%d", key="arnona")
st.number_input("Электричество", min_value=0, step=1, format="%d", key="electro")
st.number_input("Вода и Газ", min_value=0, step=1, format="%d", key="water")
st.number_input("Кружки (Арина, Натан, Лео)", min_value=0, step=1, format="%d", key="kids")
st.number_input("Доп. уроки (Артур)", min_value=0, step=1, format="%d", key="artur")
