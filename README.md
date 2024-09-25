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
        controls=controls,
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
                ft.Text(content),
            ]),
        ),
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
            },
        ),
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

## Deployment

### Deploying to Heroku

This project can be easily deployed to Heroku. There are two main methods:

1. Using the Heroku CLI:
   a. Create a Heroku account and install the Heroku CLI.
   b. In your project's root directory, run the following commands:

   ````
   heroku create
   git push heroku main
   ```

2. Connecting directly to your GitHub repository:
   a. Create a Heroku account and go to your Heroku Dashboard.
   b. Create a new app and go to the "Deploy" tab.
   c. In the "Deployment method" section, choose "GitHub".
   d. Connect your GitHub account and select the repository.
   e. Choose the branch you want to deploy and enable automatic deploys if desired.

Both methods will deploy your Flet-MVC-Template application to Heroku, making it accessible online. The GitHub integration method offers the advantage of automatic deployments whenever you push changes to your repository.

### Sample Application

You can view a live sample of the Flet-MVC-Template in action at the following URL:

[https://flet-mvc-template-03c5ed9c5b93.herokuapp.com/](https://flet-mvc-template-03c5ed9c5b93.herokuapp.com/)

This sample application demonstrates the features and usage of the Flet-MVC-Template, providing a practical example of how to structure and build web applications using this framework.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## AI-Assisted Development

This README was created with the assistance of an AI chatbot.

In the process of creating this template, organizing its structure, and documenting it, we utilized ChatGPT to efficiently and systematically produce output. Specifically, we used AI to save time on the overall composition of the article and detailed explanations, while providing clear and concise content. We plan to continue using AI as a support tool for future developments and improvements.

Please note that this section is merely a formal report. If you are interested in the project or have detailed questions about the template, we are more than willing to engage in thorough communication via messages. Feel free to contact us.