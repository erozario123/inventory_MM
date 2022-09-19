#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

class priceProcess:

    def __init__(self, bid_k, ask_k, bid_A, ask_A, sigma, N, s0=100, total_time=1):
        self.N = N
        self.cur_N = 0
        self.sigma = sigma
        self.dt = total_time/N
        self.price = s0 + np.cumsum(sigma * np.sqrt(self.dt) * np.random.choice([1, -1],  int(total_time / self.dt)))
        self.price = np.insert(self.price, 0, s0)
        self.bid_k = bid_k
        self.ask_k = ask_k
        self.bid_A = bid_A
        self.ask_A = ask_A
        self.mid_price = s0

        self.cash = 0
        self.inventory = 0

    def quote(self, bid, ask):
        bid_spread = self.mid_price - bid
        ask_spread = ask - self.mid_price 

        p_bid = self.bid_A*np.exp(-self.bid_k*bid_spread)*self.dt
        p_ask = self.ask_A*np.exp(-self.ask_k*ask_spread)*self.dt
        bid_hit = (np.random.uniform() < p_bid)
        ask_hit = (np.random.uniform() < p_ask)

        if bid_hit:
            self.inventory += 1
            self.cash -= bid

        if ask_hit:
            self.inventory -= 1
            self.cash += ask

        if self.cur_N < self.N:
            self.cur_N += 1

        return self.state()

    def state(self):
        return self.cash, self.inventory, self.cur_N*self.dt, self.mid_price


if __name__ == "__main__":
    process = priceProcess(1.5, 1.5, 140, 140, 2, 200)
    T = 0
    cash_arr, inventory_arr = [], []
    while T < 1:
        cash, inventory, T, s = process.state()
        cash_arr.append(cash)
        inventory_arr.append(inventory)
        print(f"cash : {cash} inventory : {inventory} T : {T} mid_price : {s}")
        bid = s - 0.5
        ask = s + 0.5
        process.quote(bid, ask)

    fig, ax = plt.subplots()

    ax.plot(cash_arr, color='green')
    ax_inv = ax.twinx()
    ax_inv.plot(inventory_arr, color='orange')
    lines = ax.get_lines() + ax_inv.get_lines()
    ax.legend(lines, ['Cash', 'Inventory'], loc='best')
    plt.show() 
