"""
Problem 2: Coin Change  (DYNAMIC PROGRAMMING)
=============================================
Goal : Using a FIXED set of coin denominations, make up a target amount with
       the MINIMUM number of coins.
Coins: 1, 5, 10, 20, 50 cents  (fixed - the user cannot change them).
Input: the user only chooses the target amount.

DP   : dp[a] = fewest coins to make amount a.
       Recurrence:  dp[a] = 1 + min over each coin c<=a of dp[a-c]
       Optimal substructure : the best way to make `a` is one coin plus the
                              best way to make the smaller amount `a-c`.
       Overlapping subproblems : the same dp[a-c] values are reused many
                              times, so each amount is solved only once.

All core logic (the DP table + reconstruction) is written manually.
Run directly:  python3 problem2_coin_change.py
"""

from ui import paint, box, section, table, read_int

# Fixed denominations (cents). Kept in descending order for a tidy summary.
COINS = [50, 20, 10, 5, 1]


def coin_change_dp(coins, amount):
    """
    Bottom-up DP for the minimum-coin problem.

    Returns: (min_coins, combination, dp, choice)
      * min_coins   = fewest coins (0 when amount is 0)
      * combination = list of coins actually used
      * dp          = the DP value table (dp[a] = fewest coins for a)
      * choice      = choice[a] = a coin used to reach amount a (or -1)
    """
    INF = float("inf")
    dp = [INF] * (amount + 1)        # dp[a] = fewest coins for amount a
    choice = [-1] * (amount + 1)     # choice[a] = a coin used to reach a
    dp[0] = 0                        # base case: 0 coins make amount 0

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and dp[a - coin] + 1 < dp[a]:
                dp[a] = dp[a - coin] + 1
                choice[a] = coin

    # With a 1-cent coin present every amount is reachable, but we stay safe.
    if dp[amount] == INF:
        return None, [], dp, choice

    combination = []
    remaining = amount
    while remaining > 0:
        combination.append(choice[remaining])
        remaining -= choice[remaining]
    return dp[amount], combination, dp, choice


def group_combination(combination):
    """Turn [50,20,20,5] into '1 x 50c + 2 x 20c + 1 x 5c'."""
    counts = {}
    for coin in combination:
        counts[coin] = counts.get(coin, 0) + 1
    return "  +  ".join(f"{counts[c]} x {c}c" for c in COINS if c in counts)


def run():
    print(section("🪙 Problem 2 · Coin Change  (Dynamic Programming)"))
    print("Fixed coin denominations (cents): "
          + paint(", ".join(f"{c}c" for c in COINS), "1"))

    amount = read_int("\nEnter the amount to make (in cents): ", minimum=0)

    min_coins, combination, dp, choice = coin_change_dp(COINS, amount)

    # Show the DP table so the overlapping-subproblem decomposition is visible.
    if amount <= 30:
        rows = [[str(a), str(dp[a])] for a in range(amount + 1)]
        print(paint("\nDP table  dp[a] = fewest coins to make amount a:", "1"))
        print(table(["amount", "dp[a]"], rows))

    print("\nMinimum coins to make " + paint(f"{amount}c", "1") + ": "
          + paint(str(min_coins), "1"))
    if combination:
        print("Coins used: " + paint(group_combination(combination), "1"))
        # Show the recurrence chain (proof of optimal substructure).
        print(paint("\nHow dp[amount] was built (optimal substructure):", "1"))
        a = amount
        while a > 0:
            c = choice[a]
            print(f"  dp[{a}] = dp[{a - c}] + 1 = {dp[a - c]} + 1 = {dp[a]}   (use {c}c)")
            a -= c
        print("  dp[0] = 0   (base case)")


if __name__ == "__main__":
    print(box(["🪙 Problem 2 · Coin Change (Dynamic Programming)"]))
    run()
