# Only Django - Still a WIP

The boilerplate template for building applications fast without going outside of django for the most part.

## Frontend

We would be using django templates. For dynamic UI updates we would be using htmx and alpinejs would be used for most client side UI updates. We would be using tailwindcss for styling and any extra libraries that is relevant can be used such as fontawesome.

## Backend

The general idea of this boilerplate is that `models.py` would contain most business logic within each model. For example if a template requires to check the state of a certain database object, there will be a model method for that. If a model method alone cannot handle this, only then would we bring this logic into views.py and pass in as additional context. For the most part, the only context that gets passed will be the database object itself

## AI for Coding

This template also includes aider a much better alternative to cursor IMO.

## Background Tasks

Background tasks are by default processed through huey a very simple task que. However Celery based launch configs are present in the railway json files.

## 1-click deploy to Railway

This template is also optimized so that it can be deployed instantly to railway without any additional configurations
