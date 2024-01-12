from django.urls import path, include
from . import views 
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('leads', views.LeadView)

urlpatterns = [
    path('', include(router.urls))
]
