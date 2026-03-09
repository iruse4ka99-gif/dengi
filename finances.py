import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ДИЗАЙН КАК НА МАКЕТЕ
st.markdown("""
    <style>
    /* Фон и шрифты */
    .stApp { background-color: #0e1117; color: white; }
    
    /* Центральный круг */
    .main-circle-container { text-align: center; padding: 20px; position: relative; }
    .main-circle {
        width: 180px; height: 180px; border-radius: 50%;
        background: radial-gradient(closest-side, #0e1117 85%, transparent 86% 100%),
        conic-gradient(#ff4b2b var(--p), #262730 0);
        display: flex; align-items: center; justify-content: center;
        margin: auto; border: 2px solid #333; box-shadow: 0 0 20px rgba(255, 75, 43, 0.2);
    }
    .circle-text { font-size: 32px; font-weight: bold; text-align: center; }

    /* Конверты-виджеты */
    .env-box {
        background: #1a1c24; border-radius: 15px; padding: 15px;
        border-top: 4px solid var(--color); margin-bottom: 10px;
        text-align: center; position: relative; transition: 0.3s;
    }
    .env-box:hover { transform: translateY(-5px); background: #252833; }
    .env-label { font-size: 12px; color: #888; margin-bottom: 5px; }
    .env-val { font-size: 20px; font-weight: bold; margin: 5px 0; }
    .env-pct { font-size: 10px; opacity: 0.7; }

    /* Фиксированные счета с замочком */
    .lock-box {
        background: #16181d; border-radius: 10px; padding: 10px;
        border: 1px solid #333; display: flex; align-items: center; gap: 10px; margin-bottom: 5px;
    }
    .lock-icon { color: #4facfe; }

    /* Поле ввода */
    .stTextInput>div>div>input { background-color: #1a1c24 !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ ИЗ ТАБЛИЦЫ
if 'data' not in st.session_state:
    st.session_state.data = {
        "fixed": {"Ипотека": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1400, "Больница": 350},
        "flexible": {
            "Продукты": {"bal": 4000, "lim": 4000, "color": "#4caf50"},
            "Уроки": {"bal": 1850, "lim": 1850, "color": "#4facfe"},
            "Машина": {"bal": 1365, "lim": 1365, "color": "#ff9800"},
            "Одежда": {"bal": 1000, "lim": 1000, "color": "#f44336"},
            "Памперсы": {"bal": 450, "lim": 450, "color": "#9c27b0"},
            "Животные": {"bal": 200, "lim": 200, "color": "#00bcd4"},
            "Красота": {"bal": 335, "lim": 335, "color": "#e91e63"},
            "Разное": {"bal": 2300, "lim": 2300, "color": "#607d8b"}
        },
        "history": []
    }

# ВЕРХНЯЯ ПАНЕЛЬ: ТАЮЩИЙ КРУГ
income = 18000
total_now = sum(e['bal'] for e in st.session_state.data['flexible'].values())
pct = int((total_now / income) * 100)

st.markdown(f"""
    <div class="main-circle-container">
        <div class="main-circle" style="--p: {pct}%">
            <div class="circle-text">{pct}%<br><span style="font-size:12px; font-weight:normal; color:#888;">ОСТАТОК</span></div>
        </div>
        <p style="margin-top:10px;">Осталось {total_now} ₪ из {income}</p>
    </div>
    """, unsafe_allow_html=True)

# ФИКСИРОВАННЫЕ СЧЕТА (С ЗАМОЧКОМ)
st.write("### 🔒 Фиксированные счета")
f_cols = st.columns(len(st.session_state.data['fixed']))
for i, (name, val) in enumerate(st.session_state.data['fixed'].items()):
    with f_cols[i]:
        st.markdown(f'<div class="lock-box"><span class="lock-icon">🔒</span><div style="font-size:11px;">{name}<br><b>{val} ₪</b></div></div>', unsafe_allow_html=True)

# КОНВЕРТЫ (ГИБКИЕ ТРАТЫ)
st.write("---")
st.write("### 📂 Твои Конверты")
rows = [list(st.session_state.data['flexible'].items())[i:i+4] for i in range(0, 8, 4)]
for row in rows:
    cols = st.columns(4)
    for i, (name, d) in enumerate(row):
        usage_pct = int((d['bal']/d['lim'])*100)
        with cols[i]:
            st.markdown(f"""
                <div class="env-box" style="--color: {d['color']}">
                    <div class="env-label">{name}</div>
                    <div class="env-val">{int(d['bal'])} ₪</div>
                    <div class="env-pct">{usage_pct}% осталось</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"⋮ Свойства", key=f"btn_{name}"):
                st.session_state.target = name

# ИИ ВВОД
st.write("---")
with st.form("ai_form", clear_on_submit=True):
    vvod = st.text_input("Напиши (например: кола 10 или мясо 50)")
    if st.form_submit_button("ЗАПИСАТЬ ТРАТУ"):
        try:
            parts = vvod.split()
            word, amt = parts[0].lower(), float(parts[1])
            # Умный поиск
            target = "Разное"
            for n in st.session_state.data['flexible']:
                if word in n.lower(): target = n; break
            
            st.session_state.data['flexible'][target]['bal'] -= amt
            st.session_state.data['history'].insert(0, f"🕒 {datetime.datetime.now().strftime('%H:%M')} | {word}: -{amt} ₪")
            st.rerun()
        except: st.error("Пиши: название сумма")

# ИСТОРИЯ
if st.session_state.data['history']:
    with st.expander("📜 Последние операции"):
        for h in st.session_state.data['history'][:5]:
            st.write(h)
