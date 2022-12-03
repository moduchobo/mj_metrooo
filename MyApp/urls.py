
'''
from django.contrib import admin
from django.urls import path
from product.views import ProductListAPI

urlpatterns = [
    path('admin/', admin.site.urls),
		path('api/product/', ProductListAPI.as_view())
]

'''
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('api/User/', UserDataAPI.as_view()),
    path('api/User/<int:userid>/', SingleUserDataAPI().as_view()),
    path('api/Schedule/', ScheduleDataAPI.as_view()),
    path('api/Station/', StationDataAPI.as_view()),
    path('api/Schedule/<int:userid>/', UserScheduleAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)