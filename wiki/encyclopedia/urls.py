from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:TITLE>" , views.get_entry , name="get_entry"),
    path("search_entry/", views.search_entry, name="search_entry"),
    path("new_entry/" , views.new_entry , name="new_entry"),
    path("edit_entry/<str:TITLE>", views.edit_entry, name="edit_entry"),
    path("random/" , views.random_page , name="random_page")
]
