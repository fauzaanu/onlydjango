# onlydjango

> Note: Both the readme and the code in the repo are a work in progress and is incomplete!

The idea of `onlydjango` is to 
- Use onlydjango (obviousely)
- Make deploying Django really easy
- Make it easy to implement a task que in Django
- Utilize Generic views along with Django Forms, while also using crispy forms
- Make it easy to style Django Templates with tailwindcss being setup initially
- Overall, this boilerplate is about additional productivity and speed for an already productive framework.

Overall, This boilerplate is optimized for a speedy development process based on working with Django over multiple projects in the past. Nothing that is included in this boilerplate is new. This boilerplate is also very opinionated in the way you should be building django applications. Trying to fight these opinions will not give you the best productivity this boilerplate offers.

## Generic Views

Onlydjango include a `helpers/cbv.py` file which has an extension of all the Django Generic views. The reason for extending the generic views with our own generic views are to add `FormHelpers` directly within those classes so that when a Createview is rendered through a generic view the crispy tags are used and django forms are replaced with crispy forms.

We also use `crispy-tailwind` for styling and so inside `helpers/formclass.py` we have all the styling a form might need to implement. We also include a package called `django-flatpickr` which uses `flatpickr` for Time, Datetime, and Date widgets. This package may seem unnessesary at first but, these fields by default are rendered as `text` inputs which is not great so a replacement was added so extra time wont be spent fighting it. Feel free to spend extra time and replace it later on if flatpicker doesnt work out very well.

## Static Files

As S3 is the common standard we have included the setup of `django-storages` within the `base.py` file in our settings. Cloudflare R2 will work with this setup.

## Deploying Django

The easiest way to deploy django projects really fast is railway due to the almost instant `postgresql` databases the service provides. Not to mention the covered $5 and the OSS 25% kickback they provide for developers, railway is very very attractive.

Todo: Add a dockerfile so that deployments can be possible in other platforms as well

## Authentication

The package `django-allauth` is used for all authentication. For a really quick setup telegram is implemented. Using ngork you can have a working dev environment for telegram authentication. It can be argued that google auth being default might be easier, but I disagree, as you can have telegram authentication working with a couple of chats with @botfather and running ngrok.

## Logging 

Logging setup also uses Telegram as this is how I mainly log my projects now. Telegram is where I live all the time so seeing application logs instantly just like that is a really big convenience for me. The setup I have on telegram is seperate log channels per application and a folder called Logs that has all these channels.

## AI for Coding

AI can definitely speed up the already speedy workflow django provides. Such as writing tests, UI components and more. The stack using tailwindcss, alpinejs and htmx also makes it easy for LLMs to generate working code. However from experience we often have to remind it to not use alpinejs too much when dealing with data. Because we want django templating language to deal with the data aspect and alpinejs to provide client side interactivity.

The choice of using aider for coding is to preserve privacy for one thing as cursor requests hit their own servers no matter what. It is also cost effecient, and more importantly developer productivity should not be given up just because another IDE has AI.

TBA

