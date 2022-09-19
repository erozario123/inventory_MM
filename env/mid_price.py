#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt

class priceProcess:

    def __init__(self, sigma, dt, s0=100, total_time=1):
        self.price_process = [s0]
        
        for _ in range(int(total_time/dt)):
            step = np.random.choice([-1, 1])*np.sqrt(dt)*sigma
            step += self.price_process[-1]
            self.price_process.append(step)


if __name__ == '__main__':
    mid_price = priceProcess(2, 0.00001)
    plt.plot(mid_price.price_process)
    plt.show()
