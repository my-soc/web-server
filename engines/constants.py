import json

CONTENT_PATH = 'content'
VERSION = '1.0'
CONNECTORS_INDEX = f'{CONTENT_PATH}/connectors/index.json'
COMMANDS_INDEX = f'{CONTENT_PATH}/connectors/commands.json'
INSTANCES_INDEX = f'{CONTENT_PATH}/connectors/instances.json'
ENTRIES_INDEX = f'{CONTENT_PATH}/entries/index.json'

SAMPLE_CANDLES = json.load(open('data/sample/candles-1d-1000-crwd.json'))
SAMPLE_PRICES = json.load(open('data/sample/price-spy.json'))
SAMPLE_QUOTES = json.load(open('data/sample/quote-msft.json'))

ORDER_DOC = 'order'
POSITION_DOC = 'position'
WATCHLIST_DOC = 'watchlist'
CANDLE_DOC = 'candle'
PRICE_DOC = 'price'
QUOTE_DOC = 'qoute'

ORDER_INDEX = 'order_index'
POSITION_INDEX = 'position_index'
WATCHLIST_INDEX = 'watchlist_index'
CANDLE_INDEX = 'candle_index'
PRICE_INDEX = 'price_index'
QUOTE_INDEX = 'qoute_index'

ELASTICSEARCH = '192.168.20.20'