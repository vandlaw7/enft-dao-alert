import logging

from my_package.global_var import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

token = '1934759690:AAEGnScdQXVXg5uzNmPJuF6aSjeflYgF2Y8'
nft_scanner_id = 1934759690

chat_id = '-443191914'  # 뿌릴 단톡방 id

webhook_endpoint = 'https://us-central1-enft-project.cloudfunctions.net/pollHandle'

''' data에 해당 nft에 대한 정보들을 담아서 보냄 '''


def start_telegram_poll(updater, dispatcher, data, chat_id):
    project, token_id, price_est, price_buy = data["project"], data["token_id"], data["price_est"], data["price_buy"]
    eth_remain = db.collection('dao').document(chat_id).get().to_dict()['eth_remain']

    if data['is_buy_poll']:
        questions = ["Buy", "Don't buy"]
        print('is_buy_poll', chat_id)
        underrated_ratio = round(100 * (data['price_est'] - data['price_buy']) / data['price_est'], 2)

        message = updater.bot.send_poll(
            chat_id,
            f'{project} token ID {token_id} NFT is underrated by {underrated_ratio}%.'
            f'NFT bank estimation is {price_est} ETH, and '
            f'now selling ask price is {price_buy} ETH.'
            f"Meanwhile, our DAO's ETH balance is {eth_remain} ETH."
            f'Please decide whether to buy or not.',
            questions,
            is_anonymous=False
        )
        print("start telegram poll message")
        print(message)
    else:
        questions = ["Sell", "Don't sell"]
        mdd = round(100 * (data['price_high'] - data['price_est']) / data['price_high'], 2)
        message = updater.bot.send_poll(
            chat_id,
            f'{data["project"]} token ID {data["token_id"]} NFT\'s estimate is 20% lower than previous high estimate.'
            f'NFT bank estimation now is {price_est} ETH, and '
            f'price high estimation is {data["price_high"]} ETH. Please decide whether to sell or not. ',
            questions,
            is_anonymous=False
        )

    payload = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.message_id,
            "chat_id": chat_id,
            "answers": 0,
        }
    }

    # 투표 정보가 payload에 담기면, 투표 결과를 저장하기 위해 밑에 핸들러에다가 전달하게 됩니다.
    dispatcher.bot_data.update(payload)

    return message.poll.id


def start_fake_poll(updater, dispatcher):
    questions = ["사요", "사지 마요"]
    message = updater.bot.send_poll(
        chat_id,
        f'투표 기능 체크용입니다. 실제 투표가 아닙니다.',
        questions,
        is_anonymous=False
    )
    payload = {
        message.poll.id: {
            "questions": questions,
            "message_id": message.message_id,
            # "chat_id": update.effective_chat.id,
            "chat_id": chat_id,
            "answers": 0,
        }
    }

    # 투표 정보가 payload에 담기면, 투표 결과를 저장하기 위해 밑에 핸들러에다가 전달하게 됩니다.
    dispatcher.bot_data.update(payload)
