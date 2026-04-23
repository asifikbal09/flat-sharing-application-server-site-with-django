from django.urls import path
from .views import BookingCreateView, BookingListView, BookingUpdateView

urlpatterns = [
    path('booking-applications', BookingCreateView.as_view(), name='booking-create'),
    path('booking-requests', BookingListView.as_view(), name='booking-list'),
    path('booking-requests/<str:booking_id>', BookingUpdateView.as_view(), name='booking-update'),
]