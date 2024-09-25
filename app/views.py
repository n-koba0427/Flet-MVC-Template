import flet as ft
from templates.components import *

# Views Module
#
# This module contains view functions that define the structure and layout
# of different pages in the application. Each function typically returns
# a list of Flet controls that make up the UI for a specific view.
#
# Key Components:
#
# - data_list_view(page: ft.Page, model_name: str):
#   Creates a view for listing data of a specific model.
#
# - data_add_view(page: ft.Page, model_name: str):
#   Creates a view for adding new data to a specific model.
#
# - data_edit_view(page: ft.Page, model_name: str, id: str):
#   Creates a view for editing existing data of a specific model.
#
# Custom Views:
# To add a new view function, follow this pattern:
#
# def custom_view(page: ft.Page, **params):
#     return [
#         header(page=page, title="Your Custom Title"),
#         your_custom_component(page=page, **params),
#     ]
#
# Then, create a corresponding controller function in `controller.py`
# and add the new route to the `routes` dictionary in `urls.py`.


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