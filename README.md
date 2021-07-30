# enft-dao-alert
This project is implemented by serverless system. 
The packages and main.py file is deployed by GCP cloud function. 
Every noon, A GCP scheduler calls enftAlert function in main.py.

## polling_bot.py
+ Purpose : Notifying NFTs undervalued on the market to DAO members whether to buy or not.
+ Function :

  +  start_telegram_poll(updater, dispatcher, data, chat_id)
  
      1. This function is called by check_prices function in nft_asset_check.py and 
      update_est_prices in nft_holdings_update.py. Argument 'data' is made by these functions.
      2. The poll message specifies how much undervalued (or depreciated) the NFT is through telegram bot 
      if that condition is satisfied.
      3. The poll message also informs the remaining ETH investment in the current DAO, and Initiate a vote on whether to buy 
      (or sell, in the case of NFTs DAO already has)
      4. Poll answers ale handled by pollHandle function in main.py using webhook.
    
    
       <br>
       <h4>Voting Example in Telegram</h4>
       <img src="https://github.com/vandlaw7/enft-dao-alert/blob/master/for-readme/capture_polling_bot.jpg" width="250">
  
## nft_asset_check.py
+ Purpose : Checking NFTs undervalued on the market sale. Triggering telegram poll for purchase.
+ Function :
        
  +  check_prices(updater, dispatcher)
      1. Using graphQL subgraph, we can get on sale data of NFTs.
      updatedAt_gt:{yesterday_time}} means that we call objects which are updated within one day.
      2. Checking whether the gap satisfies a (predefined) certain condition for purchase 
      by comparing the specific NFT price on current market and the estimated price of NFT Bank.
      3. If the condition is satisfied, this function triggers a telegram poll.
      
## nft_holdings_update.py
+ Purpose : Checking NFT holdings which price is crushed during recent days. Triggering telegram poll for selling.
+ Function :
        
  +  update_est_prices(updater, dispatcher)
      1. For every nft holdings in a DAO, this function updates estimated price by NFTbank. 
      Also, it records price_high, which means the most expensive estimated value  
      since the DAO bought that NFT.
      2. Checking whether the gap satisfies a (predefined) certain condition for purchase 
      by comparing now estimated price and the price_high.
      3. If the condition is satisfied, this function triggers a telegram poll.
      
      
## main.py
+ Purpose : In main.py we call the functions explained above, 
    and handle the poll answers and accept requests about DAO register 
    and governance variables adjustment.
+ Function :
        
  +  enftAlert(updater, dispatcher)
      1. Calls check_prices function in nft_asset_check.py
      2. Calls update_est_prices function in nft_holdings_update.py
      
  +  pollHandle()
      1. Using telegram webhook, the telegram answers become post requests to this pollHandle function.
      2. When the poll is made, we set the quorum of poll. For every consent answer, this function add 
      gov_token value. If gov_token value exceeds the quorum, This function buys or sells NFT of the poll.
      And then, we updates pending list and holdings list and transaction list.
      3. The buy/sell code will be replaced by solidity code or web3 code in near future.
      
  +  daoSetting()
      1. Variables about DAO, for example telegram chat id, governance token distribution, 
      governance variables will be saved in database.
      2. This part will be will be replaced by solidity code or web3 code in near future.
    