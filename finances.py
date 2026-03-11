import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
import calendar
from streamlit_gsheets import GSheetsConnection

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Семейный Бюджет", layout="wide", initial_sidebar_state="collapsed")

# --- ПОДКЛЮЧЕНИЕ К GOOGLE ТАБЛИЦЕ ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- РАСЧЕТ ДНЕЙ ДО КОНЦА МЕСЯЦА ---
today = datetime.date.today()
_, last_day = calendar.monthrange(today.year, today.month)
days_left = last_day - today.day + 1

# --- ПРЕМИУМ ДИЗАЙН (LIQUID GLASS) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    body, p, div, span, h1, h2, h3 { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important; }

    .glass-card {
        background: rgba(255, 255, 255, 0.65); border-radius: 20px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 15px; margin-bottom: 15px;
    }
    
    .stat-box { text-align: center; width: 33%; display: inline-block; }
    .stat-title { font-size: 11px; color: #777; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px; font-weight: 600;}
    .stat-value { font-size: 22px; font-weight: 700; color: #1d1d1f; }
    .stat-value.red { color: #ff3b30; } .stat-value.green { color: #34c759; }

    .envelope-card { padding: 15px; border-radius: 16px; margin-bottom: 12px; border: 1px solid rgba(0,0,0,0.03); display: flex; flex-direction: column; gap: 8px;}
    .env-header { display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 16px; color: #1d1d1f; }
    
    /* Пастельные фоны */
    .bg-lilac  { background-color: rgba(245, 243, 255, 0.8); } 
    .bg-green  { background-color: rgba(240, 253, 244, 0.8); } 
    .bg-blue   { background-color: rgba(239, 246, 255, 0.8); } 
    .bg-yellow { background-color: rgba(255, 251, 235, 0.8); } 
    .bg-red    { background-color: rgba(254, 242, 242, 0.8); } 
    
    .daily-budget { font-size: 12px; color: #555; background: rgba(255,255,255,0.6); padding: 4px 8px; border-radius: 8px; display: inline-block;}
    </style>
""", unsafe_allow_html=True)

# --- ИНИЦИАЛИЗАЦИЯ ДАННЫХ ---
if 'budget' not in st.session_state:
    st.session_state.budget = {
        "🧺 Продукты и Хозтовары": {"limit": 4000, "spent": 0},
        "📚 Доп. уроки": {"limit": 2254, "spent": 0},
        "⚽ Спорт и Секции": {"limit": 1000, "spent": 0},
        "🍼 Лео (Малыш)": {"limit": 1000, "spent": 0},
        "🏥 Здоровье и Аптека": {"limit": 500, "spent": 0},
        "🚗 Машина (Бензин)": {"limit": 350, "spent": 0},
        "👗 Арина (Личное)": {"limit": 100, "spent": 0},
        "👕 Натан (Личное)": {"limit": 100, "spent": 0},
        "🎮 Досуг и мелочи": {"limit": 40, "spent": 0},
        "🏠 Машканта": {"limit": 5700, "spent": 0},
        "💳 Кредиты": {"limit": 2540, "spent": 0},
        "🏛 Арнона": {"limit": 1700, "spent": 0},
        "⚡ Электричество": {"limit": 600, "spent": 0},
        "📱 Телефон + интернет": {"limit": 600, "spent": 0},
        "🏥 Больничная касса": {"limit": 350, "spent": 0},
        "💧 Вода": {"limit": 200, "spent": 0},
        "🎨 Кружки детей": {"limit": 1000, "spent": 0},
    }
if 'history' not in st.session_state:
    st.session_state.history = []

total_limit = sum(data['limit'] for data in st.session_state.budget.values())
total_spent = sum(data['spent'] for data in st.session_state.budget.values())
total_left = total_limit - total_spent

# --- ФУНКЦИЯ ЗАПИСИ В GOOGLE ТАБЛИЦУ ---
def save_expense(category, amount):
    if amount > 0:
        try:
            clean_cat = category.split(" ", 1)[1] if " " in category else category
            df_sheet = conn.read(worksheet="Data", ttl=0)
            new_row = pd.DataFrame([{"Category": clean_cat, "Spent": amount, "Carryover": ""}])
            updated_df = pd.concat([df_sheet, new_row], ignore_index=True)
            conn.update(worksheet="Data", data=updated_df)
            
            st.session_state.budget[category]['spent'] += amount
            st.session_state.history.insert(0, f"➖ {clean_cat}: <span style='color:#ff3b30; font-weight:600;'>-{amount} ₪</span>")
            st.success("✅ Записано!")
            return True
        except Exception as e:
            st.error(f"Ошибка таблицы: {e}")
            return False

# --- 1. DASHBOARD (БАЛАНС СЕМЬИ) ---
st.markdown(f"""
<div class="glass-card" style="display: flex; justify-content: space-around; padding: 15px;">
    <div class="stat-box"><div class="stat-title">Бюджет</div><div class="stat-value">{total_limit} ₪</div></div>
    <div class="stat-box"><div class="stat-title">Потрачено</div><div class="stat-value red">{total_spent} ₪</div></div>
    <div class="stat-box"><div class="stat-title">Остаток</div><div class="stat-value green">{total_left} ₪</div></div>
</div>
""", unsafe_allow_html=True)

# --- 2. ГРАФИК И ДАТА ---
col_cal, col_chart = st.columns([1, 1.8])
with col_cal:
    st.markdown("<div class='glass-card' style='height: 98%; padding: 10px; text-align: center;'>", unsafe_allow_html=True)
    st.date_input("Дата", today, label_visibility="collapsed")
    st.markdown(f"<div style='margin-top:20px; color:#777; font-size:14px;'>До конца месяца:<br><b style='font-size:24px; color:#1d1d1f;'>{days_left}</b> дней</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart:
    st.markdown("<div class='glass-card' style='height: 98%; padding: 5px;'>", unsafe_allow_html=True)
    df_data = [{"Категория": cat.split(" ", 1)[1] if " " in cat else cat, "Сумма": data['spent']} for cat, data in st.session_state.budget.items() if data['spent'] > 0]
    if not df_data:
        df_data.append({"Категория": "Ждем траты", "Сумма": 1})
        fig = px.pie(pd.DataFrame(df_data), values='Сумма', names='Категория', hole=0.75, color_discrete_sequence=['#f3f4f6'])
    else:
        fig = px.pie(pd.DataFrame(df_data), values='Сумма', names='Категория', hole=0.7, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textinfo='percent', hoverinfo='label+value', textfont_size=11)
    fig.update_layout(showlegend=True, legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.0, font_size=10), margin=dict(t=0, b=0, l=0, r=0), height=180)
    fig.add_annotation(text=f"<b>{total_spent} ₪</b>", x=0.5, y=0.5, font_size=18, showarrow=False, font_color="#ff3b30")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. БЫСТРОЕ ДОБАВЛЕНИЕ (ULTRA QUICK EXPENSE) ---
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<div class='env-header' style='margin-bottom:10px;'>⚡ Добавить расход</div>", unsafe_allow_html=True)

q_col1, q_col2, q_col3 = st.columns([2, 1, 1])
with q_col1:
    sel_cat = st.selectbox("Категория", list(st.session_state.budget.keys()), label_visibility="collapsed")
with q_col2:
    manual_amount = st.number_input("Сумма", min_value=0, step=1, format="%d", label_visibility="collapsed")
with q_col3:
    if st.button("Сохранить", type="primary", use_container_width=True):
        if save_expense(sel_cat, manual_amount):
            st.rerun()

st.markdown("<div style='font-size:12px; color:#777; margin-top:10px; margin-bottom:5px;'>Быстрые суммы:</div>", unsafe_allow_html=True)
b_col1, b_col2, b_col3, b_col4 = st.columns(4)
if b_col1.button("+ 20 ₪", use_container_width=True):
    if save_expense(sel_cat, 20): st.rerun()
if b_col2.button("+ 50 ₪", use_container_width=True):
    if save_expense(sel_cat, 50): st.rerun()
if b_col3.button("+ 100 ₪", use_container_width=True):
    if save_expense(sel_cat, 100): st.rerun()
if b_col4.button("+ 200 ₪", use_container_width=True):
    if save_expense(sel_cat, 200): st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- 4. КОНВЕРТЫ И УМНЫЙ БЮДЖЕТ ---
st.markdown("<p style='font-size:18px; font-weight:700; margin-left:10px; margin-top:20px; color:#1d1d1f;'>📂 Ваши конверты</p>", unsafe_allow_html=True)

bg_colors = ["bg-lilac", "bg-green", "bg-blue", "bg-yellow", "bg-red"]
c_idx = 0

for cat, data in st.session_state.budget.items():
    limit = data['limit']
    spent = data['spent']
    left = limit - spent
    percent = int((spent / limit) * 100) if limit > 0 else 0
    
    # Расчет умного бюджета (если лимит > 1000 и это не база типа машканты, считаем дневной бюджет)
    daily_allowance = int(left / days_left) if days_left > 0 and left > 0 else 0
    
    # Цветная индикация бюджета (Зеленый -> Желтый -> Красный)
    bar_color = "#34c759" if percent < 75 else "#ffcc00" if percent < 90 else "#ff3b30"
    
    parts = cat.split(" ", 1)
    icon = parts[0] if len(parts) > 1 else "💳"
    name = parts[1] if len(parts) > 1 else cat
    bg = bg_colors[c_idx % len(bg_colors)]
    c_idx += 1
    
    daily_html = f"<div class='daily-budget'>Можно тратить: <b>{daily_allowance} ₪</b> / день</div>" if limit > 0 and left > 0 and "Машканта" not in name and "Кредиты" not in name else ""
    
    st.markdown(f"""
    <div class="envelope-card {bg}">
        <div class="env-header">
            <div><span style="font-size: 22px; margin-right:8px;">{icon}</span> {name}</div>
            <div style="font-size: 18px;">{left} ₪</div>
        </div>
        <div style="width: 100%; background-color: rgba(0,0,0,0.05); border-radius: 10px; height: 8px; margin-top: 5px;">
            <div style="width: {min(percent, 100)}%; background-color: {bar_color}; height: 8px; border-radius: 10px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px;">
            <div style="font-size: 12px; color: #777;">Потрачено: {spent} из {limit} ₪ ({percent}%)</div>
            {daily_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. ПОДВАЛ (ИСТОРИЯ И ПЕРЕВОДЫ) ---
st.divider()
col_hist, col_trans = st.columns(2)

with col_hist:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    with st.expander("📝 История операций", expanded=False):
        if st.session_state.history:
            for item in st.session_state.history[:15]:
                st.markdown(f"<div style='font-size:14px; margin-bottom:8px; border-bottom:1px solid #eee; padding-bottom:4px;'>{item}</div>", unsafe_allow_html=True)
        else:
            st.write("Пока пусто.")
    st.markdown("</div>", unsafe_allow_html=True)
            
with col_trans:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    with st.expander("⇄ Перевод между конвертами", expanded=False):
        with st.form("transfer_form", clear_on_submit=True):
            clean_names = [cat.split(" ", 1)[1] if " " in cat else cat for cat in st.session_state.budget.keys()]
            from_name = st.selectbox("Откуда", clean_names, key="from")
            to_name = st.selectbox("Куда", clean_names, key="to")
            transfer_amount = st.number_input("Сумма (₪)", min_value=0, step=1)
            
            if st.form_submit_button("Перевести", use_container_width=True) and transfer_amount > 0 and from_name != to_name:
                from_cat = next(cat for cat in st.session_state.budget.keys() if from_name in cat)
                to_cat = next(cat for cat in st.session_state.budget.keys() if to_name in cat)
                
                st.session_state.budget[from_cat]['limit'] -= transfer_amount
                st.session_state.budget[to_cat]['limit'] += transfer_amount
                st.session_state.history.insert(0, f"⇄ Перевод: из {from_name} в {to_name} <span style='color:#34c759; font-weight:600;'>+{transfer_amount} ₪</span>")
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
