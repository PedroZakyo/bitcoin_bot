import json
import ssl

import websocket
import bitstamp.client

import credencias

def cliente():
    return bitstamp.client.Trading(username=credencias.USERNAME,
                                   key= credencias.KEY,
                                    secret= credencias.SECRET)



def comprar (quantidade):
    trading_client = cliente()
    trading_client.buy_market_order(quantidade)

def vender (quantidade):
    trading_client = cliente()
    trading_client.sell_market_order(quantidade)


def on_open(ws):
    print("abriu a coneção")

    json_subscribe = """
    {
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}
    """
    ws.send(json_subscribe)

def on_close(ws):
     print('fechou a coneção')


def message(ws,message):
   message = json.loads(message)
   price = message['data']['price']
   print(price)

   if price > 9000:
       vender()
   elif price < 8000:
       comprar()
   else:
       print('aguardar')


def error(ws,error):
    print('error')
    print(error)

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open=on_open,
                                on_close=on_close,
                                on_error=error,
                                on_message=message)
    ws.run_forever(sslopt={"cert_regs":ssl.CERT_NONE})
