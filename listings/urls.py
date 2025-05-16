from django.urls import path
from .views import ListingListCreate
from listings.views import home  # Import your view
from django.contrib import admin

urlpatterns = [
    path('listings/', ListingListCreate.as_view(), name='listing-list'),
    path('', home, name='home'),  # Add this line for root URL
    path('admin/', admin.site.urls),
]

