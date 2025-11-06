---
inclusion: always
---

# N+1 Queries and avoiding them

As mentioned in another steering document, we should use models to store business logic for the view using a classmethod.
The use of classmethods actually enables us to avoid N+1 quite a lot as we have the models in the same place and we can optimize
for the whole get for view function in a way that N+1 wont happen.

This includes using prefetch_related and select_related mainly but in extremely data heavy stuff annotations and all the custom 
methods provided by the django ORM should be considered. to be used.

> TLDR: use `prefetch_related` and `select_related`