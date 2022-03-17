'''
Created on 2021年10月21日

@author: chu
'''
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from pytrends.request import TrendReq
from datetime import datetime
import urllib
import re
import facebook_crawler as fc
import json
import pickle
import random
import io

# 票券網站抽象類別
class Website2(ABC):
    def __init__(self, city_name,description):
        self.city_name = city_name  # 城市名稱屬性
        self.description = description
    @abstractmethod
    def scrape(self):  # 爬取票券抽象方法
        pass
class Website(ABC):

    def __init__(self, city_name):
        self.city_name = city_name  # 城市名稱屬性

    @abstractmethod
    def scrape(self):  # 爬取票券抽象方法
        pass
    
    
    def trimString(self,string):
        arrList = string.split()
        str=''
        for i in arrList:
            str+=i
        return str
    def getProductList(self):
        url = 'https://training.jteach.com/%E5%95%86%E5%93%81%E9%A6%96%E9%A0%81/?product-page='
        i='1'
        # print('in pro')
        productList=[]
        picUrlList=[]
        req = requests.get(url+i)
        if(req.status_code == 200):
            soup = BeautifulSoup(req.text,'html.parser')
            indexList = soup.find_all('a',class_='page-numbers')
            maxList=[]
            for index in indexList:
                if(index.string is not None):
                    maxList.append(int(index.string))
            maxPage = max(maxList)
            # print(type(maxPage))
            urlList = []
            for i in range(1,maxPage+1):
                urlList.append(url+str(i))
            # print(urlList)   
            for url in urlList:
                reqs = requests.get(url)
                if(reqs.status_code == 200):
                    soup = BeautifulSoup(reqs.text,'html.parser')
                    productLists = soup.find_all('h2',class_='woocommerce-loop-product__title')
                    picList = soup.find_all('img',class_='attachment-woocommerce_thumbnail size-woocommerce_thumbnail')
                    for product in productLists:
                        # print(product.text)
                        productList.append(product.text)
                    for img in picList:
                        picUrlList.append(img.get('src'))
        return productList,picUrlList     
                           
# KLOOK客路網站
class Klook(Website):

    def scrape(self):

        result = []  # 回傳結果

        if self.city_name:  # 如果城市名稱非空值

            # 取得傳入城市的所有一日遊&導賞團票券
            response = requests.get(
                f"https://www.klook.com/zh-TW/search/?keyword={self.city_name}&template_id=2&sort=price&start=1")
            soup = BeautifulSoup(response.text, "lxml")

            # 取得十個票券卡片(Card)元素
            activities = soup.find_all(
                "div", {"class", "j_activity_item_link j_activity_item_click_action"}, limit=10)

            for activity in activities:

                # 票券名稱
                title = activity.find(
                    "a", {"class": "title"}).getText().strip()

                # 票券詳細內容連結
                link = "https://www.klook.com" + \
                    activity.find("a", {"class": "title"}).get("href")

                # 票券價格
                price = activity.find(
                    "span", {"class": "latest_price"}).getText().strip()

                # 最早可使用日期
                booking_date = activity.find(
                    "span", {"class": "g_right j_card_date"}).get("data-serverdate")[0:10]

                # 評價
                star = activity.find("span", {"class": "t14 star_score"}).getText(
                ).strip() if activity.find("span", {"class": "t14 star_score"}) else "無"

                result.append(
                    dict(title=title, link=link, price=price, booking_date=booking_date, star=star, source="https://cdn.klook.com/s/dist_web/assert/desktop/imgs/favicon-098cf2db20.png"))

        return result


# KKday網站
class Kkday(Website):

    def scrape(self):

        result = []  # 回傳結果

        if self.city_name:  # 如果城市名稱非空值

            # 取得傳入城市的所有一日遊票券
            response = requests.get(
                f"https://www.kkday.com/zh-tw/product/ajax_productlist/?keyword={self.city_name}&cat=TAG_4_4&sort=pasc")

            # 資料
            activities = response.json()["data"]

            for activity in activities:

                # 票券名稱
                title = activity["name"]

                # 票券詳細內容連結
                link = activity["url"]

                # 票券價格
                price = f'NT$ {int(activity["price"]):,}'

                # 最早可使用日期
                booking_date = datetime.strftime(datetime.strptime(
                    activity["earliest_sale_date"], "%Y%m%d"), "%Y-%m-%d")

                # 評價
                star = str(activity["rating_star"])[
                    0:3] if activity["rating_star"] else "無"

                result.append(
                    dict(title=title, link=link, price=price, booking_date=booking_date, star=star, source="https://cdn.kkday.com/m-web/assets/img/favicon.png"))

        return result
    
