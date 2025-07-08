import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from db import add_task, get_tasks, complete_task
from speech_handler import handle_voice_message

TELEGRAM_USER_ID = 123456789  # Заменить на свой Telegram ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я твой планировщик. Отправь голос или команду.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if text:
        result = add_task(text)
        await update.message.reply_text(f"✅ Задача добавлена: {result}")
    else:
        await update.message.reply_text("⚠️ Используй: /добавить Встреча завтра в 14:00")

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_tasks()
    await update.message.reply_text(result)

async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        task_id = context.args[0]
        result = complete_task(task_id)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("⚠️ Укажи ID задачи. Пример: /завершить 2")

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("добавить", add))
    app.add_handler(CommandHandler("задачи", tasks))
    app.add_handler(CommandHandler("завершить", complete))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice_message))

    app.run_polling()