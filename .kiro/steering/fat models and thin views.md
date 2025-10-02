
---
inclusion: fileMatch
fileMatchPattern: "*.py"
---

# Fat Models and Thin Views

Views must be as minimal as possible. It is ok to include the context dictionary within a view even though it should be minimal. However, if a context dictionary is extremely long (over 50 loc) we should move it to a services file. and call it as a method.

Most views that get too long are long because of database calls and processing logic. Databases are represented in `models.py` and therefore we will create class methods inside models.py to get the data for the view

Here is an example:

```python
# Create your views here.
class DiveSiteIndexView(View):

    def get(self, request):
        dive_sites = DiveSite.objects.all()
        settings = DiveSiteSetting.get_for_view()
        context = {
            'dive_sites': dive_sites,
            "cover_image": settings.cover,
            "cover_text": settings.title,
            "cover_subtext": settings.subtitle,
        }
        return render(request, "divesites/index.html", context)
```

Instead of keeping the settings data in individual lines in the view we are moving it completely to the respected model of the models.py as a class method. This is not a model method but a classmethod inside the model. so it doesnt represent a single object or instance of the model but by keeping this logic in models.py we can have a really small views.py file.

>TLDR: Fat models, thin views