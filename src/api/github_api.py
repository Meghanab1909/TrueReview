import requests
from config import HEADERS, BASE_URL

print("Fetching PRs...")
def get_all_prs(owner, repo, state="closed"):
    prs = []
    page = 1

    while page <= 5:
        url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
        params = {"state": state, "per_page": 100, "page": page}

        response = requests.get(url, headers=HEADERS, params=params)
        
        if response.status_code != 200:
            print("❌ ERROR:", response.status_code)
            print(response.text)
            break

        try:
            data = response.json()
        except:
            print("JSON PARSE ERROR")
            print(response.text)
            break 
        
        if not data:
            break

        prs.extend(data)
        page += 1

    return prs

def get_pr_comments(owner, repo, pr_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues/{pr_number}/comments"
    return requests.get(url, headers=HEADERS).json()


def get_review_comments(owner, repo, pr_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/comments"
    return requests.get(url, headers=HEADERS).json()


def get_commits(owner, repo, pr_number):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/commits"
    return requests.get(url, headers=HEADERS).json()