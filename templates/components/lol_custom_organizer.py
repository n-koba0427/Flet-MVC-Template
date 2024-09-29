import flet as ft
import requests
from bs4 import BeautifulSoup
import itertools
import random

from app.utils import *
from templates.components.basic import *

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
    max_rank = "unranked"
    max_lp = 0
    max_score = 0
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        error_msg = soup.find('div', class_='e19vm62i1')
        if error_msg:
            return None, None, None, None
        player_icon = soup.find('div', class_='profile-icon').find("img").get("src")
        rank_base = soup.find('div', class_='e15k6o3w0')
        if exists(rank_base):
            rank_info = rank_base.find("tbody")
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

def generate_ranks_with_divisions():
    base_ranks = ["iron", "bronze", "silver", "gold", "platinum", "emerald", "diamond"]
    top_ranks = ["master", "grandmaster", "challenger"]
    ranks = ["unranked"]
    for rank in base_ranks:
        for division in range(4, 0, -1):
            ranks.append(f"{rank} {division}")
    ranks.extend(top_ranks)
    return ranks

def _member_card(page: ft.Page, summoner: Summoner):
    def _delete_summoner(e, summoner):
        delete_data("Summoner", summoner.id)
        page.reload()

    def _change_rank(e, summoner):
        summoner.rank = e.control.value
        summoner.score = _calculate_score(summoner.rank, summoner.lp)
        summoner.save()
        page.reload()

    def _submit_lp(e, summoner):
        value = e.control.value
        if value.isdigit():
            if 0 <= int(value) <= 100:
                summoner.lp = value
                summoner.score = _calculate_score(summoner.rank, summoner.lp)
                summoner.save()
                page.reload()
                return
            else:
                msg = "LP must be between 0 and 100."
        else:
            msg = "Please enter a number."
        page.reload()
        page.open(ft.SnackBar(content=ft.Text(msg)))
        
    text_size = 20

    ranks_with_divisions = generate_ranks_with_divisions()

    title = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row( 
                    controls=[
                        ft.Image(
                            src=summoner.player_icon,
                            width=text_size*1.6,
                            height=text_size*1.6,
                            border_radius=ft.border_radius.all(text_size),
                        ),
                        ft.Text(f"{summoner.summoner_name} #{summoner.tag}", size=text_size*0.8, weight="bold"),
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_size=text_size*1.5,
                            on_click=lambda e, summoner=summoner: _delete_summoner(e, summoner),
                        ),
                        ft.Switch(
                            value=summoner.is_active,
                            on_change= lambda e, page=page, summoner=summoner: _change_summoner_status(e, page, summoner),
                        ),
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        bgcolor=ft.colors.SECONDARY_CONTAINER if summoner.is_active else ft.colors.GREY_100,
        border_radius=ft.border_radius.all(text_size*0.75),
        padding=ft.padding.all(text_size*0.2),
    )
    
    subtitle = ft.Row(
        controls=[
            ft.Dropdown(
                options=[
                    ft.dropdown.Option(rank) for rank in ranks_with_divisions
                ],
                value=summoner.rank,
                width=text_size*5.6,
                # content_padding=0,
                alignment=ft.alignment.center,
                text_style=ft.TextStyle(size=text_size*0.75, color=ft.colors.GREY_700, weight="bold"),
                border=ft.InputBorder.NONE,
                border_radius=ft.border_radius.all(text_size*0.75),
                on_change=lambda e, summoner=summoner: _change_rank(e, summoner),
            ),
            ft.TextField(
                value=summoner.lp,
                width=text_size,
                text_style=ft.TextStyle(size=text_size*0.75, color=ft.colors.GREY_700, weight="bold"),
                border=ft.InputBorder.NONE,
                border_radius=ft.border_radius.all(text_size*0.75),
                on_blur=lambda e, summoner=summoner: _submit_lp(e, summoner),
            ),
            ft.Text(f"LP , Score: {summoner.score} ", size=text_size*0.75, weight="bold", color=ft.colors.GREY_700),
        ],
    )

    def _change_subtitle_visibility(e):
        subtitle.visible = not subtitle.visible
        subtitle.update()

    champs_name = summoner.champs_name.split("|")
    champs_point = summoner.champs_point.split("|")
    _card = ft.ExpansionTile(
        title=title,
        subtitle=subtitle,
        controls=[
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Image(
                                src=f"https://opgg-static.akamaized.net/meta/images/lol/latest/champion/{champ_name.replace(" ", "").replace("'", "")}.png?image=e_upscale,c_crop,h_103,w_103,x_9,y_9/q_auto:good,f_webp,w_160,h_160&v=1724034092925",
                                width=text_size*2,
                                height=text_size*2,
                                border_radius=ft.border_radius.all(text_size*0.5),
                            ),
                            ft.Text(champ_name, size=text_size*0.5, weight="bold"),
                            ft.Text(champ_point, size=text_size*0.5, weight="bold"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ) for champ_name, champ_point in zip(champs_name, champs_point)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
        ],
        on_change=lambda e: _change_subtitle_visibility(e),
    )
    _card.subtitle.visible = False
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
**【Blue Team】 (Total Score: {sum(s[1] for s in blue_team)})**
{"\n".join([f"    • **{s[0].summoner_name}**  ({s[0].rank}, {s[0].lp}LP)" for s in blue_team])}

