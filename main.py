from binance_api import BinanceAPI

if __name__ == '__main__':
    pair = 'BTCUSDT'
    binance = BinanceAPI()

    binance.start_session(pair)

#import cProfile
#cProfile.run('foo()')