---
inclusion: fileMatch
fileMatchPattern: "**/*.html"
---

# Keeping the UI code as small as possible is very beneficial

- Djangos for loops are great in making conditional UI - so dont use alpinejs for something django templates can perfectly handle (unless their is a client side logic)
- create a custom templatetag instead of writing multiple if conditions perhaps when defining some conditional colors of the UI
- If you have a large section of code you are writing a {% comment %} for, you probably need to make it a seperate component using `django-cotton`

> TLDR: make use of custom templatetags as much as possible with the aim of reducing the loc in UI
