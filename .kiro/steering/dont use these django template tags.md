
# Dont use these template tags

django-cotton allows us to develop UI in a different component based way and therefore the use of the following tags will actually get in the way of our development flow.

- {% with %}
- {% block %}
- {% extends %}

Instead of with we can pass variables directly to the components. To pass something dynamic it should have the following syntax of :variable="model.call_model_method"

<cotton_documentation_snippet>
Dynamic Attributes with ":"
We saw how by default, all attributes that we pass to a component are treated as strings. If we want to pass HTML, we can use named slots. But what if we want to pass another data type like a template variable, boolean, integer, float, dictionary, list, dictionary?

Passing objects from context
Sometimes you'll want to pass a variable from the parent's context 'as is' for the child component to perform what it wants.

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


</cotton_documentation_snippet>

> TLDR: Dont use with, extends and block django tags