from django.urls import path

from . import views


urlpatterns = [
    path('<int:meter_id>/', views.view_graph, name='meter_graph'),
]
