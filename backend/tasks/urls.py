from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, ContactViewSet, DealViewSet, TaskViewSet, CampaignView,CampaignByIdView,
    login_view, logout_view, dashboard_stats, register_view
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'deals', DealViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('', include(router.urls)),

    path('campaigns/', CampaignView.as_view(), name='campaigns'),
    path('campaigns/<int:pk>/', CampaignByIdView.as_view(), name='campaign_by_id'),
]
