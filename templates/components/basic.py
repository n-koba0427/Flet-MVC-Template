"""
Basic Components Module

This module contains reusable UI components that can be used across multiple views.
Each component function returns a list of Flet controls that define the UI structure.

Key Components:
- header(page: ft.Page, title: str):
  Creates a header component with a title.

- breadcrumbs(page: ft.Page, separator: str=" / ", active_color: str=ft.colors.BLUE, inactive_color: str=ft.colors.GREY, home_content: ft.Control=ft.Icon(ft.icons.HOME)):
  Creates a breadcrumbs component with customizable colors and home icon.

- data_lv(page: ft.Page, model_name: str):
  Creates a list view for a given model.

- form_lv(page: ft.Page, model_name: str, redirect_to: str, edit_id: str=None):
  Creates a form view for adding or editing data of a given model.
"""


import flet as ft
from app.utils import *


def header(page: ft.Page, title: str):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(title, size=30, weight="bold", text_align=ft.TextAlign.CENTER),
            ],
            wrap=True,
        ),
        bgcolor=ft.colors.PRIMARY,
        padding=20,
        alignment=ft.alignment.center,
    )


def breadcrumbs(
        page: ft.Page,
        separator: str=" / ",
        active_color: str=ft.colors.BLUE,
        inactive_color: str=ft.colors.GREY,
        home_content: ft.Control=ft.Icon(ft.icons.HOME),
    ):
    parts = page.route.strip("/").split("/")

    home_content.color = inactive_color
    if parts[0] == "":
        home_content.color = active_color

    crumbs = ft.Row(
        controls=[
            ft.Container(
                content=home_content,
                on_click=lambda _: page.go("/"),
                padding=5,
                border_radius=5,
            ),
            ft.Text(separator, color=inactive_color)
        ],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    for i, part in enumerate(parts):
        if i > 0:
            crumbs.controls.append(ft.Text(separator, color=inactive_color))
        
        crumb_text = ft.Text(
            part.capitalize(),
            color=active_color if i == len(parts) - 1 else inactive_color,
            weight="bold" if i == len(parts) - 1 else "normal",
        )
        
        if i < len(parts) - 1:
            crumb = ft.Container(
                content=crumb_text,
                on_click=lambda _, p=i: page.go("/" + "/".join(parts[:p+1])),
                padding=5,
                border_radius=5,
            )
        else:
            crumb = crumb_text
        
        crumbs.controls.append(crumb)

    return ft.Container(
        content=crumbs,
        padding=10,
        border=ft.border.all(1, ft.colors.GREY_300),
        border_radius=5,
        margin=ft.margin.only(bottom=10),
    )


def customized_markdown(page: ft.Page, filename: str, patterns: dict={}):
    return ft.Markdown(
        value=read_markdown_file(filename, patterns),
        selectable=True,
        on_tap_link=lambda e: handle_markdown_tap_link(page, e),
    )


def data_lv(page: ft.Page, model_name: str):
    data_list = get_data_list(model_name)
    if not exists(data_list):
        return ft.Text(f"Model \"{model_name}\" not found")

    # list view
    lv = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True,
    )

    def _delete(id):
        delete_data(model_name, id)
        page.reload()

    for data in data_list:
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[]
                ),
                margin=10
            )
        )
        for field_name, field_value in get_items(data):
            card.content.content.controls.append(
                ft.Text(
                    value=f"{field_name}: {field_value}",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                )
            )
        card.content.content.controls.append(
            ft.Row([
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    on_click=lambda _, id=data.id: page.go(f"{page.route}/edit/{id}")
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    on_click=lambda _, id=data.id: _delete(id)
                )
            ])
        )
        lv.controls.append(card)

    # add button
    add_button = ft.ElevatedButton(
        text="ADD",
        on_click=lambda _: page.go(f"{page.route}/add")
    )
    lv.controls.append(add_button)
    return lv


def form_lv(page: ft.Page, model_name: str, redirect_to: str, edit_id: str=None):
    if exists(edit_id):
        model_or_data = get_data_by_id(model_name, edit_id)
    else:
        model_or_data = get_model_by_name(model_name)
    
    if not exists(model_or_data):
        return ft.Text(f"Model \"{model_name}\" not found")

    # list view : form
    lv = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
    )
    
    for field_name, field_value in get_items(model_or_data):
        if field_name not in ["id", "salt"]:
            lv.controls.append(
                ft.TextField(
                    label=field_name,
                    value="" if field_value is None else field_value,
                )
            )

    # add button
    def submit_data(e):
        data_dict = {}
        fields = lv.controls[:-1]
        blank=False
        for field in fields:
            if not field.value:
                blank = True
                break
            data_dict[field.label] = field.value

        if not blank:
            if exists(edit_id):
                update_data(model_name, edit_id, data_dict)
            else:
                if model_name == "user":
                    page.custom_auth.add_user(data_dict)
                else:
                    add_data(model_name, data_dict)
            page.go(redirect_to)
        else:
            dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text("All fields are required"),
                actions=[
                    ft.ElevatedButton(
                        content=ft.Text("OK"),
                        on_click=lambda e: page.close(dialog)
                    )
                ],
            )
            page.open(dialog)

    submit_button = ft.ElevatedButton(
        text="SUBMIT",
        on_click=submit_data
    )
    
    lv.controls.append(submit_button)
    return lv


def sample_apps_lv(page: ft.Page):
    sample_apps_lv = ft.ListView(expand=True, spacing=10)
    for app_name, _ in page.sample_apps.items():
        sample_apps_lv.controls.append(
            ft.ElevatedButton(
                text=app_name,
                on_click=lambda e: page.go(f"/sample-apps/{app_name}"),
            )
        )
    return sample_apps_lv
