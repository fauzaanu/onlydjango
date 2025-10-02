---
inclusion: fileMatch
fileMatchPattern: "*.html"
---

# Django cotton docs summary

Before anything here are the most important facts you should remmember about django cotton

The templates have `<c-file-name />` but the file is named `cotton/file_name.html`. This is something we often forget.

We have some tags we shouldnt use. mentioned in another guideline file.

We have a mechanism to pass dynamic data into components that prefixes ":" before a variable name
--

For each application we have a seperate cotton folder within the templates. We can make variations of components by converting the file name to a folder and including an index.html where the default component lives which is automatically picked up without the mention of index but we can then add print.html as another component inside the folder to be shown on a perhaps print only page

So:
<c-file-name /> on regular pages and <c-file-name.print /> for the print page

the dirs look like:
apps/cotton/report/file_name/index.html
apps/cotton/report/file_name/print.html

---
Here is the full summarized docs for you to refer about django cotton

### Components

* **`{{ slot }}`**
  Default content:

  ```html
  <!-- cotton/box.html -->
  <div class="box">{{ slot }}</div>
  <!-- usage -->
  <c-box>…</c-box>
  ```

* **Attributes**
  Pass strings or variables:

  ```html
  <c-weather temperature="23" unit="{{ unit }}" condition="windy"/>
  ```

* **Named Slots**
  For HTML payloads:

  ```html
  <c-weather-card day="Tue">
    <c-slot name="icon">…</c-slot>
    <c-slot name="label">…</c-slot>
  </c-weather-card>
  ```

* **Dynamic (`:`) Attributes**
  Inject context values or types:

  ```html
  <c-weather :today="today_obj"/>
  <c-mycomp :items="['a','b']" :count="1" :flag="None"/>
  ```

* **`{{ attrs }}` & `:attrs`**
  Reflect all HTML attributes or merge a dict:

  ```html
  <!-- component -->
  <input {{ attrs }}/>
  <!-- usage -->
  <c-input name="x" placeholder="…" readonly/>
  <c-input :attrs="widget_attrs" required/>
  ```

* **`<c-vars />`**
  Define defaults (excluded from `attrs`):

  ```html
  <c-vars type="success"/>
  <div class="{% if type=='success'%}…">{ slot }</div>
  ```

* **Boolean Attributes**
  Presence = `True`:

  ```html
  <c-input name="tel" required/>
  ```

* **Dynamic Components**
  Render by name:

  ```html
  <c-component is="icons.{{ icon_name }}"/>
  <c-component :is="comp_var"/>
  ```

* **Context Isolation**
  `only` attribute limits context to passed props.

* **Alpine.js**

  * Access `x-data` via `{{ x_data }}`
  * Use `::` to preserve `:` in `{{ attrs }}` (e.g. `::x-bind`)

---

### Template Layout

```
templates/
│
├─ cotton/<app>/       ← reusable components
│   └─ component.html
│
└─ <app>/             ← full-page templates
    └─ page.html
```

* **Naming**: `<c-app.component>` (dot notation).
* **Pages** import from `templates/cotton`; components don’t import pages.
