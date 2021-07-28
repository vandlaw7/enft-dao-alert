# enft-dao-alert
## polling_bot.py
+ Purpose : Notifying NFTs undervalued on the market to DAO members whether to buy or not.
+ Function :

  +  start_telegram_poll(updater, dispatcher, data, chat_id)
  
    1. 프로젝트 내 특정 NFT 가격과 NFT Bank Estimation Price와 비교하여 그 gap이 구매 판매와 같은 행위를 위한 특정 predefined condition 을 만족하는 지 체크
    
    2. 그 condition을 만족할 경우, 얼마나 undervalued( or 가치가 하락) 되어있는 지 명시
    
    3. 현재 DAO에서 남아있는 ETH 투자금을 알려주며, 구매 (보유하고 있는 NFT의 경우, 판매) 여부 투표
    
    !https://github.com/vandlaw7/enft-dao-alert/blob/master/for-readme/capture_polling_bot.jpg
    
    
