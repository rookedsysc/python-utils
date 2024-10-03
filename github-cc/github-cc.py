import requests

def get_github_user_info(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def generate_html(usernames):
    html = ""

    for username in usernames:
        user_info = get_github_user_info(username)
        if user_info:
            profile_url = user_info['html_url']
            avatar_url = user_info['avatar_url']
            name = user_info['login']  

            html += f'''<img src="{avatar_url}" alt="{name}" width="15" height="15" style="vertical-align: middle;"> [{name}]({profile_url}), '''
        else:
            html += f"{username}, "
            
    html = html[0:-2] 

    return html

# GitHub ID 리스트
usernames = ["rookedsysc"]

# HTML 생성
html_content = generate_html(usernames)

# 터미널에 HTML 출력
print(html_content)
