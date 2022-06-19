from django.urls import path
from qa import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main),
    path('login/', views.log_in),
    path('signup/', views.signup),
    path('question/<int:id>/', views.question, name='question'),
    path('ask/', views.question_add),
    path('popular/', views.popular),
    path('new/', views.test),
]