**【Red Team】 (Total Score: {sum(s[1] for s in red_team)})**
{"\n".join([f"    • **{s[0].summoner_name}**  ({s[0].rank}, {s[0].lp}LP)" for s in red_team])}
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

def _clean_text(text):
    problematic_chars = ["\u2069", "\u2066"]
    for problematic_char in problematic_chars:
        text = text.replace(problematic_char, "")
    text = text.replace("\r\n", "\n")
    return text.split("\n")

def _extract_summoner_name(join_msg):
    join_msg_list = _clean_text(join_msg)
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
        tag_list.append(tag.replace(" ", ""))
    return summoner_name_list, tag_list

def main(page: ft.Page):
    def _open_form(e, quick_add: bool = False):
        region_field = ft.TextField(label="Region", value="jp", width=100)
        summoner_name_field = ft.TextField(label="Summoner Name", width=250)
        tag_sharp = ft.Text("#", size=20, weight="bold")
        tag_field = ft.TextField(label="Tag", value="JP1", width=100)
        quick_field = ft.TextField(
            label="Please paste the lobby log here.", 
            width=350, 
            multiline=True, 
            min_lines=10,
            visible=False,
        )
        if quick_add:
            quick_field.visible = True
            summoner_name_field.visible = False
            tag_sharp.visible = False
            tag_field.visible = False
        
        dlg = ft.AlertDialog(
            title=ft.Text("Enter summoner name"),
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        region_field, 
                        summoner_name_field,
                        ft.Row(
                            controls=[
                                tag_sharp,
                                tag_field,
                            ],
                        ),
                        quick_field,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                width=500,
            ),
        )

        def _on_ok(e):
            page.close(dlg)

            msg = ""
            reload_flag = False
            if quick_add:
                region = region_field.value
                summoner_name_list, tag_list = _extract_summoner_name(quick_field.value)
                query = get_model_by_name("Summoner").update(is_active=False)
                query.execute()
                reload_flag = True
            else:
                region, summoner_name_list, tag_list = region_field.value, [summoner_name_field.value], [tag_field.value]
            
            processing_dlg = ProcessingDialog(total_count=len(summoner_name_list), message="Fetching summoner information")
            page.open(processing_dlg.content)
            
            for summoner_name, tag in zip(summoner_name_list, tag_list):
                summoner_query = search_data_multiple("Summoner", {"region": region, "summoner_name": summoner_name, "tag": tag})
                # check if summoner already exists
                summoner = summoner_query.first()
                if summoner:
                    summoner.is_active = True
                    summoner.save()
                    msg += f"{summoner_name}#{tag} already exists.\n"
                # check if all fields are filled
                else:
                    if all([region, summoner_name, tag]):
                        # add summoner
                        summoner = _add_summoner(region, summoner_name, tag)
                        if summoner:
                            reload_flag = True
                            msg += f"{summoner_name}#{tag} added.\n"
                        else:
                            msg += f"{summoner_name}#{tag} not found.\n"
                    else:
                        msg += "Please enter all fields.\n"
                processing_dlg.update_progress()

            page.close(processing_dlg.content)

            if reload_flag:
                page.reload()
            page.open(ft.SnackBar(content=ft.Text(msg[:-1])))
            

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
                    ft.ElevatedButton("Quick Add", on_click=lambda e: _open_form(e, quick_add=True)),
                    ft.ElevatedButton("Grouping", on_click=lambda e: _grouping(page)),
                ],
            ),
        ],
        expand=True,
    )

    # サモナーのリストを取得し、is_activeとscoreでソート
    summoners = get_data_list("Summoner")
    sorted_summoners = sorted(summoners, key=lambda s: (-s.is_active, -int(s.score)))

    for summoner in sorted_summoners:
        member_cards.controls.append(
            _member_card(page, summoner)
        )

    return member_cards
    
if __name__ == "__main__":
    print(_calculate_score("master 4", 0))