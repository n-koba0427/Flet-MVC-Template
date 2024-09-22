import flet as ft
from app.models import *

# 
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

def get_model_by_name(model_name):
    if isinstance(model_name, str):
        model_classes = {cls.__name__.lower(): cls for cls in BaseModel.__subclasses__()}
        return model_classes.get(model_name.lower(), None)
    return model_name

# data manipulation
def get_data_list(model_name):
    model = get_model_by_name(model_name)
    if exists(model):
        return model.select()
    return None

def get_data_by_id(model_name, id):
    model = get_model_by_name(model_name)
    if exists(model):
        return model.select().where(model.id==id).get()
    return None

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


# controller

def show_page(page, route, controls):
    page.views.clear()
    page.views.append(
        ft.View(route=route, controls=controls)
    )
    page.update()