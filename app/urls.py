from app.controller import *
import flet as ft
import re


routes = {
    "/data/<model_name>": show_data_list,
    "/data/<model_name>/add": show_data_add,
    "/data/<model_name>/edit/<id>": show_data_edit,
}

def _convert_route_to_regex(route: str):
    return re.sub(r"<([^>]+)>", r"(?P<\1>[^/]+)", route)

def handle_route(page: ft.Page, route: str):
    for pattern, controller in routes.items():
        regex_pattern = _convert_route_to_regex(pattern)
        match = re.match(f"^{regex_pattern}$", route)
        if match:
            params = match.groupdict()
            controller(page, **params)
            return
    show_404(page, route)