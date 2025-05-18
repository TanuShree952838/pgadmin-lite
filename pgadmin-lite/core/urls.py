from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('run-query/', views.run_query_view, name='run_query'),
    path('query/', views.query_view, name='query'),
    path('table/<str:table_name>/', views.table_crud, name='table_crud'),
    path('update/<str:table_name>/<int:id>/', views.update_record, name='update_record'),
    path('delete/<str:table_name>/<int:id>/', views.delete_record, name='delete_record'),

]
