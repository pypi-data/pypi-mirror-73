from django.urls import path

from . import views


# Define a list of URL patterns to be imported by NetBox. Each pattern maps a URL to
# a specific view so that it can be accessed by users.
urlpatterns = (
    path('', views.DeviceUpload.as_view(), name='file_upload'),
    path('devices/', views.DeviceListView.as_view(), name='device_view2'),
)

