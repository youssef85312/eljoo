import telebot
from keep_alive import keep_alive

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

آخر_رسالة = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global آخر_رسالة
    msg = bot.send_message(message.chat.id, "أرسل النص الجديد للرسالة:")
    آخر_رسالة = {"chat_id": message.chat.id, "message_id": message.message_id}
    bot.register_next_step_handler(msg, استلام_نص_الزر_الجديد)

def استلام_نص_الزر_الجديد(message):
    النص_الجديد = message.text.strip()
    msg = bot.send_message(message.chat.id, "اكتب نص الزر الجديد:")
    bot.register_next_step_handler(msg, استلام_الرابط_الجديد, النص_الجديد)

def استلام_الرابط_الجديد(message, النص_الجديد):
    نص_الزر_الجديد = message.text.strip()
    msg = bot.send_message(message.chat.id, "اكتب الرابط الجديد:")
    bot.register_next_step_handler(msg, تنفيذ_التعديل_الكامل, النص_الجديد, نص_الزر_الجديد)

def تنفيذ_التعديل_الكامل(message, النص_الجديد, نص_الزر_الجديد):
    الرابط_الجديد = message.text.strip()
    if not الرابط_الجديد.startswith("http"):
        bot.send_message(message.chat.id, "الرابط غير صالح. يجب أن يبدأ بـ http أو https.")
        return
    try:
        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(text=نص_الزر_الجديد, url=الرابط_الجديد)
        markup.add(button)

        bot.edit_message_text(chat_id=آخر_رسالة["chat_id"],
                              message_id=آخر_رسالة["message_id"],
                              text=النص_الجديد,
                              reply_markup=markup)
        bot.send_message(message.chat.id, "تم تعديل الرسالة بالكامل.")
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء التعديل: {e}")

keep_alive()
bot.infinity_polling()