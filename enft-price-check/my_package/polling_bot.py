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
    eth_remain = db.collection("public_account").document("public").get().to_dict()["eth_remain"]

    if data['is_buy_poll']:
        questions = ["사요", "사지 마요"]
        print(data)
        underrated_ratio = round(100 * (data['price_est'] - data['price_buy']) / data['price_est'], 2)

        message = updater.bot.send_poll(
            chat_id,
            f'{project} 토큰 아이디 {token_id}번 NFT {underrated_ratio}%만큼 저평가돼 있습니다. '
            f'NFT bank의 가치 추정치는 {price_est} ETH이고, '
            f'현재 매도 호가는 {price_buy} ETH입니다.'
            f'한편, DAO 공동계좌가 보유하고 있는 잔여 ETH는 {eth_remain}입니다.'
            f'구매 여부를 투표해주세요.',
            questions,
            is_anonymous=False
        )
    else:
        questions = ["팔아요", "팔지 마요"]
        mdd = round(100 * (data['price_high'] - data['price_est']) / data['price_high'], 2)
        message = updater.bot.send_poll(
            chat_id,
            f'{data["project"]} 토큰 아이디 {data["token_id"]}번 NFT가 고점 대비 {mdd}%만큼 가치가 하락했습니다.'
            f'NFT bank의 현재 가치 추정치는 {data["price_est"]} ETH이고, '
            f'고점 당시의 가치는 {data["price_est"]} ETH입니다. 판매 여부를 투표해주세요.',
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
