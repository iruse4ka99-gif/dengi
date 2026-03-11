import streamlit as st
import plotly.express as px
import pandas as pd

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Наш электронный кошелёк", page_icon="💳", layout="wide")

# --- ПРЕМИУМ ДИЗАЙН (ЖИДКОЕ СТЕКЛО) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    
    /* Эффект жидкого стекла */
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
    
    /* Верхние показатели */
    .stat-box { text-align: center; width: 33%; display: inline-block; }
    .stat-title { font-size: 13px; color: #555; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
    .stat-value { font-size: 24px; font-weight: bold; color: #222; }
    .stat-value.red { color: #d9534f; }
    .stat-value.green { color: #5cb85c; }
    </style>
""", unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ ДАННЫХ (Твоя логика - не трогал!) ---
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

st.title("💎 Наш электронный кошелёк")

# Считаем общие суммы
total_limit = sum(data['limit'] for data in st.session_state.budget.values())
total_spent = sum(data['spent'] for data in st.session_state.budget.values())
total_left = total_limit - total_spent

# --- 1. ВЕРХНЯЯ ПАНЕЛЬ (Жидкое стекло) ---
st.markdown(f"""
<div class="glass-card" style="display: flex; justify-content: space-around;">
    <div class="stat-box"><div class="stat-title">Доступно (без фиксов)</div><div class="stat-value">{total_limit} ₪</div></div>
    <div class="stat-box"><div class="stat-title">Уже потрачено</div><div class="stat-value red">{total_spent} ₪</div></div>
    <div class="stat-box"><div class="stat-title">Остаток</div><div class="stat-value green">{total_left} ₪</div></div>
</div>
""", unsafe_allow_html=True)

# --- 2. ЦЕНТРАЛЬНЫЙ БЛОК: КРУГ ---
st.subheader("📊 Распределение трат")
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
df_data = [{"Категория": cat, "Сумма": data['spent']} for cat, data in st.session_state.budget.items() if data['spent'] > 0]
    
if not df_data:
    st.info("💡 Трат пока нет. График появится после первой записи.")
    df_data.append({"Категория": "Ждем первые траты...", "Сумма": 1})
    fig = px.pie(df_data, values='Сумма', names='Категория', hole=0.7, color_discrete_sequence=['#e0e0e0'])
else:
    df = pd.DataFrame(df_data)
    # Используем красивые пастельные цвета для графика
    fig = px.pie(df, values='Сумма', names='Категория', hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel)
    
fig.update_traces(textinfo='percent', hoverinfo='label+value', textfont_size=14)
fig.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5), margin=dict(t=0, b=0, l=0, r=0), height=350)
fig.add_annotation(text=f"Траты:<br><b>{total_spent} ₪</b>", x=0.5, y=0.5, font_size=20, showarrow=False)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 3. ВНЕСЕНИЕ РАСХОДА (Открытая форма) ---
st.subheader("⚡ Внести расход")
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        expense_cat = st.selectbox("Куда потратили?", list(st.session_state.budget.keys()))
    with col2:
        # Убрал шаг 10, теперь step=1 (только целые числа!)
        expense_amount = st.number_input("Сумма (₪)", min_value=0, step=1, format="%d")
        
    submitted_expense = st.form_submit_button("➕ ЗАПИСАТЬ РАСХОД", type="primary", use_container_width=True)
        
    if submitted_expense and expense_amount > 0:
        st.session_state.budget[expense_cat]['spent'] += expense_amount
        st.session_state.history.insert(0, f"➖ {expense_cat}: <span style='color:#ff4b4b; font-weight:bold;'>-{expense_amount} ₪</span>")
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- 4. КОНВЕРТЫ С ПРОГРЕССОМ ---
st.subheader("📂 Состояние конвертов")
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
for cat, data in st.session_state.budget.items():
    limit = data['limit']
    spent = data['spent']
    percent = int((spent / limit) * 100) if limit > 0 else 0
        
    st.markdown(f"**{cat}**")
    st.progress(min(percent / 100, 1.0))
    st.caption(f"Потрачено: **{spent} ₪** из {limit} ₪ ({percent}%)")
    st.write("")
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# --- 5. ПОДВАЛ (История, База, Переводы) ---
col_hist, col_fix = st.columns(2)

with col_hist:
    with st.expander("📝 История операций", expanded=True):
        if st.session_state.history:
            for item in st.session_state.history[:10]:
                st.markdown(item, unsafe_allow_html=True)
        else:
            st.write("Пока пусто.")
            
    with st.expander("🔄 Перевод между конвертами"):
        with st.form("transfer_form", clear_on_submit=True):
            from_cat = st.selectbox("Откуда забрать?", list(st.session_state.budget.keys()), key="from")
            to_cat = st.selectbox("Куда добавить?", list(st.session_state.budget.keys()), key="to")
            transfer_amount = st.number_input("Сумма перевода (₪)", min_value=0, step=1, format="%d")
            
            submitted_transfer = st.form_submit_button("Выполнить перевод", use_container_width=True)
            
            if submitted_transfer and transfer_amount > 0 and from_cat != to_cat:
                st.session_state.budget[from_cat]['limit'] -= transfer_amount
                st.session_state.budget[to_cat]['limit'] += transfer_amount
                st.session_state.history.insert(0, f"🔄 Перевод: из {from_cat} в {to_cat} <span style='color:#00cc66; font-weight:bold;'>+{transfer_amount} ₪</span>")
                st.rerun()

with col_fix:
    with st.expander("🔒 Обязательные платежи (База)", expanded=True):
        st.write("Твои фиксированные счета на месяц (уже учтены):")
        st.write("🏠 **Машканта:** 5 700 ₪")
        st.write("💳 **Кредиты:** 2 540 ₪")
        st.write("🏛 **Арнона:** 1 500 ₪")
        st.write("⚡ **Электричество:** 600 ₪")
        st.write("📱 **Телефон + интернет:** 600 ₪")
        st.write("🏥 **Больничная касса:** 350 ₪")
        st.write("💧 **Вода:** 200 ₪")
        st.write("🎨 **Кружки детей:** 1 000 ₪")
        st.write("---")
        st.write("**ИТОГО БАЗА:** 12 490 ₪")
