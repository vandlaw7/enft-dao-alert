from sqlalchemy import null

transactionRepository = [
    {
        'nftAddress': 'nft0013',
        'source': 'decentralland',
        'type': 'land',
        'status': 'bought',
        'buyPrice': 3,
        'sellPrice': null,
        'holdingPeriod': null,
        'boughtDate': '1991-01-01',
        'soldDate': null,
    },

    {
        'nftAddress': 'nft0014',
        'source': 'BAYC',
        'type': 'avatar',
        'status': 'sold',
        'buyPrice': 2,
        'sellPrice': 2.5,
        'holdingPeriod': 1,
        'boughtDate': '1993-03-03',
        'soldDate': '1993-03-04',
    },
]
