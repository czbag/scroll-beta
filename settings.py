from modules import *

# RANDOM WALLETS MODE
RANDOM_WALLET = False  # True or False

# SLEEP MODE
IS_SLEEP = True  # True or False

SLEEP_FROM = 5  # Second
SLEEP_TO = 10  # Second


def deposit_scroll(account_id, key):
    """
    Deposit from official bridge
    ______________________________________________________
    all_amount - Bridge 90% ETH
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = False

    zksync = Scroll(key, "ethereum", account_id)
    zksync.deposit(min_amount, max_amount, decimal, all_amount)


def withdraw_scroll(account_id, key):
    """
    Deposit from official bridge
    ______________________________________________________
    all_amount - Bridge 90% ETH
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = False

    zksync = Scroll(key, "scroll", account_id)
    zksync.withdraw(min_amount, max_amount, decimal, all_amount)


def swap_uniswap(account_id, key):
    """
    Make swap on Uniswap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, GHO | Select one
    to_token – Choose DESTINATION token ETH, GHO | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - Swap 90% ETH or 100% ANY_TOKEN
    """

    from_token = "ETH"
    to_token = "GHO"

    min_amount = 0.01
    max_amount = 0.02
    decimal = 6
    slippage = 1

    all_amount = False

    pancake = Uniswap(key, account_id)
    pancake.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount)


def multiswap(account_id, key):
    """
    Multi-Swap module: Automatically swap a specified number of times.
    ______________________________________________________
    all_amount - If True, swap 90% ETH to GHO, after swap 100% GHO to ETH
    If False, swap 10-90% ETH to GHO, after swap GHO 10-90% to ETH remaining number of times
    """
    min_swap = 2
    max_swap = 4

    sleep_from = 5
    sleep_to = 10

    slippage = 1

    all_amount = True

    multi = Multiswap(key, account_id)
    multi.swap(sleep_from, sleep_to, min_swap, max_swap, slippage, all_amount)
