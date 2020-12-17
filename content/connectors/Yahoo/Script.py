import urllib3

from lib.common import BaseClient
import lib.mock as wave


# Disable insecure warnings
urllib3.disable_warnings()


''' CONSTANTS '''


CONNECTOR_NAME = 'Alpaca'


'''
Classes
'''


class Client(BaseClient):

    def __init__(self, api_id: str, api_secret: str, base_url: str, verify=False, proxy=False,
                 ok_codes=(200, 201, 204), headers=None, auth=None):
        super(Client, self).__init__(base_url, verify, proxy, ok_codes, headers, auth)
        self.api_id = api_id
        self.api_secret = api_secret
        self.headers = {
            "APCA-API-KEY-ID": api_id,
            "APCA-API-SECRET-KEY": api_id
        }


    def get_clock(self):
        wave.info('Getting Clock Value')
        res = self._http_request(
            "GET",
            url_suffix='/v2/clock',
            resp_type="json",
            headers=self.headers
        )
        return res

    def get_account_information(self):
        wave.info('Getting Account Information')
        res = self._http_request(
            "GET",
            url_suffix='/v2/account',
            resp_type="json",
            headers=self.headers
        )
        return res

    def get_last_trade(self,ticker):
        wave.info('Getting Last Trade Information')
        res = self._http_request(
            "GET",
            url_suffix='/v1/last/stocks/'+ticker,
            resp_type="json",
            headers=self.headers
        )
        return res

    def get_candlesticks(self, ticker, timeframe="1D", limit="100", start=None, end=None, after=None, until=None):
        wave.info('Getting Price Candlesticks')
        params = {
            "symbols": ticker,
            "limit": limit
        }
        if start is not None and after is not None:
            wave.error("Start and After filters cannot be used in one query")
        if until is not None and end is not None:
            wave.error("Until and End filters cannot be used in one query")

        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        if after is not None:
            params['after'] = after
        if until is not None:
            params['until'] = until

        res = self._http_request(
            "GET",
            url_suffix=f'/v1/bars/{timeframe}',
            resp_type="json",
            headers=self.headers,
            params=params
        )
        return res

    def get_last_quote(self, ticker):
        wave.info('Getting Last Quote Information')
        res = self._http_request(
            "GET",
            url_suffix='/v1/last_quote/stocks/'+ticker,
            resp_type="json",
            headers=self.headers
        )
        return res

    def get_orders(self, status=None, limit=None, until=None, after=None, direction=None, nested=None):
        wave.info('Getting Orders Information')
        params = {}

        if status is not None:
            params['status'] = status
        if limit is not None:
            params['limit'] = limit
        if until is not None:
            params['until'] = until
        if after is not None:
            params['after'] = after
        if direction is not None:
            params['direction'] = direction
        if nested is not None:
            params['nested'] = nested

        res = self._http_request(
            "GET",
            url_suffix='/v2/orders',
            resp_type="json",
            headers=self.headers,
            params=params
        )
        return res

    def submit_order(self, status=None, limit=None, until=None, after=None, direction=None, nested=None):
        wave.info('Getting Orders Information')
        params = {}

        if status is not None:
            params['status'] = status
        if limit is not None:
            params['limit'] = limit
        if until is not None:
            params['until'] = until
        if after is not None:
            params['after'] = after
        if direction is not None:
            params['direction'] = direction
        if nested is not None:
            params['nested'] = nested

        res = self._http_request(
            "GET",
            url_suffix='/v2/orders',
            resp_type="json",
            headers=self.headers,
            params=params
        )
        return res


'''
Commands
'''


def test_connector(client):
    res = client.get_clock()
    if res['is_open'] == 'true' or 'false':
        return 'ok'
    else:
        return 'Failed to connect to the API'


def get_account_info(client):
    raw_response = client.get_account_information()

    if raw_response:
        raws = alpaca_ec = raw_response
    else:
        return f'{CONNECTOR_NAME} - Could not find any Accounts'

    context_entry = {
        "Alpaca.Account": alpaca_ec
    }

    human_readable = context_entry
    return [human_readable, context_entry, raws]


