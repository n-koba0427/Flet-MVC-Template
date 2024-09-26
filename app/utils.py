"""
Utilities Module

This module contains utility functions that are used across the application
for various purposes such as data manipulation, model operations, and view helpers.

Key Components:

- exists(x): Checks if a value is not None.
- get_items(model_or_data): Yields (field_name, field_value) pairs for a model or data instance.
- get_model_by_name(model_name): Returns the model class corresponding to a given name.
- get_data_list(model_name): Retrieves all data entries for a given model.
- get_data_by_id(model_name, id): Retrieves a specific data entry by its ID.
- add_data(model_name, data_dict): Adds a new data entry for a given model.
- update_data(model_name, id, data_dict): Updates an existing data entry.
- delete_data(model_name, id): Deletes a specific data entry.
- show_page(page, route, controls): Updates the page with new controls and route.

Custom Utilities:
To add a new utility function, simply define it in this file:

def your_custom_utility(arg1, arg2):
    # Your utility logic here
    return result

You can then import and use your custom utility in other parts of the application.
"""

import os
import re
import flet as ft
from app.models import *


# general
def exists(x):
    return x is not None

# models
def get_items(model_or_data):
    for field_name in model_or_data._meta.fields.keys():
        if isinstance(model_or_data, type):
            field_value = None
        else:
            field_value = getattr(model_or_data, field_name)
        yield (field_name, field_value)

def get_registered_models():
    return {cls.__name__.lower(): cls for cls in BaseModel.__subclasses__()}

def get_model_by_name(model_name):
    if isinstance(model_name, str):
        return get_registered_models().get(model_name.lower(), None)
    return model_name

# data manipulation
def get_data_list(model_name):
    model = get_model_by_name(model_name)
    if exists(model):
        return model.select()
    return None

def search_data(model_name, key, value):
    model = get_model_by_name(model_name)
    if exists(model):
        try:
            return model.select().where(getattr(model, key) == value)
        except:
            return None
    return None

def get_data_by_id(model_name, id):
    return search_data(model_name, "id", id).get()

def add_data(model_name, data_dict):
    model = get_model_by_name(model_name)
    if exists(model):
        data = model.create(**data_dict)
        data.save()
        return data
    return None

def update_data(model_name, id, data_dict):
    model = get_model_by_name(model_name)
    if exists(model):
        data = model.get_by_id(id)
        for field_name, field_value in data_dict.items():
            if hasattr(data, field_name):
                setattr(data, field_name, field_value)
        data.save()
        return data
    return None

def delete_data(model_name, id):
    model = get_model_by_name(model_name)
    if exists(model):
        data = model.get_by_id(id)
        data.delete_instance()
        return model
    return None


# views
def handle_markdown_tap_link(page, e):
    page.go(e.data)

def read_markdown_file(filename: str, patterns: dict):
    file_path = os.path.join('templates', 'markdown', filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 二重中括弧で囲まれたプレースホルダーを置換
    for key, value in patterns.items():
        pattern = r'%%' + re.escape(key) + r'%%'
        content = re.sub(pattern, str(value), content)
    
    return content

# authentication
def authenticate(view_function):
    def wrapper(*args, **kwargs):
        page = kwargs["page"]
        if exists(page.session.get("user")):
            return view_function(*args, **kwargs)
        else:
            from app.views import login_view
            return login_view(page=page)
    return wrapper


# controller
def show_page(page, route, controls):
    page.views.clear()
    page.views.append(
        ft.View(route=route, controls=controls)
    )
    page.update()