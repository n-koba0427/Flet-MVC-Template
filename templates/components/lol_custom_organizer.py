import flet as ft
import requests
from bs4 import BeautifulSoup
import itertools
import random

from app.utils import *

def _calculate_score(rank: str, lp: str):
    tires = ["iron", "bronze", "silver", "gold", "platinum", "emerald", "diamond", "master", "grandmaster", "challenger"]
    tire, division = rank.split(" ")
    return (tires.index(tire) * 4 + int(division) - 1) * 100 + int(lp)


def _get_summoner_max_score(region: str="jp", summoner_name: str="naoyashiyashi", tag: str="JP1"):
    url = f'https://www.op.gg/summoners/{region}/{summoner_name}-{tag}'
    response = requests.get(url)
    player_icon = "https://opgg-static.akamaized.net/meta/images/profile_icons/profileIcon29.jpg?image=e_upscale,q_auto:good,f_webp,w_auto&v=1724034092925"
    max_rank = "Unranked"
    max_lp = 0
    max_score = 0
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
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

def _change_summoner_status(e, page: ft.Page, summoner: Summoner):
    summoner.is_active = e.control.value
    summoner.save()
    page.reload()

def _member_card(page: ft.Page, summoner: Summoner):
    _card = ft.Container(
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

    return _card


def _add_summoner(region: str, summoner_name: str, tag: str):
        player_icon, max_rank, max_lp, max_score = _get_summoner_max_score(
            region=region,
            summoner_name=summoner_name,
            tag=tag
        )
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
            }
        )

def _get_active_summoners():
    return search_data("Summoner", "is_active", True)


def _grouping(page: ft.Page, top_n: int = 10):
    active_summoners = _get_active_summoners()
    if len(active_summoners) != 10:
        page.open(ft.SnackBar(content=ft.Text("10 active summoners are required.")))
        return

    # Convert summoners to tuples with their scores
    summoners = [(s, int(s.score)) for s in active_summoners]
    # Generate all possible combinations of 5 summoners
    all_combinations = list(itertools.combinations(summoners, 5))

    top_combinations = []

    # Calculate score differences for all combinations
    for combo in all_combinations:
        team1 = list(combo)
        team2 = [s for s in summoners if s not in team1]
        team1_score = sum(s[1] for s in team1)
        team2_score = sum(s[1] for s in team2)
        diff = abs(team1_score - team2_score)
        top_combinations.append((diff, (team1, team2)))

    # Sort combinations by score difference and select top n
    top_combinations.sort(key=lambda x: x[0])
    top_n = min(top_n, len(top_combinations))  # Ensure top_n doesn't exceed available combinations
    top_n_combinations = top_combinations[:top_n]

    # Randomly choose one combination from the top n
    _, best_combination = random.choice(top_n_combinations)
    
    blue_team, red_team = best_combination
    # Ensure blue team has lower total score
    if sum(s[1] for s in blue_team) > sum(s[1] for s in red_team):
        blue_team, red_team = red_team, blue_team

    # Shuffle members within each team
    random.shuffle(blue_team)
    random.shuffle(red_team)

    # Display results
    result_dialog = ft.AlertDialog(
        title=ft.Text("Team Grouping Result", size=24, weight="bold"),
        content=ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text("Blue Team", size=20, color=ft.colors.BLUE),
                        ft.Text(f"Total Score: {sum(s[1] for s in blue_team)}", size=16),
                        ft.Column([
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Image(
                                            src=s[0].player_icon,
                                            width=14,
                                            height=14,
                                            border_radius=ft.border_radius.all(7),
                                        ),
                                        ft.Text(f"{s[0].summoner_name} ({s[0].rank}, {s[0].lp}LP, Score: {s[1]})", size=14),
                                    ],
                                ),
                                bgcolor=ft.colors.BLUE_50,
                                border_radius=5,
                                padding=5,
                            ) for s in blue_team
                        ]),
                    ]),
                    padding=10,
                    bgcolor=ft.colors.BLUE_100,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("Red Team", size=20, color=ft.colors.RED),
                        ft.Text(f"Total Score: {sum(s[1] for s in red_team)}", size=16),
                        ft.Column([
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Image(
                                            src=s[0].player_icon,
                                            width=14,
                                            height=14,
                                            border_radius=ft.border_radius.all(7),
                                        ),
                                        ft.Text(f"{s[0].summoner_name} ({s[0].rank}, {s[0].lp}LP, Score: {s[1]})", size=14),
                                    ],
                                ),
                                bgcolor=ft.colors.BLUE_50,
                                border_radius=5,
                                padding=5,
                            ) for s in red_team
                        ]),
                    ]),
                    padding=10,
                    bgcolor=ft.colors.RED_100,
                    border_radius=10,
                ),
            ]),
            padding=20,
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
            if all([region, summoner_name, tag]):
                _add_summoner(region, summoner_name, tag)
                page.close(dlg)
                page.reload()
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
        spacing=10
    )

    for summoner in get_data_list("Summoner"):
        member_cards.controls.append(
            _member_card(page, summoner)
        )

    return member_cards
    
