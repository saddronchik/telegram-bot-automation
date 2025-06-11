from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Введите ваше имя:")

async def main():
    application = ApplicationBuilder().token("7694207734:AAGcS6RkteqZh1bavWspyeNU455nB98-ZqQ").build()
    application.add_handler(CommandHandler("start", start))
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    import nest_asyncio

    nest_asyncio.apply()  # разрешаем вложенные event loops

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