def get_last_trade(client, args):
    raw_response = client.get_last_trade(args['ticker'])
    if raw_response:
        raws = raw_response
        alpaca_ec ={
            "Ticker": raw_response['symbol'],
            "Price": raw_response['last']['price'],
            "Size": raw_response['last']['size'],
            "Exchange": raw_response['last']['exchange'],
            "TimeStamp": raw_response['last']['timestamp']
        }
    else:
        return f'{CONNECTOR_NAME} - Could not Get The Last Trade Information'

    context_entry = {
        "Alpaca.Stock.LastTrade(val.Ticker && val.Ticker == obj.Ticker)": alpaca_ec
    }

    human_readable = context_entry
    return [human_readable, context_entry, raws]


def get_candlesticks(client, args):
    raws=[]
    alpaca_ec=[]
    title = f'{CONNECTOR_NAME} - Price Candlesticks'
    raw_response = client.get_candlesticks(timeframe=args.get('timeframe'), ticker=args.get('ticker'), limit=args.get('limit'),
                                           start=args.get('start'), end=args.get('end'), after=args.get('after'),
                                           until=args.get('until'))
    if raw_response:
        for candle in raw_response[args.get('ticker')]:
            raws.append(candle)
            alpaca_ec.append({
                "Time": candle['t'],
                "Open": candle['o'],
                "High": candle['h'],
                "Low": candle['l'],
                "Close": candle['c'],
                "Volume": candle['v']
            })
    else:
        return f'{CONNECTOR_NAME} - Could not Get The CandleSticks'

    context_entry = {
        "Alpaca.Stock.CandleSticks": alpaca_ec
    }

    human_readable = context_entry
    return [human_readable, context_entry, raws]


def get_last_quote(client, args):
    raw_response = client.get_last_quote(args['ticker'])
    if raw_response:
        raws = raw_response
        alpaca_ec ={
            "Ticker": raw_response['symbol'],
            "AskPrice": raw_response['last']['askprice'],
            "AskSize": raw_response['last']['asksize'],
            "AskExchange": raw_response['last']['askexchange'],
            "BidPrice": raw_response['last']['bidprice'],
            "BidSize": raw_response['last']['bidsize'],
            "BidExchange": raw_response['last']['bidexchange'],
            "TimeStamp": raw_response['last']['timestamp']
        }
    else:
        return f'{CONNECTOR_NAME} - Could not Get The Last Quote Information'

    context_entry = {
        "Alpaca.Stock.LastQuote(val.Ticker && val.Ticker == obj.Ticker)": alpaca_ec
    }

    human_readable = context_entry
    return [human_readable, context_entry, raws]


def get_orders(client, args):
    raws=[]
    alpaca_ec=[]
    raw_response = client.get_orders(status=args.get('status'), limit=args.get('limit'), until=args.get('until'),
                                     after=args.get('after'), direction=args.get('direction'), nested=args.get('nested'))
    if raw_response:
        for order in raw_response:
            raws.append(order)
            alpaca_ec.append({
                "OrderID": order.get('id'),
                "SubmitedAt": order.get('submitted_at'),
                "CreatedAt": order.get('created_at'),
                "UpdatedAt": order.get('updated_at'),
                "FilledAt": order.get('filled_at'),
                "Ticker": order.get('symbol'),
                "Quantity": order.get('qty'),
                "FilledQuantity": order.get('filled_qty'),
                "Type": order.get('type'),
                "Side": order.get('side'),
                "TimeInForce": order.get('time_in_force'),
                "LimitPrice": order.get('limit_price'),
                "StopPrice": order.get('stop_price'),
                "FilledAVGPrice": order.get('filled_avg_price'),
                "Status": order.get('status'),
                "ExtendedHours": order.get('extended_hours'),
                "Legs": order.get('legs')
            })
    else:
        return (f'{CONNECTOR_NAME} - No Orders Found',{},{})

    context_entry = {
        "Alpaca.Orders(val.OrderID && val.OrderID == obj.OrderID)": alpaca_ec
    }

    human_readable = context_entry
    return [human_readable, context_entry, raws]


