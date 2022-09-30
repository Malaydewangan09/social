from django.urls import path
from .views import GetUpdateUserProfileView

urlpatterns = [
    path(
        '', GetUpdateUserProfileView.as_view(), name='get_update_user_profile'
    ),
]