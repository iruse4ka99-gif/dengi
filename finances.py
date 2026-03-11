import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
import calendar

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="Наш кошелёк", layout="wide", initial_sidebar_state="collapsed")

# --- МАТЕМАТИКА ДНЕЙ ---
today = datetime.date.today()
_, last_day = calendar.monthrange(today.year, today.month)
days_left = last_day - today.day + 1

# --- ЧИСТЫЙ ДИЗАЙН LIQUID GLASS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    
    .glass-card {
        background: rgba(255, 255, 255, 0.7); 
        border-radius: 20px; 
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px); 
        -webkit-backdrop-filter: blur(10px); 
        border: 1px solid rgba(255, 255, 255, 0.8);
        padding: 15px; 
        margin-bottom: 15px;
    }
    
    .stat-box { text-align: center; width: 32%; display: inline-block; }
    .stat-title { font-size: 10px; color: #666; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;}
    .stat-value { font-size: 20px; font-weight: 700; color: #1d1d1f; }
    .red-text { color: #ff3b30 !important; } 
    .green-text { color: #34c759 !important; }

    .envelope-card { padding: 16px; border-radius: 18px; margin-bottom: 12px; border: 1px solid rgba(0,0,0,0.02); }
    .env-header { display: flex; justify-content: space-between; align-items: center; font-weight: 600; font-size: 16px; }
    
    .bg-1 { background-color: rgba(245, 243, 255, 0.9); } 
    .bg-2 { background-color: rgba(240, 253, 244, 0.9); } 
    .bg-3 { background-color: rgba(239, 246, 255, 0.9); } 
    </style>
""", unsafe_allow_html=True)

# --- ЛИМИТЫ (КАК МЫ РАСПРЕДЕЛИЛИ) ---
BUDGET_LIMITS = {
    "🧺 Продукты и Хозтовары": 4000,
    "📚 Доп. уроки": 60,
    "🚗 Машина (Бензин)": 350,
    "🍼 Лео (Малыш)": 300,
    "🏥 Здоровье и Аптека": 200,
    "👗 Арина (Личное)": 100,
    "👕 Натан (Личное)": 100,
    "🏠 Машканта": 5700,
    "💳 Кредиты": 2540,
    "🎨 Кружки детей": 2000,
    "🏛 Арнона": 1700,
    "⚡ Электричество": 600,
    "📱 Телефон + интернет": 600,
    "🏥 Больничная касса": 350,
    "💧 Вода": 200
}

# --- ИНИЦИАЛИЗАЦИЯ ДАННЫХ ---
if 'budget' not in st.session_state:
    st.session_state.budget = {cat: {"limit": lim, "spent": 0} for cat, lim in BUDGET_LIMITS.items()}
if 'history' not in st.session_state:
    st.session_state.history = []

total_limit = sum(data['limit'] for data in st.session_state.budget.values())
total_spent = sum(data['spent'] for data in st.session_state.budget.values())
total_left = total_limit - total_spent

# --- ФУНКЦИЯ ЗАПИСИ (ПОКА ЛОКАЛЬНАЯ) ---
def add_expense(cat, amt):
    if amt > 0:
        st.session_state.budget[cat]['spent'] += amt
        st.session_state.history.insert(0, f"➖ {cat}: {amt} ₪")
        return True
    return False

# --- 1. DASHBOARD ---
st.markdown(f"""
<div class="glass-card">
    <div class="stat-box"><div class="stat-title">План</div><div class="stat-value">{total_limit} ₪</div></div>
    <div class="stat-box"><div class="stat-title">Расход</div><div class="stat-value red-text">{total_spent} ₪</div></div>
    <div class="stat-box"><div class="stat-title">Остаток</div><div class="stat-value green-text">{total_left} ₪</div></div>
</div>
""", unsafe_allow_html=True)

# --- 2. КАЛЕНДАРЬ И ГРАФИК ---
col_cal, col_chart = st.columns([1, 1.8])
with col_cal:
    st.markdown("<div class='glass-card' style='height: 190px; text-align: center;'>", unsafe_allow_html=True)
    st.date_input("Дата", today, label_visibility="collapsed")
    st.markdown(f"<div style='margin-top:20px; color:#777;'>До конца месяца:<br><b style='font-size:24px; color:#1d1d1f;'>{days_left}</b> дн.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_chart:
    st.markdown("<div class='glass-card' style='height: 190px; padding: 5px;'>", unsafe_allow_html=True)
    df_data = [{"Cat": c.split(" ", 1)[-1], "Val": d['spent']} for c, d in st.session_state.budget.items() if d['spent'] > 0]
    if not df_data:
        fig = px.pie(values=[1], names=["Ждем траты"], hole=0.7, color_discrete_sequence=['#f3f4f6'])
    else:
        fig = px.pie(pd.DataFrame(df_data), values='Val', names='Cat', hole=0.7, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=160)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. БЫСТРАЯ ЗАПИСЬ + СУПЕР СУММЫ ---
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<p style='font-weight:700; margin-bottom:10px;'>⚡ Внести расход</p>", unsafe_allow_html=True)
c1, c2 = st.columns([2,1])
sel_cat = c1.selectbox("Категория", list(st.session_state.budget.keys()), label_visibility="collapsed")
manual_amt = c2.number_input("Сумма", min_value=0, step=10, label_visibility="collapsed")

if st.button("ЗАПИСАТЬ", use_container_width=True, type="primary"):
    if add_expense(sel_cat, manual_amt): st.rerun()

st.markdown("<div style='display: flex; gap: 5px; margin-top:10px;'>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
if col_a.button("+20", use_container_width=True): 
    if add_expense(sel_cat, 20): st.rerun()
if col_b.button("+50", use_container_width=True): 
    if add_expense(sel_cat, 50): st.rerun()
if col_c.button("+100", use_container_width=True): 
    if add_expense(sel_cat, 100): st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# --- 4. КОНВЕРТЫ ---
colors = ["bg-1", "bg-2", "bg-3"]
for i, (cat, data) in enumerate(st.session_state.budget.items()):
    lim, spnt = data['limit'], data['spent']
    rem = lim - spnt
    per = min(int((spnt/lim)*100), 100) if lim > 0 else 100
    b_color = "#ff3b30" if rem < 0 else "#34c759"
    bg = colors[i % 3]
    
    st.markdown(f"""
    <div class="envelope-card {bg}">
        <div class="env-header"><span>{cat}</span><span class="{'red-text' if rem < 0 else ''}">{rem} ₪</span></div>
        <div style="width:100%; background:rgba(0,0,0,0.05); height:6px; border-radius:3px; margin:10px 0;">
            <div style="width:{per}%; background:{b_color}; height:6px; border-radius:3px;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:11px; color:#555;">
            <span>Цель: {lim}</span><span>{int(rem/days_left) if rem > 0 else 0} ₪ / день</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. ПОДВАЛ ---
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
with st.expander("📝 История трат", expanded=False):
    for h in st.session_state.history[:10]: st.write(h)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
with st.expander("⇄ Перевод", expanded=False):
    with st.form("tr_f"):
        f = st.selectbox("Откуда", list(st.session_state.budget.keys()))
        t = st.selectbox("Куда", list(st.session_state.budget.keys()))
        v = st.number_input("Сумма", min_value=0)
        if st.form_submit_button("Перевести"):
            st.session_state.budget[f]['limit'] -= v
            st.session_state.budget[t]['limit'] += v
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
