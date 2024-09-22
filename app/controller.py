from app.models import *
from app.views import *
from app.utils import *
import flet as ft


def show_404(page: ft.Page, route: str, *args, **kwargs):
    show_page(
        page=page,
        route=route,
        controls=[ft.Text("404 - Page not found")]
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