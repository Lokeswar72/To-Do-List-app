from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('bulk-action/', views.bulk_action, name='bulk_action'),  # 👈 Add this
    path('reorder/', views.reorder_tasks, name='reorder_tasks'),

]
