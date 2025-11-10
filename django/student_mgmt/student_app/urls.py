# student_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Auth/Session URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Student List (main page)
    path('', views.student_list_view, name='student_list'),
    
    # Student CRUD URLs
    path('add/', views.student_add_view, name='student_add'),
    
    # These paths use URL Parameters (pk)
    path('update/<int:pk>/', views.student_update_view, name='student_update'),
    path('delete/<int:pk>/', views.student_delete_view, name='student_delete'),
]