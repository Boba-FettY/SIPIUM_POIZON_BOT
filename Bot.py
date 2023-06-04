import logging
from telegram.ext import Application, MessageHandler, filters, \
    CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update

start_reply_keyboard = [['💰Рассчитать'], ['🔎Информация']]
admin_reply_keyboard = [['💰Рассчитать'], ['🔎Информация'], ['🛠Курс']]
start_markup = ReplyKeyboardMarkup(start_reply_keyboard, one_time_keyboard=False)
admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, one_time_keyboard=False)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
admin_list = [1320663119, 565778929]
logger = logging.getLogger(__name__)


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message.text == '💰Рассчитать':
        with open('money.txt') as dengi:
            kr = dengi.read()
        await update.message.reply_text(f'Действуйщий курс: {kr}\nВведите сумму товара:')

    elif update.message.text == '🛠Курс' and update.message.from_user.id in admin_list:
        await update.message.reply_text(f'Введите значение валюты\n'
                                        f'в формате "к(значение)":')

    elif update.message.text == '🔎Информация':
        await update.message.reply_text(f'Информация 🔍\n\n'
                                        f'Этот бот поможет вам рассчитать точную стоимость'
                                        f' доставки и выкупа желанного товара с площадки POIZON\n\n'
                                        f'Для расчёта доставки Техники обращайтесь в личные'
                                        f' сообщения\n\n@sipium\n@r_out_t')

    else:
        if update.message.text.isdigit():
            keyboard = [
                [
                    InlineKeyboardButton("👟Кроссовки", callback_data=f"кр{float(update.message.text)}"),
                    InlineKeyboardButton("👕Одежда", callback_data=f"од{float(update.message.text)}"),
                ],
                [InlineKeyboardButton("🕶Аксессуары", callback_data=f"ак{float(update.message.text)}")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(f'Какой тип товара вас интересует?', reply_markup=reply_markup)
        elif update.message.from_user.id in admin_list and update.message.text[0] == 'к':
            try:
                q = float(update.message.text[1:])
                with open('money.txt', 'w') as mn:
                    mn.truncate(0)
                with open('money.txt', 'w') as mn:
                    mn.write(update.message.text[1:])
                await update.message.reply_text('Курс был успешно изменён!')
            except Exception:
                pass


async def start(update, context):
    id_user = update.message.from_user.id
    if id_user in admin_list:
        await update.message.reply_text(
            "Привет!)\n\n"
            "Этот бот поможет тебе разобраться с расчётом заказа с POIZON\n\n"
            "Здесь ты можешь рассчитать полную стоимость любой вещи с POIZON"
            " от покупки товара на самой площадке, до передачи тебе в руки\n\n"
            "Если у тебя появятся вопросы которые я не смогу решить, обратись"
            " к нашим администраторам, они ответят на любой твой вопрос с 10:00"
            " до 22:00 по МСК:\n\n"
            "@sipium - По вопросам заказа и доставки вещей\n"
            "@r_out_t - По вопросам сообщества",
            reply_markup=admin_markup
        )
    else:
        await update.message.reply_text(
            "Привет!\n\n)"
            "Этот бот поможет тебе разобраться с расчётом заказа с POIZON\n\n"
            "Здесь ты можешь рассчитать полную стоимость любой вещи с POIZON"
            " от покупки товара на самой площадке, до передачи тебе в руки\n\n"
            "Если у тебя появятся вопросы которые я не смогу решить, обратись"
            " к нашим администраторам, они ответят на любой твой вопрос с 10:00"
            " до 22:00 по МСК:\n\n"
            "@sipium - По вопросам заказа и доставки вещей"
            "@r_out_t - По вопросам сообщества",
            reply_markup=start_markup
        )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    await query.edit_message_text(text="***Выполнено***")
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
    await query.message.reply_text(f"Итоговая сумма за ваш товар \n'{obr[omsk]}'  -  {k} ₽")
    global money
    money = False


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, search)
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

    # Регистрируем обработчик в приложении.

    # Запускаем приложение.
    application.run_polling()


if __name__ == '__main__':
    main()
