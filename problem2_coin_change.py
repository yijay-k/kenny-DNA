"""
Problem 2: Coin Change  (DYNAMIC PROGRAMMING)
=============================================
Goal : Given coin denominations and a target amount, find the MINIMUM
       number of coins needed to make that amount.
DP   : dp[a] = fewest coins to make amount a.
       Recurrence:  dp[a] = 1 + min over each coin c<=a of dp[a-c]
       Optimal substructure : the best way to make `a` is one coin plus the
                              best way to make the smaller amount `a-c`.
       Overlapping subproblems : the same dp[a-c] values are reused many
                              times, so each amount is solved only once.

Run directly:  python3 problem2_coin_change.py
All core logic (the DP table + reconstruction) is written manually.
"""

from ui import paint, box, section, table, read_int, read_line, ask_run_again


def get_denominations():
    """Prompt for coin denominations, validate, and remove duplicates."""
    while True:
        raw = read_line("Enter coin denominations (comma-separated, e.g. 1,3,4): ")
        parts = [p.strip() for p in raw.split(",") if p.strip() != ""]
        if not parts:
            print(paint("  -> Please enter at least one denomination.", "91"))
            continue
        try:
            coins = [int(p) for p in parts]
        except ValueError:
            print(paint("  -> Invalid input. Use whole numbers separated by commas.", "91"))
            continue
        if any(c <= 0 for c in coins):
            print(paint("  -> All denominations must be positive integers.", "91"))
            continue
        # Remove duplicate denominations so the DP table stays clean.
        unique_coins = []
        for c in coins:
            if c not in unique_coins:
                unique_coins.append(c)
        return unique_coins


def coin_change_dp(coins, amount):
    """
    Bottom-up DP for the minimum-coin problem.

    Returns: (min_coins, combination, dp, choice)
      * min_coins   = fewest coins, or None if the amount cannot be made
      * combination = list of coins actually used (empty if amount is 0)
      * dp          = the full DP value table (dp[a] = fewest coins for a)
      * choice      = choice[a] = a coin used to reach amount a (or -1)
    dp and choice are returned so the caller can show the decomposition.
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

    if dp[amount] == INF:
        return None, [], dp, choice

    # Reconstruct which coins were used by walking the choice[] table back.
    combination = []
    remaining = amount
    while remaining > 0:
        coin_used = choice[remaining]
        combination.append(coin_used)
        remaining -= coin_used

    return dp[amount], combination, dp, choice


def group_combination(combination):
    """Turn [3,3,1] into a readable 'count x coin' summary. Returns a string."""
    counts = {}
    for coin in combination:
        counts[coin] = counts.get(coin, 0) + 1
    # Show larger coins first for readability (manual selection sort on keys).
    keys = list(counts.keys())
    for i in range(len(keys)):
        max_idx = i
        for j in range(i + 1, len(keys)):
            if keys[j] > keys[max_idx]:
                max_idx = j
        keys[i], keys[max_idx] = keys[max_idx], keys[i]
    return "  +  ".join(f"{counts[k]} x {k}" for k in keys)


def recurrence_trace(dp, choice, amount):
    """
    Build the chain showing how dp[amount] decomposes into subproblems,
    e.g. dp[6] = dp[3] + 1 (use coin 3) - the visible proof of optimal
    substructure. Returns a list of printable lines.
    """
    lines = []
    a = amount
    while a > 0:
        c = choice[a]
        lines.append(f"  dp[{a}] = dp[{a - c}] + 1 = {dp[a - c]} + 1 = {dp[a]}   (use coin {c})")
        a -= c
    lines.append("  dp[0] = 0   (base case: no coins needed)")
    return lines


def run():
    print(section("🪙 Problem 2 · Coin Change  (Dynamic Programming)"))
    while True:
        coins = get_denominations()
        amount = read_int("Enter target amount: ", minimum=0)

        min_coins, combination, dp, choice = coin_change_dp(coins, amount)

        # Show the DP table so the overlapping-subproblem decomposition is
        # visible (kept compact for larger amounts).
        if amount <= 30:
            rows = [[str(a), "inf" if dp[a] == float("inf") else str(dp[a])]
                    for a in range(amount + 1)]
            print(paint("\nDP table  dp[a] = fewest coins to make amount a:", "1"))
            print(table(["amount", "dp[a]"], rows))

        if min_coins is None:
            print(paint(f"\nNo combination of {coins} can make up {amount}.", "91"))
        else:
            print("\nMinimum coins needed: " + paint(str(min_coins), "1"))
            if combination:
                print("Combination used: " + paint(group_combination(combination), "1"))
                print(paint("\nOptimal substructure (how dp[amount] was built):", "1"))
                for line in recurrence_trace(dp, choice, amount):
                    print(line)
            else:
                print(paint("Combination used: none (amount is 0)", "2"))

        if not ask_run_again():
            break


if __name__ == "__main__":
    print(box(["🪙 Problem 2 · Coin Change (Dynamic Programming)"]))
    run()
