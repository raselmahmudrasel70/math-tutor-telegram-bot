from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import sympy as sp

TOKEN = "8509202734:AAEebu1jpYNp3geZxremm2GFb0_GeKgllgU"

async def start(update: Update, context):
    msg = (
        "👋 Hi! I'm your Math Tutor Bot 🤖\n\n"
        "তুমি যেকোনো math problem পাঠাও তামিম যেভাবে শিখিয়েছে আমি সেভাবে Solve করব:\n"
        "Example:\n"
        "2+3*4\n"
        "x + 5 = 15\n"
        "integrate x^2\n\n"
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
            "Try Correct math or equation Brooo"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_math))

print("Math Tutor Bot is running...")
app.run_polling()
