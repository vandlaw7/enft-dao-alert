from datetime import datetime, timezone

from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)

import requests
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from my_package.polling_bot import token, chat_id, receive_poll_answer, start_telegram_poll
from my_package.nft_assset_check import headers, my_string, get_query, check_prices


def enftAlert(request):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(PollAnswerHandler(
        receive_poll_answer))  # 투표 결과는 receive_poll_answer 이 함수의 votes_dict로 저장해두면 좋을 것 같아서 print구문 넣어뒀습니다ㅠㅠ

    # Start the Bot
    updater.start_polling()

    print(my_string)
    result = get_query(my_string)
    print(result)

    for i in range(len(result['orders'])):
        print(f'{i}번째 매물')
        token_id_deland = result['orders'][i]['tokenId']
        decentral_land_contract_id = '0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d'
        price_check_url = f'https://api.nftbank.ai/estimates-v2/estimates/{decentral_land_contract_id}/{token_id_deland}?chain_id=ETHEREUM'
        r3 = requests.get(price_check_url, headers=headers)
        estimated_result = json.loads(r3.text)
        if len(estimated_result['data']) != 0:
            nft_bank_estimate = int(estimated_result['data'][0]['estimate'][0]['estimate_price'])
            # print('nft 뱅크 추정가')
            # print(nft_bank_estimate)
            now_price = int(result['orders'][i]['price']) / pow(10, 18)
            # print('매도 호가')
            # print(now_price)
            if nft_bank_estimate > now_price * 1.1:
                start_telegram_poll(updater, dispatcher, token_id_deland)