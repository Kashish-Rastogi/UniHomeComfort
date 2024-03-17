from django.urls import path
from .views import landingpage, loginpage, ownerdashboard, community_posts_list, update_community_post, delete_community_post, property_detail, viewbiddedproperties, studentallproperties,bidding
from . import views

myapp_name = 'mainapp'

urlpatterns = [
    path('', landingpage, name='landing-page'),
    path('login/', loginpage, name='login-page'),
    path('owner-dashboard/', ownerdashboard, name='owner-dashboard'),
    path('bidding/', bidding, name='bidding'),
    path('view-bidded-properties/', viewbiddedproperties, name='view-bidded-properties'),
    path('student-all-properties/<int:student_id>/', studentallproperties, name='student-all-properties'),
    path('community/', views.community_posts_list, name='community_posts_list'),
    path('community/create/', views.create_community_post, name='create_community_post'),
    path('community/update/<int:pk>/', views.update_community_post, name='update_community_post'),
    path('community/delete/<int:pk>/', views.delete_community_post, name='delete_community_post'),
    path('properties/<int:property_id>/', property_detail, name='property_detail'),
]