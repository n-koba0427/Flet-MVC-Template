# Flet-MVC-Template

Flet-MVC-Template is a lightweight, customizable MVC (Model-View-Controller) framework built on top of Flet for Python. It provides a structured approach to building web applications with clear separation of concerns.

## Features

- MVC architecture for organized and maintainable code
- Built-in routing system
- Database integration with Peewee ORM
- Customizable views and components
- Utility functions for common operations
- Markdown template support

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
│ ├── components.py
│ └── markdown/
│     ├── home.md
│     └── model_list.md
├── static/
│ ├── css/
│ ├── js/
│ └── images/
├── main.py
└── README.md
```

## Key Components

### Models (`app/models.py`)

Define your data models using Peewee ORM. The `BaseModel` class provides common functionality for all models.

Example:

```python # app/models.py
class YourModel(BaseModel):
    field1 = CharField()
    field2 = IntegerField()
```

### Views (`app/views.py`)

Create view functions that define the structure and layout of your pages. Each function typically returns a list of Flet controls.

Example:

```python # app/views.py
def your_custom_view(page: ft.Page, **params):
    return [
        header(page=page, title="Your Custom Title"),
        your_custom_component(page=page, params),
    ]
```

### Controllers (`app/controller.py`)

Implement controller functions that handle the logic between models and views. These functions process data and prepare the appropriate view to be displayed.

Example:

```python # app/controller.py
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

```python # app/urls.py
routes = {
    "/your/custom/route/<param>": your_custom_controller,
}
```

### Utilities (`app/utils.py`)

Utilize and extend the utility functions for common operations across your application.

Example:

```python # app/utils.py
def your_custom_utility(arg1, arg2):
    # Your utility logic here
    return result
```

### Templates (`templates/components.py` and `templates/markdown/`)

The `templates` directory contains reusable UI components and markdown templates. These components help maintain a consistent design throughout the application.

Component example:

```python # templates/components.py
def custom_button(text: str, on_click):
    return ft.ElevatedButton(text=text, on_click=on_click)
```

Markdown template example (`templates/markdown/model_list.md`):

``` # templates/markdown/model_list.md
# {{page_title}}
The following pages are available:
{{model_links}}
```

## Getting Started

1. Clone this repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the application: `flet run --web --port 8080`

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
7. Add new markdown templates in `templates/markdown/`

### Creating Custom Components and Views

1. Add a new function to `templates/components.py`:

```python # templates/components.py
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

If you need to use a markdown file, you can use the `customized_markdown` function in `app/utils.py` as shown below:

``` # templates/markdown/your_markdown_file.md
# Custom View
This is a custom markdown file.
Variable values can be passed to the markdown file using the `patterns` parameter and the double percent sign (%%) as shown below:
%%your_pattern_name%%
```

```python # app/views.py
def custom_markdown(page: ft.Page, **params):
    return [
        header(page=page, title="Custom View"),
        customized_markdown(
            page=page,
            filename="your_markdown_file.md",
            patterns={
                "your_pattern_name": "your_pattern_value",
            }
        )
    ]
```

2. Use this component in a view function in `app/views.py`:

```python # app/views.py
from templates.components import custom_card

def custom_view(page: ft.Page, **params):
    return [
        header(page=page, title="Custom View"),
        custom_card("Welcome", "This is a custom card component."),
    ]
```

3. Implement a corresponding controller function in `app/controller.py`:

```python # app/controller.py
from app.views import custom_view
from app.utils import show_page

def custom_controller(page: ft.Page, params):
    controls = custom_view(page=page, params=params)
    show_page(
        page=page,
        route="/custom",
        controls=controls
    )
```

4. Add a new route in `app/urls.py`:

```python # app/urls.py
routes = {
    "/custom": custom_controller,
    # Other existing routes...
}
```

This approach allows you to easily create and reuse custom components while maintaining a consistent UI throughout your application. By adding new views and controllers and routing them appropriately, you can extend the functionality of your application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.