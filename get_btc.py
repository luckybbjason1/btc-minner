from get_wallet import get_wallet

if __name__ == "__main__":
    for i in range(10):
        wallet = get_wallet('main')
        print(wallet)