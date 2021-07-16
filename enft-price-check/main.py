from telegram.ext import (
    Updater,
    PollAnswerHandler,
)

from my_package.polling_bot import token, receive_poll_answer
from my_package.nft_assset_check import check_prices

import json
import telegram
import logging

# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}

def configure_telegram():
    """
    Configures the bot with a Telegram Token.
    Returns a bot instance.
    """

    TELEGRAM_TOKEN = token
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)


def enftAlert(request):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(PollAnswerHandler(
        receive_poll_answer))

    updater.start_polling()
    updater.idle()

    check_prices(updater, dispatcher)


def pollHandle(request):
    """ Runs the Telegram webhook """
    print(request)
    print(request.data)
    return "Hello, World/n"
