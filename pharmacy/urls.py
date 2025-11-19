"""
URL configuration for pharmacy app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router
router = DefaultRouter()
router.register(r'medicines', views.MedicineViewSet, basename='medicine')
router.register(r'orders', views.OrderViewSet, basename='order')

# URL patterns
urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Template URLs
    path('', views.home, name='home'),
    
    # Medicine URLs
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/add/', views.medicine_add, name='medicine_add'),
    path('medicines/<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    path('medicines/<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),
    
    # Order URLs
    path('orders/', views.order_list, name='order_list'),
    path('orders/place/', views.order_place, name='order_place'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/update-status/', views.order_update_status, name='order_update_status'),
]

