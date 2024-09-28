import flet as ft
import requests
from bs4 import BeautifulSoup
import itertools
import random

from app.utils import *

def _calculate_score(rank: str, lp: str):
    tires = ["iron", "bronze", "silver", "gold", "platinum", "emerald", "diamond", "master", "grandmaster", "challenger"]
    if rank in ["master", "grandmaster", "challenger"]:
        rank += " 4"
    tire, division = rank.split(" ")
    return (tires.index(tire) * 4 + (4-int(division))) * 100 + int(lp)

def _get_summoner_max_score(region: str="jp", summoner_name: str="naoyashiyashi", tag: str="JP1"):
    url = f'https://www.op.gg/summoners/{region}/{summoner_name}-{tag}'
    response = requests.get(url)
    player_icon = "https://opgg-static.akamaized.net/meta/images/profile_icons/profileIcon29.jpg?image=e_upscale,q_auto:good,f_webp,w_auto&v=1724034092925"
    max_rank = "Unranked"
    max_lp = 0
    max_score = 0
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        error_msg = soup.find('div', class_='e19vm62i1')
        if error_msg:
            return None, None, None, None
        player_icon = soup.find('div', class_='profile-icon').find("img").get("src")
        rank_info = soup.find('div', class_='e15k6o3w0').find("tbody")
        rank_list = rank_info.find_all("div", class_="rank-item")
        lp_list = rank_info.find_all("div", class_="lp")
        for rank, lp in zip(rank_list, lp_list):
            score = _calculate_score(rank.text.lower(), int(lp.text))
            if score > max_score:
                max_score = score
                max_rank = rank.text
                max_lp = lp.text
    return player_icon, max_rank, max_lp, max_score

def _get_summoner_champs(region: str="jp", summoner_name: str="naoyashiyashi", tag: str="JP1", top_n: int=10):
    url = f"https://www.op.gg/summoners/{region}/{summoner_name}-{tag}/mastery"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    champs = soup.find_all('div', class_='e1poynyt1')[:top_n]
    champs_img = []
    champs_point = []
    champs_name = []
    for champ in champs:
        champ_name = champ.find(class_="champion-name").text
        champ_point = champ.find(class_="champion-point").text
        champs_point.append(champ_point)
        champs_name.append(champ_name)
    champs_name = "|".join(champs_name)
    champs_point = "|".join(champs_point)
    return champs_name, champs_point

def _change_summoner_status(e, page: ft.Page, summoner: Summoner):
    summoner.is_active = e.control.value
    summoner.save()
    page.reload()

