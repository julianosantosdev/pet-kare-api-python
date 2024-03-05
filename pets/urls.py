from django.urls import path
from .views import PetViews, PetByIdView

urlpatterns = [
    path("pets/", PetViews.as_view()),
    path("pets/<int:pet_id>/", PetByIdView.as_view())
]
