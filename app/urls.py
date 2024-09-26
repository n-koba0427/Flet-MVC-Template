from app.controller import *
import flet as ft
import re

# URLs Module
#
# This module defines the routing configuration for the application,
# mapping URL patterns to their corresponding controller functions.
#
# Key Components:
#
# - routes: A dictionary mapping URL patterns to controller functions.
# - _convert_route_to_regex(route: str): Converts a route pattern to a regex pattern.
# - handle_route(page: ft.Page, route: str): Handles routing for the application.
#
# Custom Routes:
# To add a new route, add an entry to the `routes` dictionary:
#
# routes = {
#     # ... existing routes ...
#     "/your/new/route/<param>": your_controller_function,
# }
#
# Make sure to create the corresponding controller function in `controller.py`.


routes = {
    "/": show_home,
    "/data": show_model_list,
    "/data/<model_name>": show_data_list,
    "/data/<model_name>/add": show_data_add,
    "/data/<model_name>/edit/<id>": show_data_edit,
    "/login": show_login,
    "/sample-apps": show_sample_apps,
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