#Google Trend
class GTrens(Website):
    
    
    
    
    def scrape(self):
        
        resultList = []
        pytrend = TrendReq(hl='en-US', tz=360)
        if self.city_name:
            keyWords = []
            keyWords.append(self.city_name)
            pytrend.build_payload(kw_list=keyWords,  timeframe='all', geo='TW', gprop='')
            herfString = 'https://news.google.com/search?q='
            result = pytrend.related_queries()
            # print(result)
            resultTop=[]
            resultRising=[]
            dfTop = result.get(self.city_name).get("top")
            # print(type(dfTop))
            dfRising = result.get(self.city_name).get("rising")
            if(dfTop is None and dfRising is None):
                resultList.append(dict(top='None',rise='None'))
            elif(dfTop is None and dfRising is not None):
                resultRising = dfRising["query"].tolist()
                for rising in resultRising:
                    resultList.append(dict(top='None',rise=rising))
            elif(dfTop is not None and dfRising is None):
                resultTop = dfTop["query"].tolist()
                for top in resultTop:
                    resultList.append(dict(top=top,rise='None'))
            else:
                resultTop = dfTop["query"].tolist()
                resultRising = dfRising["query"].tolist()
#if need add search amount, then ....["value"]
                for top,rising in zip(resultTop,resultRising):
                    # print(self.trimString(top))
                    resultList.append(dict(top=top,rise=rising,topUrl=herfString+self.trimString(top),riseUrl=herfString+self.trimString(rising)))
               
        return resultList

# Get Product and Get Hashtag/keyword

class Pro(Website):
    
    
    
    
    def scrape(self):
        
        resultList = []
        # print('in pro')
        productList,picList=self.getProductList()
        # print(picList)
        for product,img in zip(productList,picList):
            resultList.append(dict(product=product,src=img))
        
        return resultList

####################################################
# add product url forword to each product details ##
####################################################
# IG entity
# search url https://www.instagram.com/explore/tags/{query}
# pchome entity
# search url='https://ecshweb.pchome.com.tw/search/v3.3/?q={query}'
class Pchome(Website):
    def scrape(self):
        resultList=[]
        if self.city_name:
            # print("https://ecshweb.pchome.com.tw/search/v3.3/?q="+self.city_name)
            response = requests.get('https://ecshweb.pchome.com.tw/search/v3.3/all/results?q='+self.city_name+'&page=1&sort=sale/dc')
            dataList = response.json()["prods"]
            for data in dataList:
                #product id to get product url
                id = data["Id"]
                #product name
                title = data["name"]
                #product describe
                describe = data["describe"]
                #product price
                price = data["price"]
                
                resultList.append(dict(title=title,describe=describe,price=price,url='https://24h.pchome.com.tw/prod/'+id))
        
        return resultList

class Momo(Website):
    def scrape(self):
        resultList=[]
        if self.city_name:
            page=1
            keyword=self.city_name
            url = 'https://m.momoshop.com.tw/search.momo?_advFirst=N&_advCp=N&curPage={}&searchType=1&cateLevel=2&ent=k&searchKeyword={}&_advThreeHours=N&_isFuzzy=0&_imgSH=fourCardType'.format(page, keyword)
            userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            headers = {'User-Agent': userAgent}
            urls=[]
            response = requests.get(url,headers=headers)
            soup = BeautifulSoup(response.text)
            for item in soup.select('li.goodsItemLi > a'):
                urls.append('https://m.momoshop.com.tw'+item['href'])
            # print(len(urls))
            df=[]
            for i, url in enumerate(urls):
                columns = []
                values = []
    
                resp = requests.get(url, headers=headers)
                soup = BeautifulSoup(resp.text,"lxml")
                # 標題
                title = soup.find('meta',{'property':'og:title'})['content']
                # 品牌
                brand = soup.find('meta',{'property':'product:brand'})['content']
                # 連結
                link = soup.find('meta',{'property':'og:url'})['content']
                # 原價
                try:
                    price = re.sub(r'\r\n| ','',soup.find('del').text)
                except:
                    price = ''
                # 特價
                amount = soup.find('meta',{'property':'product:price:amount'})['content']
                # 類型
                cate = ''.join([i.text for i in soup.findAll('article',{'class':'pathArea'})])
                cate = re.sub('\n|\xa0',' ',cate)
                # 描述
                try:
                    desc = soup.find('div',{'class':'Area101'}).text
                    desc = re.sub('\r|\n| ', '', desc)
                except:
                    desc = ''
                
                # print('==================  {}  =================='.format(i))    
                # print(title)
                # print(brand)
                # print(link)
                # print(amount)
                # print(cate)
                columns += ['title', 'brand', 'link', 'price', 'amount', 'cate', 'desc']
                values += [title, brand, link, price, amount, cate, desc]
                resultList.append(dict(title=title,describe=desc,price=price,url=link))
            # for product in resultList:
            #     print(product['price'])
                # 規格
            #     for i in soup.select('div.attributesArea > table > tr'):
            #         try:
            #             column = i.find('th').text
            #             column = re.sub('\n|\r| ','',column)
            #             value = ''.join([j.text for j in i.findAll('li')])
            #             value = re.sub('\n|\r| ','',value)
            #             columns.append(column)
            #             values.append(value)
            #         except:
            #             pass
            #     ndf = pd.DataFrame(data=values, index=columns).T
            #     df.append(ndf)
            # df=pd.concat(df, ignore_index=True)
            # df.info()
        return resultList

