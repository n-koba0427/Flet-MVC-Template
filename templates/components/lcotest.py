import requests
from bs4 import BeautifulSoup

def test():
    url = "https://www.op.gg/summoners/jp/tarutarupop-0428/mastery"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    champs = soup.find_all('div', class_='e1poynyt1')[:5]
    for champ in champs:
        champ_img = champ.find(class_="champion-image--square").find("img").get("src")
        champ_point = champ.find(class_="champion-point").text
        print(champ_img, champ_point)

if __name__ == "__main__":
    test()

