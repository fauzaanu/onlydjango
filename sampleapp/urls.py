# flake8: noqa: E501
from django.urls import path, include

from sampleapp import views

"""
In urls the new line rules of flake8 and black are not great to view. This is obviousely an opinion I have
"""

# fmt: off
urlpatterns = [
    # Public views
    path("", views.dashboard_view, name="dashboard"),


    # Admin views

]
# fmt: on
