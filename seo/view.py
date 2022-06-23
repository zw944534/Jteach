from django.shortcuts import render
from seo.scrapers import GTrens,Klook, Kkday,Pro, Pchome,Momo,Shopee,Yahoo,\
    Ruten,Buy123,Facebook,Instagram,Article,EditTemplate
from django.contrib.auth.decorators import login_required
from future.builtins.misc import isinstance
from users.models import Profile
import random

@login_required
def index(request):

    if(request.user.profile.permission!='2'):
        user_form = request.user
        return render(request,'users/user_permissions.html', {'user': user_form})
    # klook = Klook(request.POST.get("city_name"))
    # kkday = Kkday(request.POST.get("city_name"))
    gTrens = GTrens(request.POST.get("city_name"))
    # article = Article(request.POST.get("city_name"))
    # article.scrape()
    context = {
        "tickets":  gTrens.scrape()
    }

    return render(request, "seo/index.html", context)

@login_required
def product(request):
    
    if(request.user.profile.permission!='2'):
        user_form = request.user
        return render(request,'users/user_permissions.html', {'user': user_form})
    
    pro = Pro(request.POST.get("city_name"))
    
    context={
        "products":pro.scrape()
    }
    return render(request,"seo/product.html",context)

@login_required
def searchProduct(request):
    
    if(request.user.profile.permission!='2'):
        user_form = request.user
        return render(request,'users/user_permissions.html', {'user': user_form})
    
    pchome = Pchome(request.POST.get("city_name"))
    momo = Momo(request.POST.get("city_name"))
    shopee = Shopee(request.POST.get("city_name"))
    yahoo = Yahoo(request.POST.get("city_name"))
    ruten = Ruten(request.POST.get("city_name"))
    # buy123 = Buy123(request.POST.get("city_name"))
    tickets = pchome.scrape()
    momos = momo.scrape()
    shopees = shopee.scrape()
    yahoos = yahoo.scrape()
    rutens = ruten.scrape()
    # buy123s = buy123.scrape()
    resultDict = dict(pchome=tickets,momo=momos,shopee=shopees,yahoo=yahoos,ruten=rutens)
    def test(test):
        priceArray = []
        sum=0
        for i in (range(len(test))):
            price = test[i].get('price')
            if price:
                if isinstance(price,str):
                    price = price.replace(',','')
                priceArray.append(int(price))
        print(priceArray)
        for i in (range(len(priceArray))):
            sum+=priceArray[i]
        avg = 0
        if(sum!=0 and len(priceArray)!=0):
            avg = sum/len(priceArray)
            avg = round(avg)
        return avg
    pchomeAvg = test(tickets)
    momoAvg = test(momos)
    shopeeAvg = test(shopees)
    label = ['pchome','momo','shopee']
    data = [pchomeAvg,momoAvg,shopeeAvg]
    # yahooAvg = test(yahoos)
    # rutenAvg = test(rutens)
    # buy123Avg = test(buy123s)
    print(pchomeAvg,momoAvg,shopeeAvg)
    # writeFile.write(resultDict)
    # writeFile.read(resultDict)
    context={
        "tickets":tickets,
        "momos":momos,
        "shopee":shopees,
        "yahoo":yahoos,
        "ruten":rutens,
        "label":label,
        "data":data
        

    }
    return render(request,"seo/productSearch.html",context)

@login_required
def facebook(request):
    
    if(request.user.profile.permission!='2'):
        user_form = request.user
        return render(request,'users/user_permissions.html', {'user': user_form})
    
    facebook = Facebook(request.POST.get("city_name"))
    fbContent = facebook.scrape()
    context={
        "fb": fbContent
    }
    return render(request,"seo/socialContent.html",context)

@login_required
def Ig(request):
    
    if(request.user.profile.permission!='2'):
        user_form = request.user
        return render(request,'users/user_permissions.html', {'user': user_form})
    
    instagram = Instagram(request.POST.get("city_name"))
    igContent = instagram.scrape()
    context={
        "ig":igContent
    }
    return render(request,"seo/igContent.html",context)

@login_required
def ArticleView(request):
#    select source fb/ig/
#    filter by time/likes
#    article tags
#    top topics graph
#    智能小編
#    article construct limit
#    

    if(request.user.profile.permission!='2'):
        user_form = request.user
        return render(request,'users/user_permissions.html', {'user': user_form})
    
    # profile = Profile.objects.get(user = request.user);
    # constructArticle = '';
    # if profile:
    #     product = profile.product.filter(name=request.POST.get("city_name"));
    #     articleList=[];
    #     for i in list(product):
    #         print(i.id,i.name);
    #         articleList=i.article.all();
    #     if len(articleList)!=0:
    #         randomIndex = random.randint(0, len(articleList));
    #         constructArticle+=articleList[randomIndex].content;
            
    article = Article(request.POST.get("city_name"),request.POST.get("description"),
                      request.POST.get("urlTitle"),request.POST.get("address"),
                      request.POST.get("tel"),request.POST.get("saleMessage"),
                      request.POST.getlist("hashtag"),request.POST.get("productCategory"))
    articleContent = article.scrape()
    print(articleContent);
    context={
        "article":articleContent
    }
    return render(request,"seo/article.html",context)

@login_required
def editTemplate(request):
    
    # if(request.user.profile.permission!='2'):
    #     user_form = request.user
    #     return render(request,'users/user_permissions.html', {'user': user_form})
    template = EditTemplate(request.POST.get("catch"),request.POST.get("preCatch"),
                      request.POST.get("subCatch"),request.POST.get("mainBody"),
                      request.POST.get("headline"),request.POST.get("bodyText"),
                      request.POST.getlist("description"),request.POST.get("advantage1")
                      ,request.POST.get("advantage2"),request.POST.get("advantage3")
                      ,request.POST.get("reason1"),request.POST.get("reason2")
                      ,request.POST.get("reason3"),request.POST.get("slogan")
                      ,request.POST.get("bodyPoint"),request.POST.get("bodyCopy")
                      ,request.POST.get("templateType"),request.user)
    if request.method == 'POST':
        allTemplate = template.scrape()
        print(allTemplate);
        context={
            "template":allTemplate
        }
        return render(request,"seo/editTemplate.html",context)
    else:
        allTemplate = template.getAllTemplate()
        listTemplate = list(allTemplate)
        for template in listTemplate:
            print(template.catch)
        context={
            "template":listTemplate
        }
        return render(request,"seo/editTemplate.html",context)
    
