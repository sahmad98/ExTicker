#/usr/bin/env python

from random import Random
from time import sleep
from matplotlib import pyplot

last_hundred = []
random = Random()
data = []
arbitrage = [0,0,0,0,0]

fig, ax = pyplot.subplots()
pyplot.ion()

def print_tick(price, increasing):
    if increasing:
        print '\033[92m ^ %0.4f' % price
    else:
        print '\033[91m v %0.4f' % price
    print '\033[2A'
    data.append(price)

def weighted_arbitrage(data):
    length = len(data)
    result = 0
    if length < 50:
        return 0
    for i in xrange(length - 10, length - 2):
        result += (data[i + 1] - data[i])
    return -result

def save_data(price, increasing):
    data.append(price)
    ax.clear()
    ax.plot(range(len(data)), data)
    pyplot.pause(0.005)

def compute_tick(mean, var):
    return random.gauss(mean, var)

def compute_price(initial_price, number_of_iterations, interval, tick_callback):
    last_price = initial_price
    current_price = initial_price
    increasing = False

    for i in xrange(number_of_iterations):
        tick = compute_tick(0.6, 1)
        arbitrage = weighted_arbitrage(data)
        last_price = current_price
        if arbitrage < 0.0:
            current_price = current_price + 0.1 * tick * random.gauss(-arbitrage, 1)
        else:
            current_price = current_price + 0.1 * tick * random.gauss(arbitrage, 1)
        if current_price >= last_price:
            increasing = True
        else:
            increasing = False
        if interval >= 0.1:
            sleep(interval)
        for callback in tick_callback:
            callback(current_price, increasing)
    print '\033[0m'


def main():
    compute_price(50, 1000, 0.0, [save_data, print_tick])


if __name__ == '__main__':
    main()
