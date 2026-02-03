import os
import sympy as sp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

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
    "bsc": "Advanced Math",
}

MODES = {
    "tutor": "🟢 Tutor Mode",
    "exam": "🟡 Exam Mode",
    "fast": "🔵 Fast Mode",
}

# ---------- KEYBOARDS ----------

def class_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("5", callback_data="class_5"),
            InlineKeyboardButton("6", callback_data="class_6"),
            InlineKeyboardButton("7", callback_data="class_7"),
        ],
        [
            InlineKeyboardButton("8", callback_data="class_8"),
            InlineKeyboardButton("9", callback_data="class_9"),
            InlineKeyboardButton("10", callback_data="class_10"),
        ],
        [
            InlineKeyboardButton("SSC", callback_data="class_ssc"),
            InlineKeyboardButton("HSC", callback_data="class_hsc"),
            InlineKeyboardButton("BSC", callback_data="class_bsc"),
        ],
    ])

def mode_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Tutor", callback_data="mode_tutor")],
        [InlineKeyboardButton("🟡 Exam", callback_data="mode_exam")],
        [InlineKeyboardButton("🔵 Fast", callback_data="mode_fast")],
    ])

# ---------- COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "tutor"
    await update.message.reply_text(
        "আসসালামু আলাইকুম 🌸\n\n"
        "আমি Math Tutor Bot 🤖\n\n"
        "📚 তোমার class বেছে নাও:",
        reply_markup=class_keyboard()
    )

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Mode select করো:",
        reply_markup=mode_keyboard()
    )

# ---------- CALLBACKS ----------

async def class_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    level = q.data.replace("class_", "")
    context.user_data["level"] = level
    await q.edit_message_text(
        f"✅ Class set: {level.upper()}\nএখন math problem পাঠাও ✍️"
    )

async def mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    mode = q.data.replace("mode_", "")
    context.user_data["mode"] = mode
    await q.edit_message_text(f"✅ Mode set: {MODES[mode]}")

# ---------- SOLVER ----------

async def solve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "level" not in context.user_data:
        await update.message.reply_text("❗ আগে class select করো (/start)")
        return

    text = update.message.text
    mode = context.user_data.get("mode", "tutor")

    try:
        result = sp.sympify(text)
        if mode == "fast":
            reply = f"✅ {result}"
        elif mode == "exam":
            reply = f"📝 Exam Answer\n{result}"
        else:
            reply = (
                "👨‍🏫 Tutor Explanation\n\n"
                f"{sp.pretty(result)}\n\n"
                f"Final Answer: {result}"
            )
        await update.message.reply_text(reply)
    except:
        await update.message.reply_text("❌ Problem বুঝতে পারিনি")

# ---------- MAIN ----------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mode", mode))

    app.add_handler(CallbackQueryHandler(class_handler, pattern="^class_"))
    app.add_handler(CallbackQueryHandler(mode_handler, pattern="^mode_"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
