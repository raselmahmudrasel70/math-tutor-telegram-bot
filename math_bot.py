import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import sympy as sp

TOKEN = os.environ.get("TOKEN")

async def start(update: Update, context):
    msg = (
        "👋 Hi! I'm your Math Tutor Bot 🤖\n\n"
        "তুমি যেকোনো math problem পাঠাও\n\n"
        "তামিম যেভাবে শিখিয়েছে আমি সেভাবেই Solve করব 🤭\n\n"
     
        "ইংশা আল্লাহ ❤️‍🩹\n\n"
         
        "I will explain step-by-step 📘"
    )
    await update.message.reply_text(msg)

async def solve_math(update: Update, context):
    text = update.message.text
    try:
        result = sp.sympify(text)
        steps = sp.pretty(result)

        reply = (
            f"📘 Step-by-step (Tutor style):\n\n"
            f"{steps}\n\n"
            f"✅ Final Answer:\n"
            f"{result}"
        )
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(
            "❌ Sorry, তুমি কিছু ভুল বলছ...!\n"
            "Try Correct math or equation Brooo 💔"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_math))

print("Math Tutor Bot is running...")
app.run_polling()






