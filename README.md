# BitPin

Software Engineer Task: Back-End

## How to Run?

### Easy Setup by Docker

```docker compose run app poetry run python manage.py migrate```

### Installation without Docker

1.Clone the Project:
```git clone https://github.com/SepehrBazyar/BitPin.git```

2.Navigate to the Project Directory:
```cd BitPin```

3.Create a Virtual Environment("venv" is a Selective Name):
```python3 -m venv venv```

4.Activate the Interpreter of the Virtual Environment:
    *Linux:
    ```source venv/bin/active```
    *Windows:
    ```venv\Script\active```

5.Install the Dependencies:
```pip install poetry && poetry install```

6.Create a `.env` file in root directory and add your created config:

```python
DEBUG = <project-debug-status>
SECRET_KEY = <django-insecure-secret-key>
```

7.After that, migration:

```python3 manage.py migrate```

8.Write the Following Command to Run the Server:

```python3 manage.py runserver```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
