from django.urls import path
from . import views

app_name = 'studentpanel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.my_projects, name='my_projects'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('projects/delete/<int:pk>/', views.delete_project, name='delete_project'),
    path('search/', views.search_research, name='search_research'),
    path('request-collab/<int:researcher_id>/', views.request_collaboration, name='request_collaboration'),
    path('saved/', views.saved_research, name='saved_research'),
    path('messages/', views.messages_view, name='messages'),
    path('notifications/', views.notifications, name='notifications'),
    path('collaborations/', views.my_collaborations, name='my_collaborations'),
    path('researchers/', views.browse_researchers, name='browse_researchers'),
    path('request-collab/<int:researcher_id>/', views.request_collaboration, name='request_collaboration'),
    path('collaborations/', views.my_collaborations, name='my_collaborations'),
]
