"""
Views Module

This module contains view functions that define the structure and layout
of different pages in the application. Each function typically returns
a list of Flet controls that make up the UI for a specific view.

Key Components:\
- error_404_view(page: ft.Page):
  Creates a view for displaying a 404 error page.

- data_list_view(page: ft.Page, model_name: str):
  Creates a view for listing data of a specific model.

- data_add_view(page: ft.Page, model_name: str):
  Creates a view for adding new data to a specific model.

- data_edit_view(page: ft.Page, model_name: str, id: str):
  Creates a view for editing existing data of a specific model.

Custom Views:
To add a new view function, follow this pattern:

def custom_view(page: ft.Page, **params):
    return [
        header(page=page, title="Your Custom Title"),
        your_custom_component(page=page, **params),
    ]

Then, create a corresponding controller function in `controller.py`
and add the new route to the `routes` dictionary in `urls.py`.
"""


import flet as ft
from templates.components.basic import *
from templates.components.auth import *


def error_404_view(page: ft.Page):
    return [
        header(page=page, title="404 - Page not found"),
        breadcrumbs(page=page),
        ft.Text("404 - Page not found")
    ]


def home_view(page: ft.Page):
    return [
        header(page=page, title="Home"),
        breadcrumbs(page=page),
        customized_markdown(
            page=page,
            filename="sample.home.md",
        )
    ]

def model_list_view(page: ft.Page):
    registered_models = get_registered_models()
    patterns = {
        "model_links": "\n".join([f"- [{model_name}](/data/{model_name})" for model_name in registered_models.keys()])
    }

    return [
        header(page=page, title="Model List"),
        breadcrumbs(page=page),
        customized_markdown(
            page=page,
            filename="sample.model_list_view.md",
            patterns=patterns,
        )
    ]


def data_list_view(page: ft.Page, model_name: str):
    return [
        header(
            page=page,
            title=f"Data List : {model_name}",
        ),
        breadcrumbs(page=page),
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
        breadcrumbs(page=page),
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
        breadcrumbs(page=page),
        form_lv(
            page=page,
            model_name=model_name,
            redirect_to=f"/data/{model_name}",
            edit_id=id,
        )
    ]


def login_view(page: ft.Page):
    return [
        header(page=page, title="Login"),
        breadcrumbs(page=page),
        login_form(page=page),
    ]