def submit_order(client, args):
    raws=[]
    alpaca_ec=[]
    raw_response = client.submit_order(ticker=args.get('ticker'), quantity=args.get('quantity'), side=args.get('side'),
                                        type=args.get('type'), time_in_force=args.get('time_in_force'),
                                        limit_price=args.get('limit_price'), stop_price=args.get('stop_price'),
                                        extended_hours=args.get('extended_hours')
                                        , client_order_id=args.get('client_order_id'), order_class=args.get('order_class')
                                        , take_profit=args.get('take_profit'), stop_loss=args.get('stop_loss'))
    if raw_response:
        for order in raw_response:
            raws.append(order)
            alpaca_ec.append({
                "OrderID": order.get('id'),
                "SubmitedAt": order.get('submitted_at'),
                "CreatedAt": order.get('created_at'),
                "UpdatedAt": order.get('updated_at'),
                "FilledAt": order.get('filled_at'),
                "Ticker": order.get('symbol'),
                "Quantity": order.get('qty'),
                "FilledQuantity": order.get('filled_qty'),
                "Type": order.get('type'),
                "Side": order.get('side'),
                "TimeInForce": order.get('time_in_force'),
                "LimitPrice": order.get('limit_price'),
                "StopPrice": order.get('stop_price'),
                "FilledAVGPrice": order.get('filled_avg_price'),
                "Status": order.get('status'),
                "ExtendedHours": order.get('extended_hours'),
                "Legs": order.get('legs')
            })
    else:
        return (f'{CONNECTOR_NAME} - No Orders Found',{},{})

    context_entry = {
        "Alpaca.Orders(val.OrderID && val.OrderID == obj.OrderID)": alpaca_ec
    }

    human_readable = context_entry
    return [human_readable, context_entry, raws]


def main():

    params = wave.params()
    api_id = params.get('id')
    api_secret = params.get('secret')
    account_url = params['account_url'][:-1] if (params['account_url'] and params['account_url'].endswith('/')) else params['account_url']
    data_url = params['data_url'][:-1] if (params['data_url'] and params['data_url'].endswith('/')) else params['data_url']

    verify_certificate = not params.get('insecure', False)
    proxy = params.get('proxy', False)

    wave.debug(f'Command being called is {wave.command()}')

    try:
        account_client = Client(
            base_url=account_url,
            verify=verify_certificate,
            proxy=proxy,
            ok_codes=(200, 201, 204),
            headers={'accept': "application/json"},
            api_id=api_id,
            api_secret=api_secret
        )

        data_client = Client(
            base_url=data_url,
            verify=verify_certificate,
            proxy=proxy,
            ok_codes=(200, 201, 204),
            headers={'accept': "application/json"},
            api_id=api_id,
            api_secret=api_secret
        )

        if wave.command() == 'test-connector':
            result = test_connector(account_client)
            wave.results(result)

        elif wave.command() == 'alpaca-get-account-information':
            result = get_account_info(account_client)
            wave.results(*result)

        elif wave.command() == 'alpaca-get-last-trade':
            result = get_last_trade(data_client, wave.args())
            wave.results(*result)

        elif wave.command() == 'alpaca-get-candlesticks':
            result = get_candlesticks(data_client, wave.args())
            wave.results(*result)

        elif wave.command() == 'alpaca-get-last-quote':
            result = get_last_quote(data_client, wave.args())
            wave.results(*result)

        elif wave.command() == 'alpaca-get-orders':
            result = get_orders(account_client, wave.args())
            wave.results(*result)

        elif wave.command() == 'alpaca-submit-order':
            result = submit_order(account_client,args=wave.args())
            wave.results(*result)

    except Exception as e:
        wave.error(str(f'Failed to execute {wave.command()} command. Error: {str(e)}'))


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()