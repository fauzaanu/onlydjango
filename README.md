# Only Django - Boilerplate Template

This boilerplate template is designed to help you build Django applications quickly, leveraging Django’s features and integrating modern tools for efficient development.

## Frontend

- **Templates:** We use Django templates for rendering views.
- **Dynamic UI Updates:** Utilize [HTMX](https://htmx.org/) for dynamic updates.
- **Client-Side Interactivity:** Implement [Alpine.js](https://alpinejs.dev/) for handling client-side UI interactions.
- **Styling:** [Tailwind CSS](https://tailwindcss.com/) is used for styling, with optional integration of additional libraries like [Font Awesome](https://fontawesome.com/) for icons.

## Backend

- **Business Logic:** Most business logic is encapsulated within `models.py`. For instance, if a template needs to check the state of a database object, the logic is typically managed via model methods.
- **Context Handling:** If a model method alone cannot handle the logic, it will be moved to `views.py`.

## AI for Coding

- **Code Assistance:** This template includes aider, a better alternative to Cursor for enhanced coding support that gives you privacy + doesnt force you to break out of your already productive IDE

## Background Tasks

- **Task Processing:** By default, background tasks are managed using [Huey](https://huey.readthedocs.io/en/latest/), a simple task queue.
- **Celery Support:** Configuration files for Celery are included for more complex task handling, available in the Railway JSON files.

## 1-Click Deployment

- **Railway Integration:** This template is optimized for one-click deployment on [Railway](https://railway.app/) with minimal configuration required.
