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

# ================= TOKEN =================
TOKEN = os.environ.get("TOKEN")

# ================= QUESTION BANK =================
QUESTION_BANK = {
    "5": {
        "addition": [
            {"q": "2 + 3 = ?", "options": ["3", "4", "5", "6"], "answer": "5"},
            {"q": "10 + 5 = ?", "options": ["10", "12", "15", "20"], "answer": "15"},
        ],
        "subtraction": [
            {"q": "10 - 4 = ?", "options": ["5", "6", "7", "8"], "answer": "6"},
        ],
    },
    "ssc": {
        "algebra": [
            {"q": "x + 5 = 10 হলে x = ?", "options": ["2", "3", "5", "10"], "answer": "5"},
            {"q": "2x = 10 হলে x = ?", "options": ["3", "4", "5", "6"], "answer": "5"},
        ],
        "geometry": [
            {"q": "ত্রিভুজের কোণের সমষ্টি কত?", "options": ["90°", "180°", "270°", "360°"], "answer": "180°"},
        ],
    },
}

# ================= KEYBOARDS =================
def class_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Class 5", callback_data="class_5")],
        [InlineKeyboardButton("SSC", callback_data="class_ssc")],
    ])

def topic_keyboard(level):
    topics = QUESTION_BANK[level].keys()
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(t.capitalize(), callback_data=f"topic_{t}")]]
        for t in topics
    )

def mcq_keyboard(options):
    random.shuffle(options)
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(opt, callback_data=f"mcq_{opt}")]]
        for opt in options
    )

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "আসসালামু আলাইকুম 🌸\n\n"
        "আমি Premium Math Tutor Bot 🤖\n\n"
        "📚 প্রথমে Class বেছে নাও:",
        reply_markup=class_keyboard()
    )

# ================= CLASS HANDLER =================
async def class_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    level = q.data.replace("class_", "")
    context.user_data["level"] = level
    await q.edit_message_text(
        f"✅ Class selected: {level.upper()}\n\n📘 এখন Topic বেছে নাও:",
        reply_markup=topic_keyboard(level)
    )

# ================= TOPIC HANDLER =================
async def topic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    topic = q.data.replace("topic_", "")
    context.user_data["topic"] = topic

    questions = QUESTION_BANK[context.user_data["level"]][topic]
    random.shuffle(questions)

    context.user_data["questions"] = questions
    context.user_data["index"] = 0
    context.user_data["score"] = 0

    await q.edit_message_text(
        f"📝 Exam Started!\n\nClass: {context.user_data['level'].upper()}\nTopic: {topic.capitalize()}"
    )
    await send_question(q, context)

# ================= SEND MCQ =================
async def send_question(update, context):
    idx = context.user_data["index"]
    questions = context.user_data["questions"]

    if idx >= len(questions):
        score = context.user_data["score"]
        total = len(questions)
        await update.message.reply_text(
            f"✅ Exam Finished!\n\n🎯 Score: {score}/{total}"
        )
        return

    q = questions[idx]
    await update.message.reply_text(
        f"❓ Q{idx+1}: {q['q']}",
        reply_markup=mcq_keyboard(q["options"])
    )

# ================= ANSWER HANDLER =================
async def mcq_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    idx = context.user_data["index"]
    question = context.user_data["questions"][idx]
    selected = q.data.replace("mcq_", "")

    if selected == question["answer"]:
        context.user_data["score"] += 1
        feedback = "✅ Correct!"
    else:
        feedback = f"❌ Wrong! Correct: {question['answer']}"

    context.user_data["index"] += 1
    await q.edit_message_text(feedback)
    await send_question(q, context)

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(class_handler, pattern="^class_"))
    app.add_handler(CallbackQueryHandler(topic_handler, pattern="^topic_"))
    app.add_handler(CallbackQueryHandler(mcq_handler, pattern="^mcq_"))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
