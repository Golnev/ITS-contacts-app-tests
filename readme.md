![Static Badge](https://img.shields.io/badge/code%20style-Black-black)

# ITS tests for the contacts app

## Описание

Это проект с автотестами для UI и API. Проект использует `pytest` и `selenium` для выполнения тестов и `pytest-html` для
создания отчета в формате HTML. Запусков тестов происходит через команды `pytest`.

## Установка зависимостей

Перед запуском тестов необходимо установить все зависимости:

```sh
  pip install -r requirements.txt
```

# Запуск тестов

Перед запуском тестов необходимо:

- зарегистрироваться на тестируемом сайте **https://thinking-tester-contact-list.herokuapp.com/**
- заменить данные авторизации в .env
- заменить пути к браузерам `firefox` и `google chrome`
- заменить пути к `geckodriver` и `chromedriver`

Для запуска тестов с помощью pytest выполните следующую команду:

```sh
  pytest
```

### Для создания отчета в формате HTML используйте команду:

```sh
  pytest --html="путь/к/файлу/report.html" --self-contained-html
```

# Маркеры и парсеры

- Общие Маркеры:
    + Тесты UI - `ui`
    + Тесты API - `api`

- Маркеровка тестов UI распределена по тестируемым страницам:
    + Login Page - `mark.login`
    + Register Page - `mark.register`
    + Contact List Page - `mark.contact_list`
    + Add New Contact Page - `mark.add_new_contact_page`
    + Contact Details Page - `mark.contact_details_page`
    + Edit Contact Page - `mark.edit_contact_page`
- Маркеровка тестов API:
    + Маркер **auth** для тестирования login и logout.
    + Маркер **users** для тестирования пользователей.
    + Маркер **contacts** для тестирования контактов.

- Парсер **--rm** для удаления данных после тестирования.
- Парсер **--browser_name** для выбора браузера для тестирования. Принимает значения `chrome` или `firefox`. Дефолтное
  значение - `firefox`.