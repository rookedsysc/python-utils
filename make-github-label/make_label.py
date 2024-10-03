import requests
import json

class MakeGithubLabel :
  def __init__(self) -> None :
    self.TOKEN = None
    self.OWNER = None
    self.REPO = None
    self.HEADERS = None
    
    self.read_token()
    self.input_owner()
    self.input_repo()
    self.delete_old_label()
    self.make_new_label()
    
  def input_owner(self) : 
    self.OWNER = input("Input user name : ")
  
  def input_repo(self) :
    self.REPO = input("Input Repo : ")
  
  # 
  def read_token(self) :
    with open(".env", "r") as f:
      self.TOKEN = f.read().strip()
      print(f"Token read success : {self.TOKEN}")
      self.HEADERS = {
        "Authorization": f"token {self.TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        }

  def delete_old_label(self) :
    # 기존 라벨들을 삭제
    URL_DELETE = f"https://api.github.com/repos/{self.OWNER}/{self.REPO}/labels"
    response = requests.get(URL_DELETE, headers=self.HEADERS)
    
    print(f"Delete Response : {response}")

    if response.status_code == 200:
        existing_labels = response.json()
        for label in existing_labels:
            del_response = requests.delete(f"{URL_DELETE}/{label['name']}", headers=self.HEADERS)
            if del_response.status_code == 204:
                print(f"Label {label['name']} deleted successfully!")
            else:
                print(f"Failed to delete label {label['name']}. Response: {del_response.text}")
    else:
        print(f"Failed to get existing labels. Response: {response.text}")


  def make_new_label(self) :
    LABELS = []

    with open("labels.json", "r") as f:
      LABELS = json.load(f)
    
    URL = f"https://api.github.com/repos/{self.OWNER}/{self.REPO}/labels"
    print(f"request URL : {URL}")
    
    
    for label in LABELS:
      response = requests.post(URL, headers=self.HEADERS, json=label)
      
      if response.status_code == 201:
          print(f"Label {label['name']} created successfully!")
      else:
          print(f"Failed to create label {label['name']}. Response: {response.text}")

if __name__ == "__main__":
  make_label = MakeGithubLabel()

  


