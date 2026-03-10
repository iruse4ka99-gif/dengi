import telebot
from telebot import types

# ТОКЕН (уже твой)
TOKEN = '8631895320:AAEYvi_bm5U7SZhClVU0LY4AOS0bPZWcG3Y'
bot = telebot.TeleBot(TOKEN)

# 18 500 - 5700(М) - 2540(К) - 1200(С) - 1000(Круж) = 8060 на остальное
# Распределяем 8060: 4000(П), 2254(Уроки), 100(А), 100(Н), 1000(Лео), 350(Зд), 256(Маш)
categories = {
    "🛒 Продукты": 4000,
    "📚 Доп. уроки": 2254,
    "🏋️ Спорт": 1000,
    "👶 Лео (Малыш)": 1000,
    "🏥 Здоровье": 350,
    "🚗 Машина": 256,
    "👧 Арина": 100,
    "👦 Натан": 100,
}

# Тут храним траты (в реальной базе лучше хранить в файле)
spent = {cat: 0 for cat in categories}
history = []

# Обязательные платежи (для инфо)
FIXED = "🏠 Машканта: 5700\n💳 Кредиты: 2540\n📑 Счета: 1200"

def get_status_emoji(current, limit):
    percent = (current / limit) * 100
    if percent < 50: return "🟢"
    if percent < 85: return "🟡"
    return "🔴"

def main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📊 Состояние", "➕ Внести расход")
    markup.add("🔄 Перевод", "📜 История")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, Ира! Твой Max-Бюджет запущен. 💎", reply_markup=main_markup())

@bot.message_handler(func=lambda m: m.text == "📊 Состояние")
def status(message):
    res = "💳 **ВАШИ КОНВЕРТЫ (АПРЕЛЬ)**\n\n"
    res += f"🔒 **ОБЯЗАТЕЛЬНЫЕ:**\n{FIXED}\n"
    res += "----------------------------------\n"
    
    for cat, limit in categories.items():
        curr = spent[cat]
        emoji = get_status_emoji(curr, limit)
        bar_len = 10
        filled = int((curr / limit) * bar_len) if limit > 0 else 0
        bar = "█" * min(filled, bar_len) + "░" * max(0, bar_length := (bar_len - filled))
        res += f"{emoji} **{cat}**\n`{bar}` {curr}/{limit} ₪\n"
    
    bot.send_message(message.chat.id, res, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "➕ Внести расход")
def add_expense(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for cat in categories.keys():
        markup.add(types.InlineKeyboardButton(cat, callback_data=f"exp_{cat}"))
    bot.send_message(message.chat.id, "Куда тратим?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("exp_"))
def ask_amount(call):
    cat = call.data.split("_")[1]
    msg = bot.send_message(call.message.chat.id, f"Сколько внести в **{cat}**?")
    bot.register_next_step_handler(msg, save_exp, cat)

def save_exp(message, cat):
    try:
        val = float(message.text.replace(',', '.'))
        spent[cat] += val
        history.append(f"➖ {cat}: {val} ₪")
        bot.send_message(message.chat.id, f"✅ Записала {val} ₪ в {cat}")
    except:
        bot.send_message(message.chat.id, "❌ Нужны только цифры!")

@bot.message_handler(func=lambda m: m.text == "🔄 Перевод")
def transfer_start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for cat in categories.keys():
        markup.add(types.InlineKeyboardButton(f"Из {cat}", callback_data=f"from_{cat}"))
    bot.send_message(message.chat.id, "Откуда заберем деньги?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("from_"))
def transfer_to(call):
    source = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup(row_width=1)
    for cat in categories.keys():
        if cat != source:
            markup.add(types.InlineKeyboardButton(f"В {cat}", callback_data=f"to_{source}_{cat}"))
    bot.edit_message_text(f"Забираем из {source}. Куда переложить?", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("to_"))
def transfer_amount(call):
    _, source, target = call.data.split("_")
    msg = bot.send_message(call.message.chat.id, f"Сколько перенести из {source} в {target}?")
    bot.register_next_step_handler(msg, finish_transfer, source, target)

def finish_transfer(message, src, tgt):
    try:
        val = float(message.text.replace(',', '.'))
        categories[src] -= val
        categories[tgt] += val
        bot.send_message(message.chat.id, f"✅ Перевела {val} ₪. Лимит {tgt} увеличен!")
    except:
        bot.send_message(message.chat.id, "❌ Ошибка в сумме.")

@bot.message_handler(func=lambda m: m.text == "📜 История")
def show_hist(message):
    if not history:
        bot.send_message(message.chat.id, "История пока пуста.")
    else:
        bot.send_message(message.chat.id, "\n".join(history[-10:]))

bot.infinity_polling()
