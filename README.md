# Flet-MVC-Template

Flet-MVC-Template is a lightweight, customizable MVC (Model-View-Controller) framework built on top of Flet for Python. It provides a structured approach to building web applications with clear separation of concerns.

## Features

- MVC architecture for organized and maintainable code
- Built-in routing system
- Database integration with Peewee ORM
- Customizable views and components
- Utility functions for common operations

## Project Structure
```
Flet-MVC-Template/
├── app/
│ ├── controller.py
│ ├── models.py
│ ├── urls.py
│ ├── utils.py
│ └── views.py
├── templates/
│ └── components.py
├── main.py
└── README.md
```

## Key Components

### Models (`app/models.py`)

Define your data models using Peewee ORM. The `BaseModel` class provides common functionality for all models.

Example:

```python
class YourModel(BaseModel):
    field1 = CharField()
    field2 = IntegerField()
```

### Views (`app/views.py`)

Create view functions that define the structure and layout of your pages. Each function typically returns a list of Flet controls.

Example:

```python
def your_custom_view(page: ft.Page, **params):
    return [
        header(page=page, title="Your Custom Title"),
        your_custom_component(page=page, params),
    ]
```

### Controllers (`app/controller.py`)

Implement controller functions that handle the logic between models and views. These functions process data and prepare the appropriate view to be displayed.

Example:

```python
def your_custom_controller(page: ft.Page, params):
    # Process any necessary data
    controls = your_custom_view(page=page, params)
    show_page(
        page=page,
        route="/your/custom/route",
        controls=controls
    )
```

### URLs (`app/urls.py`)

Define your application's routing by mapping URL patterns to controller functions.

Example:

```python
routes = {
    "/your/custom/route/<param>": your_custom_controller,
}
```

### Utilities (`app/utils.py`)

Utilize and extend the utility functions for common operations across your application.

Example:

```python
def your_custom_utility(arg1, arg2):
    # Your utility logic here
    return result
```

### Templates (`templates/components.py`)

The `templates` directory contains reusable UI components. These components help maintain a consistent design throughout the application.

Example:

```python
def custom_button(text: str, on_click):
    return ft.ElevatedButton(text=text, on_click=on_click)
```

## Getting Started

1. Clone this repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

## Dependencies

This project uses the following main dependencies:

- Flet: A framework for building modern web applications in Python
- Peewee: A simple and small ORM library

For a complete list of dependencies, please refer to the `requirements.txt` file.

## Customization

To extend the framework with your own functionality:

1. Add new models in `app/models.py`
2. Create new view functions in `app/views.py`
3. Implement corresponding controller functions in `app/controller.py`
4. Add new routes in `app/urls.py`
5. Create custom utility functions in `app/utils.py` as needed
6. Add reusable UI components in `templates/components.py`

### Creating Custom Components

1. Add a new function to `templates/components.py`:

```python
def custom_card(title: str, content: str):
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text(title, size=20, weight="bold"),
                ft.Text(content)
            ])),
            padding=10
        )
```

2. Use this component in your view functions:

```python
from templates.components import custom_card

def custom_view(page: ft.Page, **params):
    return [
        header(page=page, title="Custom View"),
        custom_card("Welcome", "This is a custom card component."),
    ]
```

This approach allows you to easily create and reuse custom components while maintaining a consistent UI throughout your application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.