---
inclusion: fileMatch
fileMatchPattern: "**/views.py"
---

# No Generic Views


All Views must be class based views that dont use generic views. This means every single view written must be in the following way

```python
class SomeRandom(View):
    def get(self, request):
        ...

    def post(self,request):
        ...
```

Optionally we can also define a Base View with all the common mixins of multiple Views and create a Base View. However this baseview is also required to inherit from View and not from any generic views.

> TLDR: Never use Generic views and inherit from `View`

