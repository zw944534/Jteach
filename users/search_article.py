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
import asyncio
import jieba
import imageio
import wordcloud
import matplotlib.pyplot as plt
import io
import urllib, base64



def _init_(self):
    self.session=None;
    
def load(self,session):
    self.session = session;

def login(self):
    # link = 'https://www.instagram.com/accounts/login/'
    # login_url = 'https://www.instagram.com/accounts/login/ajax/'
    # username = 'zw944534@yahoo.com.tw'
    # password = 'zw611541'
    # time = int(datetime.now().timestamp())
    # response = requests.get(link)
    # csrf = response.cookies['csrftoken']
    #
    # payload = {
    #         'username': username,
    #         'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
    #         'queryParams': {},
    #         'optIntoOneTap': 'false'
    # }
    #
    # login_header = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    #         "X-Requested-With": "XMLHttpRequest",
    #         "Referer": "https://www.instagram.com/accounts/login/",
    #         "x-csrftoken": csrf
    # }
    #
    # login_response = requests.post(login_url, data=payload, headers=login_header)
    # json_data = json.loads(login_response.text)
    #
    # if json_data["authenticated"]:
    #
    #     print("login successful")
    #     cookies = login_response.cookies
    #     save_cookies(self,cookies )
    #     cookie_jar = cookies.get_dict()
    #     csrf_token = cookie_jar['csrftoken']
    #     print("csrf_token: ", csrf_token)
    #     session_id = cookie_jar['sessionid']
    #     print("session_id: ", session_id)
    # else:
    #     print("login failed ", login_response.text)

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
        cookie_jar = cookies.get_dict()
        csrf_token = cookie_jar['csrftoken']
        print("csrf_token: ", csrf_token)
        session_id = cookie_jar['sessionid']
        print("session_id: ", session_id)
        self.session = {
                "csrf_token": cookie_jar['csrftoken'],
                "session_id": cookie_jar['sessionid']
        }
    else:
        print("login failed ", login_response.text)

def search(product_name,user):
    if(product_name,user):
        print('test')
        # Get instance
        # L = instaloader.Instaloader()
        # Optionally, login or load session
        # L.login('zw944534@yahoo.com.tw', 'david960027')        # (login)
        # print(instaloader.Hashtag.from_name(L.context, 'cat').get_posts());
        count = 0;
        # hashtags = instaloader.Hashtag.from_name(L.context, product_name).get_posts();
        # for post in hashtags:
            # print(post)
            # if(count == 20):
                # break;
            # count+=1;
            # L.download_post(post, target='#'+product_name)
        # L.interactive_login('zw944534@yahoo.com.tw')      # (ask password on terminal)
        # L.load_session_from_file('zw944534@yahoo.com.tw') # (load session created w/
        # instam = Instagram();
        # instam.with_credentials('zw944534@yahoo.com.tw', 'zw611541');
        # instam.login();
        
        
        
        # account = instam.get_account('zw944534')
        
        # medias = instam.get_medias_by_tag(product_name, count=20)
        # medias = instam.get_medias_by_tag(product_name,count=20);
        # print(medias);
        
        # medias = instam,get_medias_by_tag(product_name,count=20);
        #
        # print(medias);
        # url = 'https://www.instagram.com/explore/tags/'+product_name+'/?__a=1'
        # print(url)
        # resultList = []
        # cookies={
        #     "sessionid":'1447359165%3ASn8u0HTRswdZrJ%3A10%3AAYeIxd2abtD1E6913fAkL6QtFd95e8LB5lb9q72i1Q',
        #     'csrftoken':'VbBPlVBUwh1tdgSRtaWAPp1WmyPJHvHX'
        # }
        #
        # response = requests.get(url,cookies=cookies)
        # print(response.text);
        # resResult = json.loads(response.text)
        # # print(response.text)
        # print(type(resResult))
        # postDict = resResult.get('data').get('top').get('sections')
        # print(type(postDict))
        # for post in range(len(postDict)):
        #     dictPost = postDict[post]
        #     dictList = dictPost.get('layout_content').get('medias')
        #     for media in dictList:
        #         mediaDict = media.get('media')
        #         shortcode = mediaDict.get('code')
        #         time = mediaDict.get('taken_at')
        #         likeCount = mediaDict.get('like_count')
        #         commentCount = mediaDict.get('comment_count')
        #         text = mediaDict.get('caption').get('text')
        #         print(shortcode)
        #         print(text)
        #         print(commentCount)
        #         resultList.append(dict(code=shortcode,text=text,time=time,likeCount=likeCount,commentCount=commentCount))
        #         # for index in range(len(edgesList)):
        #             # edgeDict = edgesList[index].get('node')
        #             # text = edgeDict.get('text')
        #             # resultList.append(dict(shortcode=shortcode,text=text))
        # print(resultList)
        # userObj = User.objects.get(username=user);
        # profile = Profile.objects.get(user=userObj);
        # product = profile.product.get(name=product_name)
        # articleContent='';
        # commentCount = 0;
        # likeCount = 0;
        # for article in range(len(resultList)):
        #     print(resultList[article].get('code'));
        #     print(resultList[article].get('text'));
        #     articleContent+=resultList[article].get('text');
        #     if resultList[article].get('commentCount'):
        #         commentCount = resultList[article].get('commentCount');
        #     if resultList[article].get('likeCount'):
        #         likeCount = resultList[article].get('likeCount');    
        #     product.article.create(
        #         src=resultList[article].get('code'),
        #         time = resultList[article].get('time'),
        #         likes = resultList[article].get('likeCount'),
        #         commentCount = commentCount,
        #         content = resultList[article].get('text'),
        #         product = product
        #     )
        # mk = imageio.imread('https://wordcloudapi.com/word_cloud.png');
        # wc = wordcloud.WordCloud(background_color="white",
        #                  prefer_horizontal=0.5,
        #                  repeat=True,
        #                  mask=mk,
        #                  contour_width=2,
        #                  contour_color='pink',
        #                  collocation_threshold=100,
        #                  )
        # articleContentList = jieba.cut(articleContent);
        # jiebaString = ''.join(articleContentList);
        # #
        # wc.generate(jiebaString);
        # plt.imshow(wc, interpolation='bilinear')
        # plt.axis("off")
        #
        # image = io.BytesIO()
        # plt.savefig(image, format='png')
        # image.seek(0)  # rewind the data
        # string = base64.b64encode(image.read())
        #
        # image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
        #
        # product.wordcloud = image_64;
        # product.save();
        # print(user)
#    template?    product category to produce article
#    

