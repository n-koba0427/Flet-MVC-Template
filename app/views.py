import flet as ft
from app.models import *
from app.utils import *


def header(page: ft.Page, title: str):
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(title, size=30, weight="bold", text_align=ft.TextAlign.CENTER),
            ],
            wrap=True,
        ),
        bgcolor=page.theme_color,
        padding=20,
        alignment=ft.alignment.center,
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
        if field_name != "id":
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


def data_list_view(page: ft.Page, model_name: str):
    return [
        header(
            page=page,
            title=f"Data List : {model_name}",
        ),
        data_lv(
            page=page,
            model_name=model_name,
        )
    ]


def data_add_view(page: ft.Page, model_name: str):
    return [
        header(
            page=page,
            title=f"Data Add : {model_name}",
        ),
        form_lv(
            page=page,
            model_name=model_name,
            redirect_to=f"/data/{model_name}"
        )
    ]


def data_edit_view(page: ft.Page, model_name: str, id: str):
    return [
        header(
            page=page,
            title=f"Data Add : {model_name}",
        ),
        form_lv(
            page=page,
            model_name=model_name,
            redirect_to=f"/data/{model_name}",
            edit_id=id,
        )
    ]