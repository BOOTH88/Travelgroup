from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/(?P<foodie_id>[\w]{1,11})$',views.food)
]