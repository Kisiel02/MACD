import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os

def eman(N,index, data): #exponential moving average of n
    alfa = 2 / (N+1)
    p = data[index]
    for i in range(1, N + 1):
        tmp = (1-alfa)**i
        p = p + tmp * data[index - i] #numerator
    denominator = 1
    for i in range(1, N + 1):
        denominator = denominator + (1-alfa)**i
    return p / denominator # numerator / denominator


dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'wig20_d.csv') # file with data

file = pd.read_csv(filename)
data = pd.DataFrame(file)

dates = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in file['Data'].values ]
values = file['Zamkniecie'].values

ema12 = [] #exponential moving average 12
ema26 = [] #exponential moving average 26
signal = []

for i in range(26, 1000):               #calculating ema12 and ema26 (from day 27)
    ema12.append(eman(12,i,values))     #ema12
    ema26.append(eman(26,i,values))     #ema26

macd = [a - b for a,b in zip(ema12,ema26)] #calculating MACD

for i in range(9, 974):                #calculating signal
    signal.append(eman(9,i,macd))


macd = macd[9:974]
dates2 = dates[35:1000]

if(signal[0] > macd[0]):
    isSignaHigher = True
else:
    isSignaHigher = False #checks, if at the beggining MACD or Signal is higher

buy = []
sell = [] #lists to store buy and sell days

for i in range(1, len(signal)):
    if(isSignaHigher): #MACD cross Signal from ottom - time to buy
        if(macd[i] >= signal[i]):
            isSignaHigher = False
            buy.append(i)
    else:            #MACD cross Signal from tip - time to sell
        if (macd[i] <= signal[i]):
            isSignaHigher = True
            sell.append(i)


plt.plot(dates[35:1000], values[35:1000], color='red',marker='o',mfc='green', markevery=buy + sell) # original plot with
plt.figure(2)                                                                                       # sell and buy days marked
plt.plot(dates2, signal)
plt.plot(dates2, macd)
plt.legend(["Signal","MACD"])
plt.show()

money = 1000.0
actions = 0.0
if(buy[0] > sell[0]): #Make sure that first action is buying, not selling
    sell.pop(0)

if(len(buy) > len(sell)): #if last action is buying, remove it
    buy.pop(-1)

shouldBuy = True
day = buy.pop(0)  # first element from buy list - a day to buy

for i in range (len(values)):
    if(i == day): #time to buy
        if(shouldBuy):
            actions = money / values[i]
            shouldBuy = False
            day = sell.pop()
        else:
            money = actions * values[i] #action sell
            shouldBuy = True
            day = buy.pop()

print(f"Final money: {money}" )



