def maxProfit(max_trades, daily_prices):
    if not daily_prices or max_trades == 0:
        return 0

    buy = [-10**9] * (max_trades + 1)
    sell = [0] * (max_trades + 1)

    for price in daily_prices:
        for t in range(1, max_trades + 1):
            buy[t] = max(buy[t], sell[t-1] - price)
            sell[t] = max(sell[t], buy[t] + price)

    return sell[max_trades]




















# Example 1
#print(maxProfit(2, [2000, 4000, 1000])) 


#Example 2
print(maxProfit(4, [3000, 2000, 7000, 1000, 4000, 5000]))