# shopee entity
class Shopee(Website):
    def scrape(self):
        resultList=[]
        if(self.city_name):
            keyword=self.city_name
            headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.68',
                    'x-api-source': 'pc',
                    'referer': f'https://shopee.tw/search?keyword={urllib.parse.quote(keyword)}'
                    }
            session = requests.Session()
            url = 'https://shopee.tw/api/v4/search/product_labels'
            r = session.get(url, headers=headers)
            base_url = 'https://shopee.tw/api/v2/search_items/'
            query = f"by=relevancy&keyword={keyword}&limit=50&newest=0&order=desc&page_type=search&version=2"
            url = base_url + '?' + query
            r = session.get(url, headers=headers)
            if r.status_code==200:
                result = r.json()['items']
                for product in result:
                    # print(product)
                    name = product['name']
                    price = int(product['price']/100000)
                    resultList.append(dict(name=name,price=price))
        return resultList
# yahoo entity
class Yahoo(Website):
    def scrape(self):
        resultList=[]
        if(self.city_name):
            keyword=self.city_name
            url = f'https://tw.buy.yahoo.com/search/product?p={urllib.parse.quote(keyword)}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text,'html.parser')
            titleList=[]
            priceList=[]
            for items in soup.find_all(class_='BaseGridItem__title___2HWui'):
                titleList.append(items.text)
            for priceSet in soup.find_all(class_='BaseGridItem__price___31jkj'):
                priceList.append(priceSet.text.replace('$','').replace(',',''))
            
            for title,price in zip(titleList,priceList):
                resultList.append(dict(title=title,price=price))
        return resultList
# Ruten entity
class Ruten(Website):
    def scrape(self):
        resultList=[]
        if(self.city_name):
            keyword = self.city_name
            url = f'https://www.ruten.com.tw/find/?q={urllib.parse.quote(keyword)}'
            headers = {'User-Agent':'GoogleBot'}
            response = requests.get(url,headers=headers)
            soup = BeautifulSoup(response.text,'html.parser')
            # print(soup)
            for product in soup.find_all('div','prod_info'):
                name = product.find('h5').find('a').text
                price = product.find(class_='price').text.replace(',','')
                if(name!='NoneType' and price!=''):
                    resultList.append(dict(name=name,price=price))
        return resultList
# Buy123 entity
class Buy123(Website):
    def scrape(self):
        resultList=[]
        if(self.city_name):
            keyword=self.city_name
            print(keyword)
            
        return resultList
    
    
    
