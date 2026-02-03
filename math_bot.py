from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sympy as sp
import os

TOKEN = os.environ.get("TOKEN")

LEVEL_MAP = {
    "5": "Basic Arithmetic & Algebra",
    "6": "Basic Arithmetic & Algebra",
    "7": "Basic Arithmetic & Algebra",
    "8": "Basic Arithmetic & Algebra",
    "9": "Algebra, Geometry & Trigonometry",
    "10": "Algebra, Geometry & Trigonometry",
    "ssc": "Equation & Basic Calculus",
    "hsc": "Equation & Basic Calculus",
    "bsc": "Advanced / Expensive Math",
    "higher": "Advanced / Expensive Math"
}

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Hi! I'm your Math Tutor Bot 🤖\n\n"
        "প্রথমে বলো তুমি কোন class / level এ পড়ো 📚\n\n"
        "Example:\n"
        "5\n6\n9\nssc\nhsc\nbsc"
    )

# Set class
async def set_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level = update.message.text.lower().strip()

    if level not in LEVEL_MAP:
        await update.message.reply_text(
            "❌ এই level টা বুঝতে পারিনি 😅\n"
            "Try: 5–10, ssc, hsc, bsc"
        )
        return

    context.user_data["level"] = level
    context.user_data["topic"] = LEVEL_MAP[level]

    await update.message.reply_text(
        f"✅ Level set: **{level.upper()}** 📘\n"
        f"📚 Topics: {LEVEL_MAP[level]}\n\n"
        "এখন যেকোনো math problem পাঠাও ✍️\n"
        "আমি তোমার level অনুযায়ী teacher-style বুঝাবো 👨‍🏫"
    )

# Solve math
async def solve_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "level" not in context.user_data:
        await update.message.reply_text(
            "❗ আগে তোমার class / level বলো 📚\n"
            "Example: 7 / 9 / ssc / bsc"
        )
        return

    level = context.user_data["level"]
    topic = context.user_data["topic"]
    text = update.message.text

    try:
        result = sp.sympify(text)

        reply = (
            f"👨‍🏫 Tutor Explanation\n"
            f"Level: {level.upper()}\n"
            f"Topic: {topic}\n\n"
            f"✏️ Problem:\n{text}\n\n"
            f"📘 Working:\n{sp.pretty(result)}\n\n"
            f"✅ Final Answer:\n{result}"
        )

        await update.message.reply_text(reply)

    except Exception:
        await update.message.reply_text(
            "❌ এই problem টা parse করতে পারিনি 😅\n"
            "Example:\n"
            "2+3*4\n"
            "x+5=15\n"
            "integrate x^2"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_class))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_math))

    print("Math Tutor Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
