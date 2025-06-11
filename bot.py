from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
from db import init_db, is_time_available, save_appointment

import asyncio
import nest_asyncio

NAME, DATE, TIME = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Введите ваше имя:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Введите желаемую дату (в формате ГГГГ-ММ-ДД):")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['date'] = update.message.text
    await update.message.reply_text("Введите время (в формате ЧЧ:ММ):")
    return TIME

async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data['name']
    date = context.user_data['date']
    time = update.message.text

    if is_time_available(date, time):
        save_appointment(name, date, time)
        await update.message.reply_text(f"Вы записаны на {date} в {time}. Спасибо!")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Это время занято. Попробуйте другое.")
        return TIME

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Запись отменена.")
    return ConversationHandler.END

async def run_bot():
    init_db()

    app = Application.builder().token("7694207734:AAGcS6RkteqZh1bavWspyeNU455nB98-ZqQ").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    await app.initialize()
    print("Бот инициализирован")
    await app.start()
    print("Бот запущен")
    await app.updater.start_polling()
    print("Ожидание сообщений...")

    # Просто ждём прерывания
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Получен сигнал остановки...")

    print("Останавливаем бота...")
    await app.updater.stop()
    await app.stop()
    await app.shutdown()
    print("Бот остановлен")


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.run(run_bot())
