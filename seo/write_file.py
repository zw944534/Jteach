import io;
import json;
from datetime import datetime;
import ast;
from distutils.file_util import write_file
import matplotlib.pyplot as plt

class writeFile():
    
    def write(self):
        print(type(self))
    # resultDict = dict(pchome=tickets,momo=momos,shopee=shopees,yahoo=yahoos,ruten=rutens,buy123=buy123s)
        pchome = self['pchome']
        momo = self['momo']
        shopee = self['shopee']
        yahoo = self['yahoo']
        ruten = self['ruten']
        buy123 = self['buy123']
        with open("C:/Users/chu/Documents/for nku/paper/testProduct/"+datetime.today().strftime('%Y%m%d%H%M%S')+".txt", 'w',encoding='utf-8') as file:
            file.write(json.dumps(self))
        # fp = io.open("C:/Users/chu/Documents/for nku/paper/testProduct/"+datetime.today().strftime('%Y%m%d')+".txt","ab+")
        # fp.write(json.dumps(self))     
    def read(self):
        dateList = ['20211229','20211230','20220103','20220104']
        pcDict = {}
        momoDict={}
        shopeeDict = {}
        yahooDict = {}
        rutenDict = {}
        buy123Dict = {}
        for date in dateList:
            file = open('C:/Users/chu/Documents/for nku/paper/testProduct/'+date+'.txt','r')
            contents = file.read()       
            dict = ast.literal_eval(contents)
            pchome = dict.get('pchome')
            momo = dict.get('momo')
            shopee = dict.get('shopee')
            yahoo = dict.get('yahoo')
            ruten = dict.get('ruten')
            buy123 = dict.get('buy123')

            pricePC = []
            priceMomo = []
            priceShopee = []
            priceYahoo = []
            priceRuten = []
            priceBuy = []
            
            for i in range(len(pchome)):
                price = pchome[i].get('price')
                if price:
                    if isinstance(price, str):
                        price = price.replace(',','')
                    pricePC.append(int(price))
            for i in range(len(momo)):
                price = momo[i].get('price')
                if price:
                    if isinstance(price,str):
                        price = price.replace(',','')
                    priceMomo.append(int(price))
            for i in range(len(shopee)):
                price = shopee[i].get('price')
                if price:
                    if isinstance(price, str):
                        price = price.replace(',','')
                    priceShopee.append(int(price))
            # for i in range(len(yahoo)):
            #     price = yahoo[i].get('price')
            #     if price:
            #         if isinstance(price, str):
            #             price = price.replace(',','')
            #         priceYahoo.append(int(price))
            # for i in range(len(ruten)):
            #     price = ruten[i].get('price')
            #     if price:
            #         if isinstance(price, str):
            #             price = price.replace(',','')
            #         priceRuten.append(int(price))
            # for i in range(len(buy123)):
            #     price = buy123[i].get('price')
            #     if price:
            #         if isinstance(price, str):
            #             price = price.replace(',','')
            #         priceBuy.append(int(price))
            pcDict[date] = writeFile.getAvgPrice(writeFile.normalList(pricePC))
            momoDict[date] = writeFile.getAvgPrice(writeFile.normalList(priceMomo)) 
            shopeeDict[date] = writeFile.getAvgPrice(writeFile.normalList(priceShopee))
            # yahooDict[date] = writeFile.getAvgPrice(writeFile.normalList(priceYahoo))
            # rutenDict[date] = writeFile.getAvgPrice(writeFile.normalList(priceRuten)) 
            # buy123Dict[date] = writeFile.getAvgPrice(writeFile.normalList(priceBuy))
        # x-axis
        x = [int(i) for i in range(len(dateList))]
        plt.xticks(x, dateList)  # 將 x-axis 用字串標註
        price_momo = [momoDict[d] for d in dateList]  # y1-axis
        price_pchome = [pcDict[d] for d in dateList]  # y2-axis
        price_shopee = [shopeeDict[d] for d in dateList]
        # price_yahoo = [yahooDict[d] for d in dateList]
        # price_ruten = [rutenDict[d] for d in dateList]
        # price_buy123 = [buy123Dict[d] for d in dateList]
        plt.plot(x, price_momo, marker='o', linestyle='solid')
        plt.plot(x, price_pchome, marker='o', linestyle='solid')
        plt.plot(x, price_shopee, marker='o', linestyle='solid')
        # plt.plot(x, price_yahoo, marker='o', linestyle='solid')
        # plt.plot(x, price_ruten, marker='o', linestyle='solid')
        # plt.plot(x, price_buy123, marker='o', linestyle='solid')
        # plt.legend(['momo', 'pchome','shopee','yahoo','ruten','buy123'])
        plt.legend(['momo', 'pchome','shopee'])
        # specify values on ys
        for a, b in zip(x, price_momo):
            plt.text(a, b, str(int(b)))
        for a, b in zip(x, price_pchome):
            plt.text(a, b, str(int(b)))
        for a, b in zip(x, price_shopee):
            plt.text(a, b, str(int(b)))
        # for a, b in zip(x, price_yahoo):
        #     plt.text(a, b, str(int(b)))
        # for a, b in zip(x, price_ruten):
        #     plt.text(a, b, str(int(b)))
        # for a, b in zip(x, price_buy123):
        #     plt.text(a, b, str(int(b)))
        plt.show()
    def normalList(self):
        self.remove(max(self))
        self.remove(min(self))
        return self
    def getAvgPrice(self):
        size =len(self)
        sum = 0
        for i in range(size):
            sum+=self[i]
        avg = sum/size
        return avg