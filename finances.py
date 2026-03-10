import telebot
from telebot import types

# Твой токен от BotFather
TOKEN = '8631895320:AAEYvi_bm5U7SZhClVU0LY4AOS0bPZWcG3Y'
bot = telebot.TeleBot(TOKEN)

# Твои настройки конвертов (Лимиты)
budget = {
    "🛒 Продукты": {"limit": 4000, "spent": 0},
    "📚 Доп. уроки": {"limit": 2254, "spent": 0},
    "🏋️ Спорт": {"limit": 1000, "spent": 0},
    "👶 Лео (Малыш)": {"limit": 1000, "spent": 0},
    "🏥 Здоровье": {"limit": 500, "spent": 0},
    "🚗 Машина": {"limit": 350, "spent": 0},
    "👧 Арина": {"limit": 100, "spent": 0},
    "👦 Натан": {"limit": 100, "spent": 0},
    "🎮 Досуг": {"limit": 40, "spent": 0},
}

# Фиксированные платежи (просто для инфо)
FIXED_PAYMENTS = 9156  # Машканта + Кредиты + Счета

# Функция для создания полоски прогресса (Светофор)
def get_progress_bar(spent, limit):
    if limit == 0: return ""
    percent = (spent / limit) * 100
    bar_length = 10
    filled_length = int(bar_length * spent // limit)
    if filled_length > bar_length: filled_length = bar_length
    
    # Логика цвета
    if percent < 50: circle = "🟢"
    elif percent < 85: circle = "🟡"
    else: circle = "🔴"
    
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    return f"{circle} `{bar}` {int(percent)}%"

# Главное меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📊 Мой Бюджет", "➕ Внести расход")
    markup.add("🔄 Перевод", "📜 История")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, Ира! Твое приложение 'Макс-Бюджет' готово. 💎", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "📊 Мой Бюджет")
def show_budget(message):
    text = "💳 **ВАШ БАЛАНС (АПРЕЛЬ)**\n"
    text += f"🔒 Фикс. платежи: `{FIXED_PAYMENTS} ₪` (Оплачено)\n"
    text += "----------------------------------\n"
    
    for cat, data in budget.items():
        bar = get_progress_bar(data['spent'], data['limit'])
        text += f"{cat}\n{bar}  `{data['spent']}/{data['limit']} ₪` \n\n"
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "➕ Внести расход")
def ask_category(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(cat, callback_data=f"add_{cat}") for cat in budget.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выбери конверт для записи:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def process_add(call):
    category = call.data.replace("add_", "")
    msg = bot.send_message(call.message.chat.id, f"Сколько потратила в категорию {category}?")
    bot.register_next_step_handler(msg, save_expense, category)

def save_expense(message, category):
    try:
        amount = float(message.text.replace(',', '.'))
        budget[category]['spent'] += amount
        bot.send_message(message.chat.id, f"✅ Записала {amount} ₪ в {category}!", reply_markup=main_menu())
    except:
        bot.send_message(message.chat.id, "❌ Ошибка! Напиши число цифрами.", reply_markup=main_menu())

# Запуск
print("Бот в стиле Max запущен!")
bot.infinity_polling()
