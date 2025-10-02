---
inclusion: fileMatch
fileMatchPattern: "*.html"
---

# Keeping the UI code as small as possible is very beneficial

Djangos for loops are great in making conditional UI. For example based on the text we decide a different color. Instead of creating different components we can actually create templatetags folder and create custom filters which would minimize the frontend code by a lot.

> TLDR: make use of custom templatetags as much as possible with the aim of reducing the loc in UI