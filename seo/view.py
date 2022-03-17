from django.shortcuts import render
from seo.scrapers import GTrens,Klook, Kkday,Pro, Pchome,Momo,Shopee,Yahoo,\
    Ruten,Buy123,Facebook,Instagram,Article
from django.contrib.auth.decorators import login_required
from future.builtins.misc import isinstance

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

def ArticleView(request):
    
    if(request.user.profile.permission!='2'):
        user_form = request.user
        return render(request,'users/user_permissions.html', {'user': user_form})
    
    article = Article(request.POST.get("city_name"),request.POST.get("description"))
    # article.scrape();
    articleContent = article.scrape()
    context={
        "article":articleContent
    }
    return render(request,"seo/article.html",context)
