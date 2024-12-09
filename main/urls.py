from django.urls import path
from .views import *

urlpatterns = [
    path('projects/', ProjectView.as_view(), name='project-list'),
    path('projects/<str:pk>/', ProjectDetailView.as_view(), name='project-detail'),

    path('tags/', TagView.as_view(), name='tag-list'),
    path('tags/<str:pk>/', TagDetailView.as_view(), name='tag-detail'),

    path('bids/', BidListView.as_view(), name='bid-list'),
    path('projects/<uuid:pk>/bids/', ProjectBidsView.as_view(), name='project-bids'),
    path('projects/<uuid:pk>/add-member/', AddTeamMemberView.as_view(), name='add-member'),

    path('reviews/<str:pk>/', ReviewListView.as_view(), name="reviews"),
]
