import flet as ft
from app.urls import *
from auth.authentication import *
from app.views import *


def main(page: ft.Page):
    page.on_route_change = lambda e: handle_route(page, e.route)
    page.reload = lambda: handle_route(page, page.route) 
    page.theme_color = ft.colors.GREEN_ACCENT_200
    page.bgcolor = ft.colors.BLUE_GREY_100
    page.custom_auth = SaltedHashAuth()
    page.sample_apps = {
        "lol-custom-organizer": lol_custom_organizer_view,
    }

    page.go("/")
    
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    ft.app(target=main, port=port)