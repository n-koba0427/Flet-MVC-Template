"""
Components Module for Authentication

This module contains reusable UI components for authentication views.
Each component function returns a list of Flet controls that define the UI structure.

Key Components:
- login_view(page: ft.Page):
  Creates a login view.
"""

import flet as ft
from app.utils import *


def login_form(page: ft.Page):
    username = ft.TextField(
        value="user",
        label="Username",
        autofocus=True,
        prefix_icon=ft.icons.PERSON,
    )
    password = ft.TextField(
        value="userp@ss",
        label="Password",
        password=True,
        prefix_icon=ft.icons.LOCK,
        
    )
    submit_button = ft.ElevatedButton(
        text="Login",
        icon=ft.icons.LOGIN,
    )

    def submit(e):
        if not all([username.value, password.value]):
            page.open(ft.SnackBar(content=ft.Text("Username and Password are required")))
            return
        
        result = page.custom_auth.verify_password(username.value, password.value)
        user = result["user"]
        print(f"User Object: {type(user)}")
        if exists(user):
            page.open(ft.SnackBar(content=ft.Text("Login successful")))
        else:
            page.open(ft.SnackBar(content=ft.Text("Login failed")))

    submit_button.on_click = submit

    form_container = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text("Login Form", size=24, weight=ft.FontWeight.BOLD),
                            margin=ft.margin.only(bottom=20)
                        ),
                        username,
                        password,
                        submit_button
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=40,
                border_radius=10,
                bgcolor=ft.colors.WHITE,
                width=400,
                height=400,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

    return form_container
