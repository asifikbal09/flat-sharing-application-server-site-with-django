from django.urls import path
from .views import FlatListCreateView, FlatUpdateView

urlpatterns = [
    path('flats', FlatListCreateView.as_view(), name='flats'),
    path('flats/<str:flat_id>', FlatUpdateView.as_view(), name='flat-update'),
]