def _member_card(page: ft.Page, summoner: Summoner):
    title = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row( 
                    controls=[
                        ft.Image(
                            src=summoner.player_icon,
                            width=30,
                            height=30,
                            border_radius=ft.border_radius.all(15),
                        ),
                        ft.Text(f"{summoner.summoner_name} #{summoner.tag} ({summoner.rank}, {summoner.lp}LP)", size=20, weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Row(
                    controls=[
                        ft.Switch(value=summoner.is_active, on_change= lambda e, page=page, summoner=summoner: _change_summoner_status(e, page, summoner)),
                    ],
                    alignment=ft.MainAxisAlignment.END
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        bgcolor=ft.colors.SECONDARY_CONTAINER if summoner.is_active else ft.colors.GREY_100,
        border_radius=ft.border_radius.all(10),
        padding=ft.padding.all(10),
    )
    champs_name = summoner.champs_name.split("|")
    champs_point = summoner.champs_point.split("|")
    _card = ft.ExpansionTile(
        title=title,
        controls=[
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Image(
                                src=f"https://opgg-static.akamaized.net/meta/images/lol/latest/champion/{champ_name.replace(" ", "").replace("'", "")}.png?image=e_upscale,c_crop,h_103,w_103,x_9,y_9/q_auto:good,f_webp,w_160,h_160&v=1724034092925",
                                width=50,
                                height=50,
                                border_radius=ft.border_radius.all(5),
                            ),
                            # ft.Text(champ_name),
                            ft.Text(champ_point),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ) for champ_name, champ_point in zip(champs_name, champs_point)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
    )
    return _card

def _add_summoner(region: str, summoner_name: str, tag: str):
        player_icon, max_rank, max_lp, max_score = _get_summoner_max_score(
            region=region,
            summoner_name=summoner_name,
            tag=tag
        )
        champs_name, champs_point = _get_summoner_champs(region, summoner_name, tag, top_n=10)
        if exists(player_icon):
            add_data(
                model_name="Summoner",
                data_dict={
                    "region": region,
                    "summoner_name": summoner_name,
                    "tag": tag,
                    "player_icon": player_icon,
                    "rank": max_rank,
                    "lp": str(max_lp),
                    "score": str(max_score),
                    "champs_name": champs_name,
                    "champs_point": champs_point,
                }
            )
            return True
        return False

def _get_active_summoners():
    return search_data("Summoner", "is_active", True)

def _grouping(page: ft.Page, top_n: int = 5):
    active_summoners = _get_active_summoners()
    if len(active_summoners) != 10:
        page.open(ft.SnackBar(content=ft.Text("10 active summoners are required.")))
        return

    # Convert summoners to tuples with their scores
    summoners = [(s, int(s.score)) for s in active_summoners]
    # Generate all possible combinations of 5 summoners
    all_combinations = list(itertools.combinations(summoners, 5))

    unique_combinations = set()
    top_combinations = []

    # Calculate score differences for all combinations
    for combo in all_combinations:
        team1 = list(combo)
        team2 = [s for s in summoners if s not in team1]
        team1_score = sum(s[1] for s in team1)
        team2_score = sum(s[1] for s in team2)
        diff = abs(team1_score - team2_score)
        
        unique_key = tuple(sorted([tuple(sorted(s[0].summoner_name for s in team1)), 
                                   tuple(sorted(s[0].summoner_name for s in team2))]))
        
        if unique_key not in unique_combinations:
            unique_combinations.add(unique_key)
            top_combinations.append((diff, (team1, team2)))

    # Sort combinations by score difference and select top n
    top_combinations.sort(key=lambda x: x[0])
    top_n = min(top_n, len(top_combinations))
    top_n_combinations = top_combinations[:top_n]

    def _copy_clipboard(e, combination):
        blue_team, red_team = combination
        if sum(s[1] for s in blue_team) > sum(s[1] for s in red_team):
            blue_team, red_team = red_team, blue_team
        result_txt = f"""
【Blue Team】 (Score: {sum(s[1] for s in blue_team)})
{"\n".join([f"• {s[0].summoner_name} ({s[0].rank}, {s[0].lp}LP, Score: {s[1]})" for s in blue_team])}

【Red Team】 (Score: {sum(s[1] for s in red_team)})
{"\n".join([f"• {s[0].summoner_name} ({s[0].rank}, {s[0].lp}LP, Score: {s[1]})" for s in red_team])}
"""
        page.set_clipboard(result_txt)
        page.open(ft.SnackBar(content=ft.Text("Copied to clipboard")))

    # Display results
    def _create_team_container(team_members, color_name, color_code, color_code_2):
        icon_size = 16
        return ft.Container(
            content=ft.Column([
                ft.Text(color_name, size=20, color=color_code),
                ft.Text(f"Total Score: {sum(s[1] for s in team_members)}", size=icon_size),
                ft.Column([
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Image(
                                    src=s[0].player_icon,
                                    width=icon_size,
                                    height=icon_size,
                                    border_radius=ft.border_radius.all(icon_size//2),
                                ),
                                ft.Text(f"{s[0].summoner_name} ({s[0].rank}, {s[0].lp}LP, Score: {s[1]})", size=icon_size),
                            ],
                        ),
                        bgcolor=ft.colors.GREY_100,
                        border_radius=5,
                        padding=5,
                    ) for s in team_members
                ]),
            ]),
            padding=10,
            bgcolor=color_code_2,
            border_radius=10,
            width=page.width*0.4,
        )

    def create_team_view(combination):
        blue_team, red_team = combination
        if sum(s[1] for s in blue_team) > sum(s[1] for s in red_team):
            blue_team, red_team = red_team, blue_team
        random.shuffle(blue_team)
        random.shuffle(red_team)
        if page.width < 1000:
            layout = ft.ListView(expand=True)
        else:
            layout = ft.Row(expand=True, wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        layout.controls = [
            _create_team_container(blue_team, "Blue Team", ft.colors.BLUE, ft.colors.BLUE_100),
            _create_team_container(red_team, "Red Team", ft.colors.RED, ft.colors.RED_100),
        ]
        return ft.Column([
            layout,
            ft.ElevatedButton("Copy to Clipboard", on_click=lambda e, c=combination: _copy_clipboard(e, c)),
        ])

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text=f"Combination {i+1}",
                content=create_team_view(combination[1])
            ) for i, combination in enumerate(top_n_combinations)
        ],
    )

    result_dialog = ft.AlertDialog(
        title=ft.Text(f"Team Grouping Result (Top {top_n})", size=24, weight="bold"),
        content=ft.Container(
            content=tabs,
            padding=20,
            width=page.width,
            height=page.height*0.7,
        ),
        actions=[
            ft.TextButton("Close", on_click=lambda _: page.close(result_dialog)),
        ],
    )
    page.open(result_dialog)


def main(page: ft.Page):
    def _open_form(e):
        region_field = ft.TextField(label="Region", value="jp", width=100)
        summoner_name_field = ft.TextField(label="Summoner Name", width=250)
        tag_field = ft.TextField(label="Tag", value="JP1", width=100)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Enter summoner name"),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        region_field, 
                        summoner_name_field,
                        ft.Row(
                            controls=[
                                ft.Text("#", size=20, weight="bold"),
                                tag_field,
                            ],
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                width=500,
            ),
        )
        def _on_ok(e):
            region, summoner_name, tag = region_field.value, summoner_name_field.value, tag_field.value
            if search_data_multiple("Summoner", {"region": region, "summoner_name": summoner_name, "tag": tag}):
                page.close(dlg)
                page.open(ft.SnackBar(content=ft.Text("Summoner already exists.")))
                return
            if all([region, summoner_name, tag]):
                page.close(dlg)
                if _add_summoner(region, summoner_name, tag):
                    page.reload()
                else:
                    page.open(ft.SnackBar(content=ft.Text("Summoner not found.")))
            else:
                page.open(ft.SnackBar(content=ft.Text("Please enter all fields")))
        def _close_dlg(e):
            page.close(dlg)
        dlg.actions = [
            ft.TextButton("Add", on_click=_on_ok),
            ft.TextButton("Cancel", on_click=_close_dlg),
        ]
        dlg.on_dismiss = _close_dlg
        page.open(dlg)

    member_cards = ft.ListView(
        controls=[
            ft.Row(
                controls=[
                    ft.ElevatedButton("Add Member", on_click=_open_form),
                    ft.ElevatedButton("Grouping", on_click=lambda e: _grouping(page)),
                ],
            ),
        ],
        expand=True,
    )

    for summoner in get_data_list("Summoner"):
        member_cards.controls.append(
            _member_card(page, summoner)
        )

    return member_cards
    
if __name__ == "__main__":
    print(_calculate_score("master 4", 0))