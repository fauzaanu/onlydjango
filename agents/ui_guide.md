Tailwindcss is always running in the background and so is the server. we are using django cotton for UI.

Here is an overview of django-cotton:

Components
Components are reusable pieces of view template. They can contain native Django template syntax and can be used inside
standard Django templates.

1. The basic building block: {{ slot }}
   The {{ slot }} variable captures all content passed between a component's opening and closing tags.

cotton/box.html
<div class="box">
    {{ slot }}
</div>
Used in a parent template:

my_view.html
<c-box>
<p>Some <strong>content</strong></p>
</c-box>
preview
Some content

2. Adding Component Attributes
   We can further customize components with attribute, which allow you to pass specific data into the component as
   key-value pairs.

cotton/weather.html
<p>It's {{ temperature }}<sup>o</sup>{{ unit }} and the condition is {{ condition }}.</p>

<c-weather temperature="23" unit="{{ unit }}" condition="windy"></c-weather>
preview
It's 23oC and the condition is windy.

3. Using Named Slots
   If we want to pass HTML instead of just a string (or another data type) into a component, we can pass them as named
   slots with the <c-slot name="...">...</c-slot> syntax.

   **Important**: Always use <c-slot name="...">...</c-slot> for passing HTML content to components. Do not use <div slot="...">, 
   as this is not the correct syntax and may not work as expected.

So as with normal attributes, you reference the slot content like normal variables, as in:

cotton/weather_card.html
<div class="flex ...">
    <h2>{{ day }}:</h2> {{ icon }} {{ label }}
</div>
view.html
<c-weather-card day="Tuesday">
    <c-slot name="icon">
        <img src="sunny-icon.png" alt="Sunny">
    </c-slot>

    <c-slot name="label">
        <div class="yellow">Sunny</div>
    </c-slot>

</c-weather-card>
preview
Tuesday:
Sunny
Component filenames should be snake_cased by default. To use kebab-cased / hyphenated filenames instead, set COTTON_SNAKE_CASED_NAMES to False in your settings.py, more.
4. Dynamic Attributes with ":"
We saw how by default, all attributes that we pass to a component are treated as strings. If we want to pass HTML, we can use named slots. But what if we want to pass another data type like a template variable, boolean, integer, float, dictionary, list, dictionary?

Passing objects from context
Sometimes you'll want to pass a variable from the parent's context 'as is' for the child component to perform what it
wants.

view.html
<!--
context = { 'today': Weather.objects.get(...) }
-->
<c-weather :today="today"></c-weather>
cotton/weather.html
<p>It's {{ today.temperature }}<sup>o</sup>{{ today.unit }} and the condition is {{ today.condition }}.</p>
Passing python types
Integers & Floats
<c-mycomp :prop="1" />
<!-- {% prop == 1 %} -->
None
<c-mycomp :prop="None" />
<!-- {% prop is None %} -->
Lists
<c-mycomp :items="['item1','item2','item3']" />
<!-- {% for item in items %} -->
Dicts
<c-mycomp :mydict="{'name': 'Thom', 'products': [1,2]}" />
<!-- {{ mydict.name }}, {{ mydict.products }} -->
Parent variable
<c-mycomp :product="product" />
<!-- {{ product.title }} -->
With template expressions
<c-mycomp :slides="['{{ image1 }}', '{{ image2 }}']" />
<!-- {% for images in slides %} -->
Generated with template expressions
<c-mycomp :is_highlighted="{% if important %}True{% endif %}" />
<!-- {% is_valid is False %} -->
Note: You can use the same dynamic attribute patterns in c-vars to apply dynamic defaults to your components.
A quick example of this is a select component that you want to fill with options:

view.html
<c-select :options="['no', 'yes', 'maybe']" />
preview
Are carrots tasty?

no
cotton/select.html
<select>
{% for option in options %}
<option value="{{ option }}">{{ option }}</option>
{% endfor %}
</select>

5. Pass all attributes with {{ attrs }}
   Sometimes it's useful to be able to reflect all attributes provided in the parent on to an HTML element in the
   component. This is particularly powerful when you are building form inputs.

form_view.html
<c-input name="first_name" placeholder="First name" />
<c-input name="last_name" placeholder="Last name" value="Smith" readonly />
preview
First name
Smith
cotton/input.html
<input type="text" {{ attrs }} />

