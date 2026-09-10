import telebot
import qrcode
import tempfile
import os

TOKEN = "TOKEN"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "✅ ربات QR Code آماده است!\n\nهر متن یا لینکی بفرست تا QR Code آن را بسازم."
    )


@bot.message_handler(func=lambda m: True)
def generate_qr(message):
    text = message.text.strip()

    if not text:
        bot.reply_to(message, "❌ لطفاً یک متن یا لینک ارسال کن.")
        return

    msg = bot.reply_to(message, "⏳ در حال ساخت QR Code...")

    filename = None

    try:
        # ساخت فایل موقت
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            filename = tmp.name

        # ساخت QR
        img = qrcode.make(text)
        img.save(filename)

        # ارسال عکس
        with open(filename, "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="✅ QR Code ساخته شد."
            )

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.reply_to(message, f"❌ خطا:\n{e}")

    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass


print("🤖 ربات فعال شد...")

bot.infinity_polling(skip_pending=True)
