---
inclusion: fileMatch
fileMatchPattern: "{**/forms.py,**/*.html}"
---

# Django forms are great, mostly but . . .

Django forms are great but not so great when we use tailwindcss to design the form in a very custom way. so to allow full freedom in designing the form in whatever way we as the developer see fit we will not be using django forms on the templates. This only means we will not be passing the form on a get request to the template. we will however use djangoforms to the full extent on the post request. For example:

```python
class AddSunglass(View):
    def get(self, request):
        # Render the template, optionally passing context if needed
        return render(request, "sunglass/add.html", {})

    def post(self, request):
        form = AddSunglassForm(request.POST)
        if form.is_valid():
            try:
                form.save()  # Save the form data
                return redirect('sunglass:dashboard')
            except Exception as e:
                # Handle potential errors (e.g., database issues)
                return render(request, "sunglass/add.html", {
                    'errors': [f"An error occurred: {str(e)}"],
                })
        else:
            # If form is invalid, re-render the template with errors
            return render(request, "sunglass/add.html", {
                'errors': form.errors,
            })
```

It is important to remmember that we have to use csrf token tag in the custom template we write from scratch. we must also use the exact names that the django form would expect. We must also not use widgets in forms.py as we wont be needing them.

>TLDR: Use django forms but dont pass to the template