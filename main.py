import flet as ft
from app.urls import *


def main(page: ft.Page):
    page.on_route_change = lambda e: handle_route(page, e.route)
    page.reload = lambda: handle_route(page, page.route) 
    page.theme_color = ft.colors.GREEN_ACCENT_200

    page.go("/")
    
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    ft.app(target=main, port=port)

