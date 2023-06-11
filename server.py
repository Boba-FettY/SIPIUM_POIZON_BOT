import logging
from telegram.ext import Application, MessageHandler, filters, \
    CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler
from config import BOT_TOKEN
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton, Update, ReplyKeyboardRemove

start_reply_keyboard = [['💰Рассчитать'], ['🔎Информация']]
admin_reply_keyboard = [['💰Рассчитать'], ['🔎Информация'], ['🛠Курс']]
start_markup = ReplyKeyboardMarkup(start_reply_keyboard, one_time_keyboard=False)
admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, one_time_keyboard=False)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
admin_list = [1320663119, 565778929]
logger = logging.getLogger(__name__)


async def start(update, context):
    id_user = update.message.from_user.id
    if id_user in admin_list:
        await update.message.reply_text('Приветствую, хозяин!\n\nВыберите пункт Главного меню ⬇️')
    else:
        await update.message.reply_text(
            "Привет!)\n\n"
            "Этот бот поможет тебе разобраться с расчётом заказа с POIZON\n\n"
            "Здесь ты можешь рассчитать полную стоимость любой вещи с POIZON"
            " от покупки товара на самой площадке, до передачи тебе в руки\n\n"
            "Если у тебя появятся вопросы которые я не смогу решить, обратись"
            " к нашим администраторам, они ответят на любой твой вопрос с 10:00"
            " до 22:00 по МСК:\n\n"
            "@sipium - По вопросам заказа и доставки вещей"
            "@r_out_t - По вопросам сообщества\n\n"
            "Выберите пункт Главного меню ⬇️")


async def money_change(update, context):
    print(111111111111111111111111111111111111111111111111111111111111111111111111111)
    try:
        q = float(update.message.text[1:])
        with open('money.txt', 'w') as mn:
            mn.truncate(0)
        with open('money.txt', 'w') as mn:
            mn.write(update.message.text[1:])
        await update.message.reply_text('Курс был успешно изменён!')
    except Exception:
        pass


async def price(update, context):
    await update.message.reply_text(f'Введите сумму товара:')
    return 1


async def info(update, context):
    await update.message.reply_text(f'Информация 🔍\n\n'
                                    f'Этот бот поможет вам рассчитать точную стоимость'
                                    f' доставки и выкупа желанного товара с площадки POIZON\n\n'
                                    f'Для расчёта доставки Техники обращайтесь в личные'
                                    f' сообщения\n\n@sipium\n@r_out_t')


async def money(update, context):
    with open('money.txt') as dengi:
        kr = dengi.read()
    await update.message.reply_text(f'Действуйщий курс: {kr}')
    id_user = update.message.from_user.id
    if id_user in admin_list:
        keyboard = [[InlineKeyboardButton("⏮", callback_data=f"0"),
                     InlineKeyboardButton("⏪", callback_data=f"1"),
                     InlineKeyboardButton("◀️", callback_data=f"2"),
                     InlineKeyboardButton("▶️", callback_data=f"3"),
                     InlineKeyboardButton("️⏩", callback_data=f"4"),
                     InlineKeyboardButton("️⏭", callback_data=f"5")],

            [InlineKeyboardButton("✅Сменить", callback_data=f"см")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f'Изменить курс {kr}', reply_markup=reply_markup)


async def first(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        keyboard = [
            [
                InlineKeyboardButton("👟Кроссовки", callback_data=f"кр{float(update.message.text)}"),
                InlineKeyboardButton("👕Одежда", callback_data=f"од{float(update.message.text)}"),
            ],
            [InlineKeyboardButton("🕶Аксессуары", callback_data=f"ак{float(update.message.text)}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(f'Какой тип товара вас интересует?', reply_markup=reply_markup)
    except Exception:
        await update.message.reply_text('Неверный формат!')
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def button(update, context):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    if query.data[:2] in ('кр', 'од', 'ак'):
        last_mn = float(query.data[2:])
        omsk = query.data[:2]
        qq = {'кр': 1950, 'од': 1400, 'ак': 900}
        k = 0
        with open('money.txt') as dengi:
            k = dengi.read()
            print(k)
        k = float(k)
        k *= last_mn
        k += qq[omsk]
        k *= 1.04
        k += 950
        obr = {'кр': '👟Кроссовки', 'од': '👕Одежда', 'ак': '🕶Аксессуары'}
        await query.message.reply_text(f"Итоговая цена за ваш товар \n'{obr[omsk]}'  -  {round(k, 2)} ₽")
        await query.delete_message()
    elif query.data in ('0', '1', '2', '3', '4', '5'):
        qwerty = {'0': -1, '1' : -0.1, '2': -0.01, '3': 0.01, '4': 0.1, '5': 1}
        a = float(query.message.text[14:])
        a += qwerty[query.data]
        keyboard = [[InlineKeyboardButton("⏮", callback_data=f"0"),
                     InlineKeyboardButton("⏪", callback_data=f"1"),
                     InlineKeyboardButton("◀️", callback_data=f"2"),
                     InlineKeyboardButton("▶️", callback_data=f"3"),
                     InlineKeyboardButton("️⏩", callback_data=f"4"),
                     InlineKeyboardButton("️⏭", callback_data=f"5")],

                    [InlineKeyboardButton("✅Сменить", callback_data=f"см")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f'Изменить курс {round(a, 2)}', reply_markup=reply_markup)
    elif query.data == 'см':
        try:
            aa = query.message.text[14:]
            with open('money.txt', 'w') as mn:
                mn.truncate(0)
            with open('money.txt', 'w') as mn:
                mn.write(aa)
            await query.edit_message_text('Курс был успешно изменён!')
        except Exception:
            pass


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    conv_hand_change = ConversationHandler(
        entry_points=[CommandHandler('button', button)],

        states={
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, money_change)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('price', price)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_hand_change)
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("money", money))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

    # Регистрируем обработчик в приложении.

    # Запускаем приложение.
    application.run_polling()


if __name__ == '__main__':
    main()
