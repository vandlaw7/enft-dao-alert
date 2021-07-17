import datetime

data_intersection = {
    'project': 'project',
}
data_holding_unique = {'on_sale': False}
data_transaction_unique = {
    'price_sell': 0,
    'date_buy': datetime.date.today(),
    'data_sell': datetime.date(2100, 12, 31)
}

data_holding = data_intersection.copy()
data_holding.update(data_holding_unique)
data_transaction = data_intersection.copy()
data_transaction.update(data_transaction_unique)

print(data_holding, data_transaction)