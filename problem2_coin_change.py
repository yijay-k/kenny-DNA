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

from ui import paint, box, section, table, choose

# Fixed denominations (cents). Kept in descending order for a tidy summary.
COINS = [50, 20, 10, 5, 1]

# Fixed set of amounts the user can choose from (cents). Using a menu instead
# of typed input means there is no invalid data to guard against. Kept small so
# the full DP table (every amount from 0 to the target) fits on screen.
AMOUNTS = [8, 18, 27, 37]


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


def run():
    print(section("🪙 Problem 2 · Coin Change  (Dynamic Programming)"))
    print("Fixed coin denominations (cents): "
          + paint(", ".join(f"{c}c" for c in COINS), "1"))

    print()
    amount = AMOUNTS[choose("Choose an amount to make:",
                            [f"{a}c" for a in AMOUNTS])]

    min_coins, combination, dp, choice = coin_change_dp(COINS, amount)

    print("\nGoal: make " + paint(f"{amount}c", "1")
          + " using the FEWEST coins. The program does this in 2 steps.")

    # --- STEP 1: fill the table for EVERY amount from 0 to the target --------
    print(paint(f"\nSTEP 1 - Work out the fewest coins for every amount from 0 to {amount}.", "1"))
    print(paint("  dp[a]     = fewest coins needed to make amount a", "2"))
    print(paint("  last coin = the coin we added to reach a (remembered for Step 2)", "2"))
    print(paint("  Each amount reuses the smaller amounts already solved above it.", "2"))
    rows = []
    for a in range(amount + 1):
        last = "-" if choice[a] < 0 else f"{choice[a]}c"
        rows.append([str(a), str(dp[a]), last])
    print(table(["amount a", "dp[a]", "last coin"], rows))
    print("So the fewest coins for " + paint(f"{amount}c", "1") + " is "
          + paint(f"dp[{amount}] = {min_coins}", "1") + ".")

    # --- STEP 2: rebuild the actual coins by following 'last coin' -----------
    print(paint(f"\nSTEP 2 - Rebuild the coins by following 'last coin' back from {amount} to 0:", "1"))
    a = amount
    while a > 0:
        c = choice[a]
        print(f"  at {a:>3}c  ->  last coin {c:>2}c  ->  {a - c}c left")
        a -= c
    print(f"  at   0c  ->  done")

    # --- Clear final answer --------------------------------------------------
    coins_str = "  +  ".join(f"{c}c" for c in combination)
    print()
    print(box([
        paint("ANSWER", "1"),
        "",
        f"Fewest coins to make {amount}c : {min_coins}",
        f"Coins used : {coins_str}",
    ]))


if __name__ == "__main__":
    print(box(["🪙 Problem 2 · Coin Change (Dynamic Programming)"]))
    run()
