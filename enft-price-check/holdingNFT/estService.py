"""
가지고 있는 NFT들의 가치를 일정 주기로 update로 함.

!!! 필요 : DB로 하게 된다면 다음과 같은 코드가 들어갈 것으로 예상됨: !!!

import pymysql
enft_db = pymysql.connect(
    user='root',
    passwd='{설정한 비밀번호}',
    host='127.0.0.1',
    db='enft-db',
    charset='utf8')

cursor = enft_db.cursor(pymysql.cursors.DictCursor)
sql = '''UPDATE holdingNFTRepository
  SET estPrice = 2
  WHERE nftAddress == 'nft0015';'''
cursor.execute(sql)
enft_db.commit()
enft_db.close()
"""

#
import json
from projectAddress import projectAddress
from gql.transport import requests
from holdingNFT.holdingNFTRepository import holdingNFTRepository
from apscheduler.schedulers.blocking import BlockingScheduler

# 구글 스케줄러 쓰면 해결될 것 같지만 일단 스케쥴러 생성
sched = BlockingScheduler()

# NFTbank.ai 로부터 EST value 받기
nftbankApi = 'b8bb9504e550e732265f08434414b8dd'
headers = {'x-api-key': nftbankApi}


# estPrice 업데이트 함수
def updateEstPrice():
    idx = 0
    for item in holdingNFTRepository:
        price_check_url = f'https://api.nftbank.ai/estimates-v2/estimates/{projectAddress[item["source"]]}/{item["nftAddress"]}?chain_id=ETHEREUM'
        r3 = requests.get(price_check_url, headers=headers)
        estimated_result = json.loads(r3.text)
        nftbankEstValue = int(estimated_result['data'][0]['estimate'][0]['estimate_price'])

        # DB에 nftbank 추정치 업데이트 하는 것임 !!!!! 따라서
        # !!!!!!!!!이 update 부분은, 이 파일 상단의 SQL로 교체해야함!!!!!!!!!!!!!!!
        holdingNFTRepository[idx]['estPrice'] = nftbankEstValue

        idx += 1


# 스케쥴러 세팅 및 작동(600초마다 돼있지만, nftbank.ai 에서 업데이트 하는 주기랑 맞추면 될 듯)
sched.add_job(updateEstPrice, 'interval', seconds=600)
sched.start()
