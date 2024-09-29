import requests
from bs4 import BeautifulSoup
import json
import os
import flet as ft


def test():
    url = "https://www.op.gg/summoners/jp/tarutarupop-0428/mastery"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    champs = soup.find_all('div', class_='e1poynyt1')[:5]
    for champ in champs:
        champ_img = champ.find(class_="champion-image--square").find("img").get("src")
        champ_point = champ.find(class_="champion-point").text
        print(champ_img, champ_point)

def get_json(url="https://ddragon.leagueoflegends.com/cdn/14.19.1/data/en_US/champion.json"):
    response = requests.get(url)
    downloadData = response.json()
    with open(os.path.join(os.path.dirname(__file__), "champion.json"), "w", encoding="utf-8") as f:
        json.dump(downloadData, f, ensure_ascii=False)

def load_champs_json():
    with open(os.path.join(os.path.dirname(__file__), "../../database/champion.json"), "r", encoding="utf-8") as f:
        downloadData = json.load(f)
    return downloadData["data"]

def get_champ(champ_name):
    champs = load_champs_json()
    return champs[champ_name]

def get_champ_img(champ_name):
    return f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ_name}_0.jpg"

def clean_text(text):
    problematic_chars = ["\u2069", "\u2066"]
    for problematic_char in problematic_chars:
        text = text.replace(problematic_char, "")
    text = text.replace("\r\n", "\n")
    return text.split("\n")

def extract_summoner_name(join_msg):
    join_msg_list = clean_text(join_msg)
    summoner_name_list = []
    tag_list = []
    for join_msg in join_msg_list:
        tails = ["がロビーに参加しました。", "joined the lobby"]
        for tail in tails:
            if tail in join_msg:
                join_msg = join_msg.replace(tail, "")
                break
        join_msg_split = join_msg.split(" #")
        summoner_name, tag = join_msg_split
        summoner_name_list.append(summoner_name)
        tag_list.append(tag)
    return summoner_name_list, tag_list

def main(page: ft.Page):
    textfield = ft.TextField(label="lobby log", multiline=True, min_lines=10)
    def submit_button_click(e):
        summoner_name_list, tag_list = extract_summoner_name(textfield.value)
        for summoner_name, tag in zip(summoner_name_list, tag_list):
            print(f"{summoner_name}#{tag}")
    submit_button = ft.ElevatedButton("Submit", on_click=submit_button_click)
    page.add(textfield, submit_button)

if __name__ == "__main__":
    ft.app(target=main)