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

# -------- TOKEN --------
TOKEN = os.environ.get("TOKEN")

# -------- DATA --------

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

# -------- COMMANDS --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "tutor"
    await update.message.reply_text(
        "আসসালামু আলাইকুম 🌸\n\n"
        "আমি Premium Math Tutor Bot 🤖\n\n"
        "📚 আগে তোমার class বলো:\n"
        "5 / 6 / 9 / ssc / hsc / bsc"
    )

async def change_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🟢 Tutor Mode", callback_data="mode_tutor")],
        [InlineKeyboardButton("🟡 Exam Mode", callback_data="mode_exam")],
        [InlineKeyboardButton("🔵 Fast Mode", callback_data="mode_fast")],
    ]
    await update.message.reply_text(
        "🎮 Mode select করো:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    mode = query.data.replace("mode_", "")
    context.user_data["mode"] = mode
    await query.edit_message_text(f"✅ Mode changed to:\n{MODES[mode]}")

# -------- LOGIC --------

async def set_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    level = update.message.text.lower().strip()
    if level not in LEVEL_MAP:
        await update.message.reply_text("❌ Invalid class\nUse: 5–10, ssc, hsc, bsc")
        return
    context.user_data["level"] = level
    await update.message.reply_text(
        f"✅ Class set: {level.upper()}\nএখন math problem পাঠাও ✍️"
    )

async def solve_math(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = context.user_data.get("mode", "tutor")
    try:
        result = sp.sympify(text)
        if mode == "fast":
            reply = f"✅ Answer:\n{result}"
        elif mode == "exam":
            reply = f"📝 Exam Style\nProblem: {text}\nAnswer: {result}"
        else:
            reply = (
                "👨‍🏫 Tutor Mode\n\n"
                f"Problem:\n{text}\n\n"
                f"Working:\n{sp.pretty(result)}\n\n"
                f"Final Answer:\n{result}"
            )
        await update.message.reply_text(reply)
    except Exception:
        await update.message.reply_text("❌ Problem বুঝতে পারিনি")

async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "level" not in context.user_data:
        await set_class(update, context)
    else:
        await solve_math(update, context)

# -------- MAIN --------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mode", change_mode))
    app.add_handler(CallbackQueryHandler(mode_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
