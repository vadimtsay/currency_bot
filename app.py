import telebot
import babel.numbers

from config import keys, TOKEN, locale
from extensions import ConvertionException, CurrencyConverter
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Конвертер валют\nФормат команды: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nДля просмотра списка валют введите команду /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException('Слишком много параметров')
        elif len(values) < 3:
            raise ConvertionException('Не хватает параметров')
        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = babel.numbers.format_currency(amount, keys[quote], locale=locale.get(keys[quote])) + ' = ' + babel.numbers.format_currency(total_base, keys[base], locale=locale.get(keys[base]))
        bot.send_message(message.chat.id, text)

bot.polling()