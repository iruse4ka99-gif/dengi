import streamlit as st
import datetime

st.set_page_config(page_title="Выход в Ноль", layout="wide")

# ДИЗАЙН: ЧЕРНЫЙ НЕОН (Как в NotebookLM)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main-circle {
        width: 170px; height: 170px; border-radius: 50%;
        background: radial-gradient(closest-side, #0e1117 85%, transparent 86% 100%),
        conic-gradient(#ff4b2b var(--p), #262730 0);
        display: flex; align-items: center; justify-content: center;
        margin: auto; border: 2px solid #333; box-shadow: 0 0 15px rgba(255, 75, 43, 0.2);
    }
    .env-card {
        background: #1a1c24; border-radius: 12px; padding: 12px;
        border-top: 4px solid var(--c); margin-bottom: 8px; text-align: center;
    }
    .lock-box {
        background: #16181d; border-radius: 8px; padding: 8px;
        border: 1px solid #333; display: flex; align-items: center; gap: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# ДАННЫЕ СТРОГО ИЗ ТВОЕЙ ТАБЛИЦЫ
if 'db' not in st.session_state:
    st.session_state.db = {
        "fixed": {"Ипотека": 5700, "Кредиты": 2540, "Кружки": 1000, "Счета": 1400, "Здоровье": 350},
        "envs": {
            "Продукты": {"b": 4000, "l": 4000, "c": "#4caf50"},
            "Доп. уроки": {"b": 1850, "l": 1850, "c": "#4facfe"},
            "Машина": {"b": 1365, "l": 1365, "c": "#ff9800"},
            "Одежда": {"b": 1000, "l": 1000, "c": "#f44336"},
            "Личные": {"b": 500, "l": 500, "c": "#9c27b0"},
            "Памперсы": {"b": 450, "l": 450, "c": "#e91e63"},
            "Подарки": {"b": 500, "l": 500, "c": "#ffeb3b"},
            "Животные": {"b": 200, "l": 200, "c": "#00bcd4"},
            "Еда вне дома": {"b": 500, "l": 500, "c": "#8bc34a"},
            "Красота": {"b": 335, "l": 335, "c": "#ff4081"},
            "Разное": {"b": 1300, "l": 1300, "c": "#607d8b"}
        },
        "log": []
    }

# ВЕРХ: КРУГ С ОСТАТКОМ ЗАРПЛАТЫ
total_left = sum(v['b'] for v in st.session_state.db['envs'].values())
pct = int((total_left / 18000) * 100)
st.markdown(f'<div class="main-circle" style="--p:{pct}%"><div style="text-align:center;"><span style="font-size:26px; font-weight:bold;">{int(total_left)} ₪</span><br><span style="font-size:10px;color:#888;">ОСТАТОК</span></div></div>', unsafe_allow_html=True)

# ЗАМОЧКИ (ФИКСИРОВАННЫЕ)
st.write("### 🔒 Постоянные (Заблокировано)")
f_cols = st.columns(5)
for i, (n, v) in enumerate(st.session_state.db['fixed'].items()):
    with f_cols[i % 5]:
        st.markdown(f'<div class="lock-box">🔒 <div style="font-size:10px;color:#888;">{n}<br><b>{v} ₪</b></div></div>', unsafe_allow_html=True)

# КОНВЕРТЫ (11 КАТЕГОРИЙ)
st.write("---")
st.write("### 📂 Твои Конверты")
items = list(st.session_state.db['envs'].items())
for i in range(0, len(items), 4):
    cols = st.columns(4)
    for j, (name, d) in enumerate(items[i:i+4]):
        with cols[j]:
            st.markdown(f'<div class="env-card" style="--c:{d["c"]}"><div style="font-size:11px;color:#888;">{name}</div><div style="font-size:20px;font-weight:bold;">{int(d["b"])} ₪</div><div style="font-size:9px;">из {d["l"]}</div></div>', unsafe_allow_html=True)

# ВВОД
with st.form("tablet_input", clear_on_submit=True):
    txt = st.text_input("Введи расход (например: машина 50)")
    if st.form_submit_button("ЗАПИСАТЬ"):
        try:
            p = txt.split()
            cat, amt = p[0].lower(), float(p[1])
            target = "Разное"
            for n in st.session_state.db['envs']:
                if cat in n.lower(): target = n; break
            st.session_state.db['envs'][target]['b'] -= amt
            st.session_state.db['log'].insert(0, f"{datetime.datetime.now().strftime('%H:%M')} | {cat}: -{amt} ₪")
            st.rerun()
        except: st.error("Пиши: что купила и сколько")
