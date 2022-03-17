'''
Created on 2022年3月15日

@author: chu
'''
import pickle
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from .models import Profile,Product,Article 
from django.contrib.auth.models import User
from os.path import exists

def load_cookies(self):
    if exists(self): 
        with open(self, 'rb') as f:
            return pickle.load(f)  
    else:
        login(self)         
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
        save_cookies(self,cookies )
        cookie_jar = cookies.get_dict()
        csrf_token = cookie_jar['csrftoken']
        print("csrf_token: ", csrf_token)
        session_id = cookie_jar['sessionid']
        print("session_id: ", session_id)
    else:
        print("login failed ", login_response.text)



def search(product_name,user):
    if(product_name,user):
        url = 'https://www.instagram.com/explore/tags/'+product_name+'/?__a=1'
        print(url)
        resultList = []
            
        cookies = load_cookies('iglogincookie')
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
        userObj = User.objects.get(username=user);
        profile = Profile.objects.get(user=userObj);
        product = profile.product.get(name=product_name)
        
        for article in range(len(resultList)):
            print(resultList[article].get('code'));
            print(resultList[article].get('text'));
            product.article.create(
                src=resultList[article].get('code'),
                content = resultList[article].get('text'),
                product = product
            )
        print(product_name)
        print(user)