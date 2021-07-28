# enft-dao-alert
## polling_bot.py
+ Purpose : Notifying NFTs undervalued on the market to DAO members whether to buy or not.
+ Function :

  +  start_telegram_poll(updater, dispatcher, data, chat_id)
  
      1. Check whether the gap satisfies a (predefined) certain condition for a trade such as purchase (or sale) by comparing the specific NFT price on current market and the estimated price by NFT Bank.
      2. Specify how much undervalued (or depreciated) the NFT is through telegram bot if that condition is satisfied.
    
      3. Inform the remaining ETH investment in the current DAO, and Initiate a vote on whether to buy (or sell, in the case of NFTs DAO already has)
    
    
       <br>
       <h4>Voting Example in Telegram</h4>
       <img src="https://github.com/vandlaw7/enft-dao-alert/blob/master/for-readme/capture_polling_bot.jpg" width="250">
  
