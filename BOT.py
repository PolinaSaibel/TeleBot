import telebot
from config import TOKEN, keys
from extensions import PriceConverter, ConvertionException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n ❗Курс может быть не точным.\nПосмотреть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text ='\n'.join((text,key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) > 3:
            raise ConvertionException('Слишком много параметров')
        if len(values) < 3:
            raise ConvertionException ('Недостаточно параметров.')

        quote, base, amount = values
        total_base = PriceConverter.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользоватееля\n{e}")

    except Exception as e:
        bot.reply_to(message, f"не удалось обработать команду\n {e}")
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)





bot.polling()