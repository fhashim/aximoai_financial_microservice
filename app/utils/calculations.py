import numpy as np
from scipy.optimize import root_scalar
from scipy.optimize import minimize, root_scalar

def get_proft_commission_amt_psx(buy_price: float, sell_price: float, num_shares: int, day_trade: bool = False):
    if buy_price <= 4.99:
        buy_commission = num_shares * 0.03
    else:
        buy_commission_fixed = 0.05 * num_shares
        buy_commission_percentage = ((0.15/100) * buy_price) * num_shares
        buy_commission = max(buy_commission_fixed, buy_commission_percentage)
    buy_commission_taxed = buy_commission * 1.15

    if sell_price <= 4.99:
        sell_commission = num_shares * 0.03
    else:
        sell_commission_fixed = 0.05 * num_shares
        sell_commission_percentage = ((0.15/100) * sell_price) * num_shares
        sell_commission = max(sell_commission_fixed, sell_commission_percentage)
    sell_commission_taxed = sell_commission * 1.15

    buy_cdc_handling_charges = num_shares * 0.005
    sell_cdc_handling_charges = num_shares * 0.005
    buy_cvt = (0.01/100) *  (buy_price * num_shares)

    if day_trade:
        total_cost = sell_commission_taxed 
    else:
        total_cost = buy_commission_taxed + sell_commission_taxed + buy_cdc_handling_charges + sell_cdc_handling_charges

    profit = (sell_price - buy_price) * num_shares - total_cost

    return profit, total_cost

def get_optimal_sell_price_psx(target_profit: float, buy_price: float, num_shares: int, day_trade: bool = False):
    def profit_difference(sell_price):
        profit, _ = get_proft_commission_amt_psx(buy_price, sell_price, num_shares, day_trade)
        return profit - target_profit

    from scipy.optimize import root_scalar
    result = root_scalar(profit_difference, bracket=[0, buy_price + 1000], method='brentq')

    if result.converged:
        return result.root
    else:
        raise ValueError("Could not find a valid sell price for the desired profit.")
