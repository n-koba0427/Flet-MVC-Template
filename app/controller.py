"""
Controller Module

This module contains controller functions that handle the logic between
models and views. Each function typically processes data and prepares
the appropriate view to be displayed.

Key Components:

- show_404(page: ft.Page, route: str, *args, **kwargs):
  Displays a 404 error page when a route is not found.

- show_data_list(page: ft.Page, **params):
  Displays a list view for a given model.

- show_data_add(page: ft.Page, **params):
  Displays a form view for adding new data to a given model.

- show_data_edit(page: ft.Page, **params):
  Displays a form view for editing existing data of a given model.

Custom Controllers:
To add a new controller function, follow this pattern:

def show_custom_view(page: ft.Page, **params):
    # Process any necessary data
    controls = custom_view_function(page=page, **params)
    show_page(
        page=page,
        route="/your/custom/route",
        controls=controls
    )

Then, add the new route to the `routes` dictionary in `urls.py`.
"""


from app.models import *
from app.views import *
from app.utils import *
import flet as ft


def show_404(page: ft.Page, route: str, *args, **kwargs):
    show_page(
        page=page,
        route=route,
        controls=error_404_view(page=page),
    )


def show_home(page: ft.Page, **params):
    show_page(
        page=page,
        route="/",
        controls=home_view(page=page),
    )


def show_model_list(page: ft.Page, **params):
    show_page(
        page=page,
        route="/data",
        controls=model_list_view(page=page),
    )


def show_data_list(page: ft.Page, **params):
    model_name = params["model_name"]
    controls = data_list_view(
        page=page,
        model_name=model_name,
    )
    show_page(
        page=page,
        route=f"/data/{model_name}",
        controls=controls,
    )
    

def show_data_add(page: ft.Page, **params):
    model_name = params["model_name"]
    controls = data_add_view(
        page=page,
        model_name=model_name,
    )
    show_page(
        page=page,
        route=f"/data/{model_name}/add",
        controls=controls,
    )


def show_data_edit(page: ft.Page, **params):
    model_name = params["model_name"]
    id = params["id"]
    controls = data_edit_view(
        page=page,
        model_name=model_name,
        id=id,
    )
    show_page(
        page=page,
        route=f"/data/{model_name}/edit/{id}",
        controls=controls,
    )

def show_login(page: ft.Page, **params):
    controls = login_view(page=page)
    show_page(
        page=page,
        route="/login",
        controls=controls,
    )

def show_sample_apps(page: ft.Page, **params):
    controls = sample_apps_view(page=page)
    show_page(
        page=page,
        route="/sample-apps",
        controls=controls,
    )
