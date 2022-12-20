from django.shortcuts import render,HttpResponse
from app.forms import ValideGitUrl
import re
import json
import requests

def validate(request):
    form = ValideGitUrl()

    if request.method == 'POST':
        regex = r'^(http(s?):\/\/)?(www\.)?github\.com\/([A-Za-z0-9]{1,})+\/?$'
        url = request.POST['url']

        if bool(re.match(regex,url)):
            url="https://api.github.com/users/CoinGecko/repos"
            f=requests.get(url)
            repo_name=[]
            l=len(f.json())
            #return HttpResponse(l)
            for i in range(0,l):
                l1=f.json()[i]["name"]
                repo_name.append(l1)

            count=0
            commit_list=[]
            for repo in repo_name:
                url=f"https://api.github.com/repos/CoinGecko/{repo}"
                for commit in repo:
                    if count<500:
                        f = requests.get(url)
                        x=f.json()["commits_url"]
                        commit_list.append(x)
                        count+=1
                    else:
                        break

            json_string = json.dumps(commit_list)
            
            with open("info.json", "w") as outfile:
                json.dump(json_string, outfile)
            
            return HttpResponse("valid git url")
        
        else:
            return HttpResponse("Invalid git url")

    return render(request,'index.html',{'form': form})

'''from django.shortcuts import render,HttpResponse
from app.forms import ValideGitUrl
import re

def validate(request):
    form = ValideGitUrl()
    
    if request.method == 'POST':
        regex = r'^(http(s?):\/\/)?(www\.)?github\.com\/([A-Za-z0-9]{1,})+\/?$'
        url = request.POST['url']

        if bool(re.match(regex,url)):
            return HttpResponse("valid git url")
        else:
            return HttpResponse("Invalid git url")
        
    return render(request,'index.html',{'form': form}) 
'''

# https://api.github.com/users/whatever?client_id=2f29e695d422b7372030&client_secret=eb85c14637672c198f72d1466bafd68c9da11721