from rest_framework import generics
from .models import Listing
from .serializers import ListingSerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to ALX Travel App!")

class ListingListCreate(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    from django.http import HttpResponse