# if(self.city_name):
#             keyword=self.city_name
#             url=f'https://www.buy123.com.tw/search?q={urllib.parse.quote(keyword)}'
#             userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
#             headers = {'User-Agent': userAgent}
#             response = requests.get(url,headers=headers)
#             productCount=0
#             totalPrice=0
#             soup = BeautifulSoup(response.text,'html.parser')
#             for product in soup.find_all('div','item-info'):
#                 name = product.find('h2').text
#                 price = product.find(class_='large-font').text.replace('$','')
#                 resultList.append(dict(name=name,price=price))
# Rakuten
# class Rakuten(Website):
#     def scrape(self):
#         resultList=[]
#         if(self.city_name):
#             keyword=self.city_name
#             url=f'https://www.rakuten.com.tw/search/{urllib.parse.quote(keyword)}'
#             userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
#             headers = {'User-Agent': userAgent}
#             response = requests.get(url,headers=headers)
#             soup = BeautifulSoup(response.text,'html.parser')
#             print(soup)
#             for product in soup.find_all('a',class_='product-info'):
#                 print('1234')
#                 print(product.text)
#                 name = product.find('h3').text
#                 print(name)
#                 price = product.find(class_='price').text
#                 print(price)
#                 resultList.append(dict(name=name,price=price))
#         print(resultList)
# Get facebook fanpage/group content
class Facebook(Website):
    def scrape(self):
        print('1234')
        query = self.city_name
        print(query)
        if(query):
            pageUrl = query;
            fanPage = fc.Crawl_PagePosts(pageurl=pageUrl, until_date='2021-12-31')
            fanPageDict = fanPage.to_dict('records')
            # contentArray = fanPage['MESSAGE'];
            return fanPageDict
           
#        group has some bug need to fix

        # groupUrl = 'https://www.facebook.com/groups/528068505186588';
        # group = fc.Crawl_GroupPosts(groupUrl, until_date='2021-12-31')
        # print(type(group))
        # print(group)
        
# Get IG content by search hash tag keyword
class Instagram(Website):
    def scrape(self):
        print('Instagram')
        query = self.city_name
        
#        explore = 'https://www.instagram.com/p/'+shortcode

        if(query):
            url = 'https://www.instagram.com/explore/tags/'+query+'/?__a=1'
            print(url)
            resultList = []
            
            cookies = Instagram.load_cookies('iglogincookie')
            response = requests.get(url,cookies=cookies)
            resResult = json.loads(response.text)
            # print(response.text)
            print(type(resResult))
            postDict = resResult.get('data').get('top').get('sections')
            print(type(postDict))
            for post in range(len(postDict)):
                dictPost = postDict[post]
                dictList = dictPost.get('layout_content').get('medias')
                for media in dictList:
                    mediaDict = media.get('media')
                    shortcode = mediaDict.get('code')
                    text = mediaDict.get('caption').get('text')
                    print(shortcode)
                    print(text)
                    resultList.append(dict(code=shortcode,text=text))
                # for index in range(len(edgesList)):
                    # edgeDict = edgesList[index].get('node')
                    # text = edgeDict.get('text')
                    # resultList.append(dict(shortcode=shortcode,text=text))
            print(resultList)    
            return resultList   
    def load_cookies(self):
        with open(self, 'rb') as f: 
            if not f:
                Instagram.login(self)
            return pickle.load(f)           
    def save_cookies(self,requests_cookiejar ):
        with open(self, 'wb') as f:
            pickle.dump(requests_cookiejar, f)
    def login(self):
        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'
        username = 'zw944534@yahoo.com.tw'
        password = 'zw611541'
        time = int(datetime.now().timestamp())
        response = requests.get(link)
        csrf = response.cookies['csrftoken']
                    
        payload = {
                'username': username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
                'queryParams': {},
                'optIntoOneTap': 'false'
        }
                    
        login_header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken": csrf
            }
                    
        login_response = requests.post(login_url, data=payload, headers=login_header)
        json_data = json.loads(login_response.text)
                    
        if json_data["authenticated"]:
                    
            print("login successful")
            cookies = login_response.cookies
            Instagram.save_cookies(self,cookies )
            cookie_jar = cookies.get_dict()
            csrf_token = cookie_jar['csrftoken']
            print("csrf_token: ", csrf_token)
            session_id = cookie_jar['sessionid']
            print("session_id: ", session_id)
        else:
            print("login failed ", login_response.text)
            
            
class Article(Website2):
    def scrape(self):
        print('1234')
        desc = self.description
        keyword = self.city_name
        if desc:            
            txt = random.randint(0, 1)
            fileNum = random.randint(1,2)
            fileName = ['meme','trend']
            file = io.open(('C:/Users/chu/Documents/for nku/雜/final/ec_workshop/Jteach/src/text_template/'+fileName[txt]+str(fileNum)+'.txt'),mode="r",encoding="utf-8")
            # file = open(('C:/Users/chu/Documents/for nku/雜/final/ec_workshop/Jteach/src/text_template/'+fileName[txt]+str(fileNum)+'.txt'),'r')
            lines = file.readlines()
            article=""
            for line in lines:
                if line.find("{keyword}")!=-1:
                    article+=line.replace("{keyword}",keyword)
                elif "{description}" in line:
                    article += line.replace("{description}",desc)
                else:
                    article+=line
            return article;