from django.urls import path
from . import views

app_name = 'researchpanel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('my-research/', views.my_research, name='my_research'),
    path('create/', views.create_research, name='create_research'),
    path('edit/<int:pk>/', views.edit_research, name='edit_research'),
    path('delete/<int:pk>/', views.delete_research, name='delete_research'),
    path('post/<int:pk>/', views.research_detail, name='research_detail'),
    path('collaborations/', views.collaborations, name='collaborations'),
    path('collaborations/<int:pk>/<str:action>/', views.update_collab, name='update_collab'),
    path('request-collab/<int:pk>/', views.request_collaboration, name='request_collaboration'),
    path('messages/', views.messages_view, name='messages'),
    path('notifications/', views.notifications, name='notifications'),
    path('search/', views.search_researchers, name='search_research'),
]
