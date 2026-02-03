import os
import random
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

# =================================================
# QUESTION BANK (ALL CLASS + TOPIC)
# =================================================
QUESTION_BANK = {
    "5": {
        "addition": [
            {"q": "2 + 3 = ?", "options": ["3", "4", "5", "6"], "answer": "5"},
            {"q": "7 + 8 = ?", "options": ["12", "13", "14", "15"], "answer": "15"},
        ],
        "subtraction": [
            {"q": "10 − 4 = ?", "options": ["5", "6", "7", "8"], "answer": "6"},
        ],
    },

    "6": {
        "algebra": [
            {"q": "x + 3 = 7 হলে x = ?", "options": ["3", "4", "5", "6"], "answer": "4"},
        ]
    },

    "7": {
        "algebra": [
            {"q": "2x = 10 হলে x = ?", "options": ["3", "4", "5", "6"], "answer": "5"},
        ]
    },

    "8": {
        "linear_equation": [
            {"q": "x − 5 = 0 হলে x = ?", "options": ["0", "3", "5", "10"], "answer": "5"},
        ]
    },

    "9": {
        "geometry": [
            {"q": "ত্রিভুজের কোণের সমষ্টি কত?", "options": ["90°", "180°", "270°", "360°"], "answer": "180°"},
        ]
    },

    "10": {
        "trigonometry": [
            {"q": "sin 90° = ?", "options": ["0", "1", "√3", "½"], "answer": "1"},
        ]
    },

    "ssc": {
        "algebra": [
            {"q": "x + 5 = 10 হলে x = ?", "options": ["3", "4", "5", "6"], "answer": "5"},
        ],
        "geometry": [
            {"q": "বৃত্তের ব্যাসার্ধ r হলে ক্ষেত্রফল = ?", 
             "options": ["πr²", "2πr", "πd", "r²"], "answer": "πr²"},
        ]
    },

    "hsc": {
        "calculus": [
            {"q": "d/dx (x²) = ?", "options": ["x", "2x", "x²", "2"], "answer": "2x"},
        ]
    },

    "bsc": {
        "advanced_math": [
            {"q": "∫ 2x dx = ?", "options": ["x² + C", "2x + C", "x + C", "x³"], "answer": "x² + C"},
        ]
    }
}

MODES = {
    "tutor": "Tutor Mode",
    "fast": "Fast Mode",
    "exam": "Exam Mode (MCQ)"
}

# =================================================
# KEYBOARDS
# =================================================
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

def topic_keyboard(level):
    topics = QUESTION_BANK[level].keys()
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t.replace("_", " ").title(), callback_data=f"topic_{t}")]
        for t in topics
    ])

def mode_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Tutor", callback_data="mode_tutor")],
        [InlineKeyboardButton("Fast", callback_data="mode_fast")],
        [InlineKeyboardButton("MCQ Exam", callback_data="mode_exam")],
    ])

def mcq_keyboard(options):
    random.shuffle(options)
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(o, callback_data=f"mcq_{o}")]] for o in options
    )

# =================================================
# START
# =================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["mode"] = "tutor"
    await update.message.reply_text(
        "আসসালামু আলাইকুম 🌸\n\n"
        "আমি Premium Math Tutor Bot 🤖\n\n"
        "📚 Class বেছে নাও:",
        reply_markup=class_keyboard()
    )

# =================================================
# CLASS / TOPIC / MODE HANDLERS
# =================================================
async def class_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    level = q.data.replace("class_", "")
    context.user_data["level"] = level
    await q.edit_message_text(
        f"✅ Class: {level.upper()}\n\n📘 Topic বেছে নাও:",
        reply_markup=topic_keyboard(level)
    )

async def topic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    topic = q.data.replace("topic_", "")
    context.user_data["topic"] = topic
    await q.edit_message_text(
        f"📘 Topic: {topic.replace('_',' ').title()}\n\n🎮 Mode বেছে নাও:",
        reply_markup=mode_keyboard()
    )

async def mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    mode = q.data.replace("mode_", "")
    context.user_data["mode"] = mode

    if mode == "exam":
        qs = QUESTION_BANK[context.user_data["level"]][context.user_data["topic"]]
        random.shuffle(qs)
        context.user_data["questions"] = qs
        context.user_data["index"] = 0
        context.user_data["score"] = 0
        await q.edit_message_text("📝 MCQ Exam শুরু হচ্ছে...")
        await send_mcq(q, context)
    else:
        await q.edit_message_text(f"✅ Mode set: {MODES[mode]}\n\n✍️ এখন math পাঠাও")

# =================================================
# MCQ LOGIC
# =================================================
async def send_mcq(update, context):
    idx = context.user_data["index"]
    qs = context.user_data["questions"]

    if idx >= len(qs):
        await update.message.reply_text(
            f"✅ Exam Finished!\nScore: {context.user_data['score']}/{len(qs)}"
        )
        return

    q = qs[idx]
    await update.message.reply_text(
        f"❓ Q{idx+1}: {q['q']}",
        reply_markup=mcq_keyboard(q["options"])
    )

async def mcq_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    idx = context.user_data["index"]
    question = context.user_data["questions"][idx]
    selected = q.data.replace("mcq_", "")

    if selected == question["answer"]:
        context.user_data["score"] += 1

    context.user_data["index"] += 1
    await send_mcq(q, context)

# =================================================
# NORMAL SOLVER (Tutor / Fast)
# =================================================
async def solve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "level" not in context.user_data:
        await update.message.reply_text("❗ আগে /start দিয়ে class select করো")
        return

    text = update.message.text
    mode = context.user_data.get("mode", "tutor")

    try:
        result = sp.sympify(text)
        if mode == "fast":
            await update.message.reply_text(f"✅ {result}")
        else:
            await update.message.reply_text(
                f"👨‍🏫 Solution:\n{sp.pretty(result)}\n\nFinal Answer: {result}"
            )
    except:
        await update.message.reply_text("❌ Problem বুঝতে পারিনি")

# =================================================
# MAIN
# =================================================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(class_handler, pattern="^class_"))
    app.add_handler(CallbackQueryHandler(topic_handler, pattern="^topic_"))
    app.add_handler(CallbackQueryHandler(mode_handler, pattern="^mode_"))
    app.add_handler(CallbackQueryHandler(mcq_handler, pattern="^mcq_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
