import streamlit as st
import pandas as pd
import plotly.express as px

# Настройка страницы
st.set_page_config(page_title="Мой Бюджет", page_icon="💎", layout="centered")

# --- ДИЗАЙН "ЖИДКОЕ СТЕКЛО" ---
st.markdown("""
<style>
    .glass-card {
        background: rgba(255, 255, 255, 0.65);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 20px;
        margin-bottom: 20px;
    }
    .stat-box { text-align: center; width: 33%; }
    .stat-title { font-size: 13px; color: #555; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .stat-value { font-size: 22px; font-weight: bold; color: #222; }
    .stat-value.red { color: #d9534f; }
    .stat-value.green { color: #5cb85c; }
    
    /* Убираем лишние отступы у expander */
    .streamlit-expanderHeader { font-weight: bold; color: #333; }
</style>
""", unsafe_allow_html=True)

# --- 1. ВЕРХ: ПОКАЗАТЕЛИ ---
st.markdown("""
<div class="glass-card" style="display: flex; justify-content: space-between;">
    <div class="stat-box"><div class="stat-title">Лимит</div><div class="stat-value">18500 ₪</div></div>
    <div class="stat-box"><div class="stat-title">Траты</div><div class="stat-value red">0 ₪</div></div>
    <div class="stat-box"><div class="stat-title">Остаток</div><div class="stat-value green">18500 ₪</div></div>
</div>
""", unsafe_allow_html=True)

# --- 2. КРУГ (ГРАФИК БЮДЖЕТА) ---
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
# Создаем красивый круглый график
data = pd.DataFrame({
    "Категория": ["Машина", "Продукты", "Аптека", "Остаток"],
    "Сумма": [240, 1500, 300, 6464]
})
fig = px.pie(data, values="Сумма", names="Категория", hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False, height=250)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 3. ЗАПИСЬ (ВСЕГДА ОТКРЫТА, ТОЛЬКО ЦЕЛЫЕ ЧИСЛА) ---
st.markdown("### ➕ Новая трата")
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    category = st.selectbox("Куда?", ["Продукты и Хозтовары", "Аптека", "Разное", "Машина"], label_visibility="collapsed")
with col2:
    # step=1 гарантирует, что будут только целые числа
    amount = st.number_input("Сколько ₪", min_value=0, step=1, value=0, label_visibility="collapsed")

if st.button("ЗАПИСАТЬ", use_container_width=True):
    if amount > 0:
        st.success(f"Успешно записано: {category} - {amount} ₪")
        # --- ТУТ БУДЕТ СВЯЗЬ С ТАБЛИЦЕЙ ---
    else:
        st.warning("Введите сумму больше нуля")
st.markdown("</div>", unsafe_allow_html=True)

# --- 4. ГИБКИЕ КОНВЕРТЫ ---
st.markdown("### 📂 Ежедневные конверты")
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

st.markdown("🚗 **Машина**")
st.progress(0.68)
st.caption("Потрачено 240 из 350 ₪")
st.write("")

st.markdown("👧🏼 **Арина**")
st.progress(0.0)
st.caption("Потрачено 0 из 100 ₪")
st.write("")

st.markdown("👦🏻 **Натан**")
st.progress(0.0)
st.caption("Потрачено 0 из 100 ₪")
st.write("")

st.markdown("👶🏼 **Лео**")
st.progress(0.0)
st.caption("Потрачено 0 из 100 ₪")
st.write("")

st.markdown("📚 **Доп. уроки**")
st.progress(0.0)
st.caption("Лимит: 2270 ₪")

st.markdown("</div>", unsafe_allow_html=True)

# --- 5. ПОДВАЛ (ИСТОРИЯ, БАЗА, ПЕРЕВОДЫ) ---
with st.expander("📜 История"):
    st.write("Последние записи появятся здесь после подключения таблицы.")

with st.expander("🔒 Обязательные платежи (База)"):
    st.write("🏠 Машканта: 5700 ₪")
    st.write("💳 Кредиты: 2540 ₪")
    st.write("🏛 Арнона: 1500 ₪")
    st.write("⚡ Электричество: 600 ₪")
    st.write("📱 Телефон + интернет: 600 ₪")
    st.write("🏥 Больничная касса: 350 ₪")
    st.write("💧 Вода: 200 ₪")
    st.write("🎨 Кружки детей: 1000 ₪")

with st.expander("🔄 Перевод между конвертами"):
    st.write("Здесь можно будет перекинуть деньги из одного конверта в другой.")
