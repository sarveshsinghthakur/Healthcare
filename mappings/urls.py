from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapping_list_create, name='mapping-list-create'),
    path('<int:patient_id>/', views.mapping_by_patient, name='mapping-by-patient'),
    path('delete/<int:pk>/', views.mapping_delete, name='mapping-delete'),
]
