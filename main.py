from binance_api import BinanceAPI

if __name__ == '__main__':
    binance = None
    try:
        #pair = 'BTCUSDT'
        binance = BinanceAPI()
        print("\n=============================================\n")
        pair = input("Enter Trade Pair: ")

        binance.start_session(pair)
    except (KeyboardInterrupt, SystemExit):
        if binance is not None:
            binance.dump_position()


#import cProfile
#cProfile.run('foo()')