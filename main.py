import random
import sys

import questionary
from questionary import Choice

from settings import *
from config import ACCOUNTS
from utils.sleeping import sleep


def get_module():
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("1) Make bridge to Scroll", deposit_scroll),
            Choice("2) Make withdraw to Ethereum Sepolia", withdraw_scroll),
            Choice("2) Make swap on Uniswap", swap_uniswap),
            Choice("3) Multiswap", multiswap),
            Choice("4) Exit", "exit"),
        ],
        qmark="🛠 ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
        print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
        sys.exit()
    return result


def main(module):
    if RANDOM_WALLET:
        random.shuffle(ACCOUNTS)

    for j, key in enumerate(ACCOUNTS):

        module(j + 1, key)

        if j + 1 < len(ACCOUNTS) and IS_SLEEP:
            sleep(SLEEP_FROM, SLEEP_TO)


if __name__ == '__main__':
    print("❤️ Subscribe to me – https://t.me/sybilwave\n")

    module = get_module()
    main(module)

    print("\n❤️ Subscribe to me – https://t.me/sybilwave\n")
    print("🤑 Donate me: 0x00000b0ddce0bfda4531542ad1f2f5fad7b9cde9")
