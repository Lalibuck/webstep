from django.urls import path
from qa import views
from django.contrib import admin

urlpatterns = [
    path('/admin', admin.site.urls),
    path('', views.main),
    path('login/', views.test),
    path('signup/', views.test),
    path('question/<int:id>/', views.question),
    path('ask/', views.test),
    path('popular/', views.popular),
    path('new/', views.test),
]
