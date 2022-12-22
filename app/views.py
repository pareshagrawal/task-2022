from django.shortcuts import render, HttpResponse
from app.forms import ValidGitUrl
import re
import json 
from urllib.parse import urlparse
from github import Github
from datetime import datetime
import pandas as pd
import requests
from .utils import send_mail_to_user

def root(request):
    return render(request,'root.html')

def validate(request):
    form = ValidGitUrl()
    if request.method == 'POST':
        regex = r'^(http(s?):\/\/)?(www\.)?github\.com\/([A-Za-z0-9\-]{1,})+\/?$'
        url = request.POST['url']
        request.session['organization'] = urlparse(url).path[1:]
        if bool(re.match(regex,url)):

            github = Github("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")
            organization = github.get_organization(request.session['organization'])

            # storing all repos name

            repos = []
            for each_repo in organization.get_repos():
                repos.append(each_repo)

            # storing the recent 500 commits of all repos

            all_commits = []
            user_names = []

            for each_repo in repos:
                for each_commit in each_repo.get_commits():
                    if each_commit.author is not None:
                        
                        commits = {
                            'info' : each_commit.commit.message,
                            'date' : each_commit.commit.committer.date,
                            'author' : each_commit.commit.author.name,
                            'username' : each_commit.author.login
                        }
                        user_names.append(each_commit.author.login)
                        all_commits.append(commits)
            
            recent_commits = sorted(all_commits,key=lambda x: x['date'], reverse=True)[0:500]

            # dumping the recent commits into json format

            json_data = {}
            json_data['recent_commits'] = recent_commits
            with open("info.json", "w") as outfile:
                json.dump(json_data, outfile, default=str, indent=4)
            
            # fetching the name of all contributors

            authors = []
            user_names = []
            for each in recent_commits:
                authors.append(each['author'])
                user_names.append(each['username'])

            # fetching all contributors with their frequency and then taking out top 10 contributors

            df = pd.DataFrame(zip(authors,user_names),columns=["author_name","user_names"])            
            df1 = pd.DataFrame(df.value_counts().head(10),columns=["frequency"])
            
            # converting the list into .csv file as well as json format (for attachment purpose)

            df1.to_csv("top10_contributors.csv")

            df1.to_json("top10_contributors.json")
            
            # for storing all starred repos of those 10 users

            df = pd.read_csv("top10_contributors.csv")
            starred_info = {}

            for i in df.user_names:
                page=(github.get_user(i).get_starred().totalCount//100)+1
                starred_repo = []
                for j in range(1,page+1):
                    link = f"https://api.github.com/users/{i}/starred?per_page=100&page={j}"
                    f = requests.get(link)
                    fjson = f.json()
                    l = len(fjson)
                    if l != 0:
                        for j in range(l):
                            starred_repo.append(fjson[j]["full_name"])
                starred_info[i] = starred_repo                

            # dumping the starred info into json format

            with open("starred.json","w") as outfile:
                json.dump(starred_info, outfile, default=str, indent=4)

            return render(request,'output.html')

        else:
            return HttpResponse("Invalid URL, Please enter a valid URL")

    return render(request,'index.html',{'form': form})

def email(request):
    flag = send_mail_to_user(['siddhisharma0820@gmail.com','er.pareshagrawal@gmail.com'],'Task done','Attached all files')
    if flag:
        return HttpResponse("Email Successfully sent")
    return HttpResponse("Failure in sending Email")

