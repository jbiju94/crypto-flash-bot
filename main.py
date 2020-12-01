from binance_api import BinanceAPI

if __name__ == '__main__':
    binance = None
    try:

        binance = BinanceAPI()
        pair = 'ETH_BTC'
        # pair = input("Enter Trade Pair: ")
        print("\n=============================================\n")

        asset = pair.split("_")[0]
        quote = pair.split("_")[1]
        binance.start_session(asset, quote)

    except (KeyboardInterrupt, SystemExit):
        if binance is not None:
            binance.dump_position()


#import cProfile
#cProfile.run('foo()')