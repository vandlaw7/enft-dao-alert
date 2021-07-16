# """
# 이 서비스는, NFT를 pendingNFTRepository에 등록 및 업데이트 하는 서비스임.
# 1. 투표가 1건 날라옴. 만일 pendingNFTRepository에 없으면 (즉, 첫번째 승인 투표이면) 등록하고, 있으면 승인 토큰 업데이트
# 	2. 업데이트했는데 승인 토큰이 과반수 기준인 buyLimitTokenAmt보다 더 많다? 그러면 구매.
# 		3. 구매 되면, (1)pendingRepository에서 삭제하고, (2)transaction & holdingNFTlist로 올라감, (3)pA 업데이트
#
# 	(논의 사항 : 투표하는 동안 NFTbank 에서 추정한 value가 변하면?..)
# 	: Daniel 님한테 업데이트 주기 여쭤볼게요!
#
# 창우님..
# 투표 결과 받아오실 때
# 1. 어떤 프로젝트인지 (예 : decenralland 혹은 BAYC , ...)
# 2. 아이템이 어떤 type 인 지,(land냐 avatar냐..)
# 3. 얼마에 올라왔는 지(3Eth)
# 4. 얼마로 추정하였는 지
# 받아와야 합니다~
#
# """
#
#
# from datetime import datetime
# from member.memberRepository import memberRepository
# from transaction.transactionRepository import transactionRepository
#
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
#
# # db Setup
# cred = credentials.Certificate("./serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# db = firestore.client()
#
# # (더미) 투표결과가 날라옴(1건마다 옴)
# voteRes = dict({
#     'telegramId': 123123,
#     'nftId': 'nft0010',
#     'answer': 'buy',
#     'source': 'decentralland',
#     'type': 'land',
#     'salePrice': 3,
#     'estPrice': 4
# })
#
# pendings_docs = db.collection('nft_pendings')
# for doc in pendings_docs:
#
# nftlist = []
# for item in pendingNFTRepository:
#     nftlist.append(item['nftAddress'])
#
# updateTokenAmt = None
# for mem in memberRepository:
#     if mem['telegramId'] == voteRes['telegramId']:
#         updateTokenAmt = mem['numTokenBalance']
#         break
#
#
# def poll_handle(request):
#     """
#      만일 투표를 했는데 그 순간 구매에 필요한 거버넌스 토큰을 넘어버리면 바로 승인 프로세스(approvalProcess).
#     그리고 transactionRepository에 구매기록으로 남음.
#     """
#
#     if (voteRes['nftId'] in nftlist) & (voteRes['answer'] == 'buy'):
#         for item in pendingNFTRepository:
#             if item['nftAddress'] == voteRes['nftId']:
#                 item['approvalTokenAmt'] += updateTokenAmt
#
#                 if item['approvalTokenAmt'] > item['buyLimitTokenAmt']:
#                     approvalProcess()
#                     # !!!!!!!!!!!!!! 그리고 투표 또한 쓸데없이 더 안하게 종료시켜버려야 함.!!!!!!!!!!!!!!!!!
#                     break
#
#
#
#
#
# # 다음 코드에 실제 구매 프로세스까지 추가되어야 함 & Repository와 관련된 코드는 실제 DB에 sql로 날려야함!
# def approvalProcess():
#     idx = 0
#     for item in pendingNFTRepository:
#         if item['nftAddress'] == voteRes['nftId']:
#             # (1)pendingRepository에서 삭제. 실제로는 delete SQL을 날려야 함!!
#             pendingNFTRepository.pop(idx)
#             # (2)transactionRepository & holdingNFTRepository로 올라감,실제로는 INSERT SQL을 날려야 함!!
#             transactionRepository.append(
#                 {
#                     'nftAddress': item['nftAddress'],
#                     'source': voteRes['source'],
#                     'type': voteRes['type'],
#                     'status': 'bought',
#                     'buyPrice': voteRes['salePrice'],
#                     'sellPrice': null,
#                     'holdingPeriod': null,
#                     'boughtDate': datetime.now().strftime("%Y-%m-%d"),
#                     'soldDate': null,
#                 }
#             )
#
#             holdingNFTRepository.append(
#                 {
#                     'nftAddress': 'nft0015',
#                     'source': 'decentralland',
#                     'type': 'land',
#                     'buyPrice': voteRes['salePrice'],
#                     'estPrice': voteRes['estPrice'],
#                     'onSale': 'no',
#                 }
#             )
#
#             poll_result = False
#
#             if poll_result:
#                 data = {
#                     'project': 'decentralland',
#                     'project_address': decentral_land_contract_id,
#                     'chain': 'ethereum',
#                     'token_id': token_id_deland,
#                     'price_buy': now_price,
#                     'price_est': nft_bank_estimate,
#                     'on_sale': False
#                 }
#                 db.collection('nft_holdings').add(data)
#
#             # (3)publicAccountRepository 업데이트. 실제로는 UPDATE SQL을 날려야 함!!
#             # 이거 밸런스 체크 무조건 돼있어야 함!!!!!! 중요!!!!!!!!!1
#             publicAccountRepository['remainedETH'] -= voteRes['salePrice']
#             publicAccountRepository['nftHolding'].append(voteRes['nftId'])
#             publicAccountRepository['currentTotalNFTValue'] += voteRes['estPrice']
#             publicAccountRepository['currentTotalBalance'] += voteRes['estPrice']
#
#             break
#         idx += 1
#
#
