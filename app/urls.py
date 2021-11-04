from django.conf.urls import url
from .import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
urlpatterns=[

 url(r'^api/plants/$', views.PlantList.as_view(),name = "apiplants" ),
 path("api/<int:temp>/<int:alt>/", views.PlantRecc.as_view(),name = "apisearch")   
]
 