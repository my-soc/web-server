import time
from elasticsearch import Elasticsearch, helpers
from engines.logging import log_debug, log_info, log_error
from engines.constants import CONNECTORS_INDEX, ORDER_INDEX, WATCHLIST_INDEX, CANDLE_INDEX, \
    POSITION_INDEX, PRICE_INDEX, QUOTE_INDEX, ORDER_DOC, WATCHLIST_DOC, CANDLE_DOC, \
    POSITION_DOC, PRICE_DOC, QUOTE_DOC, SAMPLE_CANDLES, SAMPLE_PRICES, SAMPLE_QUOTES, ELASTICSEARCH


class Database:

    # Constructor
    def __init__(self):
        pass

    # Class Attributes
    ES = Elasticsearch(ELASTICSEARCH)

    # Static Methods
    @staticmethod
    def load_sample_data(data: str):
        try:
            if data == "prices":
                Database.ES.indices.delete(index="sample_prices", ignore=404)
                Database.ES.indices.create(
                    index="sample_prices",
                    body={
                        'mappings': {},
                        'settings': {},
                    },
                    ignore=400
                )
                helpers.bulk(
                    Database.ES,
                    SAMPLE_PRICES,
                    index="sample_prices"
                )
                log_debug(f"New {data} sample data created")
                return True

            elif data == "candles":
                Database.ES.indices.delete(index="sample_candles", ignore=404)
                Database.ES.indices.create(
                    index="sample_candles",
                    body={
                        'mappings': {},
                        'settings': {},
                    },
                    ignore=400
                )
                helpers.bulk(
                    Database.ES,
                    SAMPLE_CANDLES,
                    index="sample_candles"
                )
                log_debug(f"a new {data} sample data created")
                return True

            elif data == "qoutes":
                Database.ES.indices.delete(index="sample_qoutes", ignore=404)
                Database.ES.indices.create(
                    index="sample_qoutes",
                    body={
                        'mappings': {},
                        'settings': {},
                    },
                    ignore=400
                )
                helpers.bulk(
                    Database.ES,
                    SAMPLE_QUOTES,
                    index="sample_qoutes"
                )
                log_debug(f"a new {data} sample data created")
                return True

            else:
                return False

        except Exception as e:
            log_error(e)
            return False

    @staticmethod
    def delete_sample_data(data: str):
        try:
            if data == "prices":
                Database.ES.indices.delete(index="sample_prices", ignore=404)
                log_debug(f"{data} sample data deleted")
                return True

            elif data == "candles":
                Database.ES.indices.delete(index="sample_candles", ignore=404)
                log_debug(f"{data} sample data deleted")
                return True

            elif data == "qoutes":
                Database.ES.indices.delete(index="sample_qoutes", ignore=404)
                log_debug(f"{data} sample data deleted")
                return True

            else:
                return False

        except Exception as e:
            log_error(e)
            return False

    @staticmethod
    def get_docs(index: str, query: object = None):
        try:
            res = Database.ES.search(index=index)
            results = []
            for result in res['hits']['hits']:
                results.append({
                    'id': result['_id'],
                    'content': result['_source']['content']
                })
            return {
                "data": results,
                "total": res['hits']['total']['value'],
            }
        except Exception as e:
            log_error(e)

    @staticmethod
    def store_doc(index: str, data: object):
        doc_id = int(round(time.time() * 1000))
        try:
            res = Database.ES.index(index=index, id=doc_id, body=data)
            return {
                "index": res['_index'],
                "id": res['_id'],
                "result": res['result']
            }
        except Exception as e:
            log_error(e)

    @staticmethod
    def delete_doc(index: str, doc_id: str):
        try:
            res = Database.ES.delete(index=index, id=doc_id)
            return {
                "index": res['_index'],
                "id": res['_id'],
                "result": res['result']
            }
        except Exception as e:
            log_error(e)