from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.home, name='home'),
    path('drugs/', views.drug_list, name='drug_list'),
    path('drugs/add/', views.create_drug, name='create_drug'),
    path('drugs/<int:drug_id>/update/', views.update_drug, name='update_drug'),
    path('drugs/<int:drug_id>/delete/', views.delete_drug, name='delete_drug'),
    path('drugs/export/csv/', views.export_inventory_csv, name='export_drugs_csv'),
]
