from django.urls import path
from qa import views
from django.contrib import admin

urlpatterns = [
    path('/admin', admin.site.urls),
    path('', views.test),
    path('login/', views.test),
    path('signup/', views.test),
    path('question/<int:id>/', views.test),
    path('ask/', views.test),
    path('popular/', views.test),
    path('new/', views.test),
]
