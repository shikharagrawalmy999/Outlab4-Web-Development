import requests
from requests.exceptions import HTTPError
def fetchrepo(username):
    str='https://api.github.com/users/'
    str=str+username
    str=str+'/repos'
    try:
        response=requests.get(str)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}') 
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        repolist=response.json()
        name=[]
        followers=[]
        for repo in repolist:
            name.append(repo['name'])
            followers.append(repo['stargazers_count'])
        return name,followers