<!-- html output
<input type="text" name="first_name" placeholder="First name" />
<input type="text" name="last_name" placeholder="Last name" value="Smith" readonly />
-->
5.1 Merging Attributes with :attrs
In addition to using {{ attrs }} to output attributes, you can also pass in a dictionary of attributes using the
special :attrs dynamic attribute. This is useful when you have a collection of attributes from your view or another
component that you want to apply.

cotton/input.html
<input type="text" {{ attrs }} />
form_view.html
<!-- In your view -->
context = {
'widget_attrs': {
'placeholder': 'Enter your name',
'data-validate': 'true',
'size': '40'
}
}

<!-- In your template -->
<c-input :attrs="widget_attrs" required />

<!-- html output
<input type="text" placeholder="Enter your name" data-validate="true" size="40" required />
-->
You can also proxy the whole attrs dictionary to other components. <c-comp :attrs="attrs" /> This is useful when you
want to pass all attributes from one component to another without having to specify each one individually. More info.

6. Defining Local Variables with <c-vars />
   The <c-vars /> tag simplifies component design by allowing local variable definition, reducing the need for
   repetitive attribute declarations and maintaining backend state.

Place a single <c-vars /> at the top of a component to set key-value pairs that provide a default configuration.

Example: Setting Default Attributes
In components with common defaults, <c-vars /> can pre-define attributes that rarely need overriding.

cotton/alert.html
<c-vars type="success" />

<div class="{% if type == 'success' %} .. {% elif type == 'danger' %} .. {% endif %}">
    {{ slot }}
</div>
form_view.html
<c-alert>All good!</c-alert>
<c-alert type="danger">Oh no!</c-alert>
preview
All good!
Oh no!
<c-vars /> are excluded from {{ attrs }}
Keys in <c-vars /> are omitted from {{ attrs }}, making them ideal for configuration attributes that shouldn't appear in HTML attributes.

cotton/input_group.html
<c-vars label errors />

<label>{{ label }}</label>

<input type="text" class="border ..." {{ attrs }} />

{% if errors %}
{% for error in errors %}
{{ error }}
{% endfor %}
{% endif %}
form_view.html
<c-input-group label="First name" placeholder="First name" :errors="errors.first_name" />
<c-input-group label="Last name" placeholder="Last name" :errors="errors.last_name" />
preview
First name
First name
Last name
Last name

Last name is required
By specifying label and errors keys in <c-vars />, these attributes won’t be included in {{ attrs }}, allowing you to
control attributes that are designed for component configuration and those intended as attributes.

7. Boolean attributes
   Sometimes you just want to pass a simple boolean to a component. Cotton supports providing the attribute name without
   a value which will provide a boolean True to the component.

cotton/input.html
<input type="text" {{ attrs }} />

{% if required is True %}
<span class="text-red-500">*</span>
{% endif %}
form_view.html
<c-input name="telephone" required />
preview
Telephone

*

8. Dynamic Components
   There can be times where components need to be included dynamically. For these cases we can reach for a special <
   c-component> tag with an is attribute:

cotton/icon_list.html
{% for icon in icons %}
<c-component is="icons.{{ icon }}" />
{% endfor %}
The is attribute is similar to other attributes so we have a number of possibilities to define it:

cotton/icon_list.html
<!-- as variable -->
<c-component :is="icon_name" />

<!-- as an expression -->
<c-component is="icon_{{ icon_name }}" />
9. Context Isolation
You can pass the only attribute to the component, which will prevent it from adopting any context other than its direct attributes.

10. Alpine.js support
    The following key features allow you to build re-usable components with alpine.js:

x-data is accessible as {{ x_data }} inside the component as cotton makes available snake_case versions of all
kebab-cased attributes. (If you use {{ attrs }} then the output will already be in the correct case).
Shorthand x-bind support (:example). Because single : attribute prefixing is reserved for cotton's dynamic attributes,
we can escape the first colon using ::. This will ensure the attribute maintains a single : inside {{ attrs }}
Summary of Concepts
{{ slot }} - Default content injection.
Attributes - Simple, straightforward customization.
Named Slots - Provide HTML or template partial as a variable in the component.
: Dynamic Attributes - Pass variables and other data types other than strings.
{{ attrs }} - Prints attributes as HTML attributes.
<c-vars /> - Set default values and other component state.
Boolean attributes - Attributes without values are passed down as True
Dynamic Components - Insert a component where the name is generated by a variable or template expression: <c-component :
is="my_variable" />

--
You can create new components and reference them and move to a components based design. We also have htmx and alpinejs
and fontawesome within the layout component so u can use those libraries. We have fontawesome pro so utilize it to the
best of usecases.
---
