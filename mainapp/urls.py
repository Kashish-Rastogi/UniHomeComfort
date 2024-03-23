from django.urls import path
from .views import landingpage, loginpage, ownerdashboard, community_posts_list, update_community_post, delete_community_post, property_detail, viewbiddedproperties, studentallproperties, add_property,bidding, property_listing
from . import views

myapp_name = 'mainapp'

urlpatterns = [
    path('', landingpage, name='landing-page'),
    path('add-property/', add_property, name='add-property'),
    path('login/', loginpage, name='login-page'),
    path('register-student-user/', views.register_student_user, name='register-student-user'),
    path('register/', views.property_owner_register, name='register'),
    path('properties/', property_listing, name='property_listing'),
    path('owner-dashboard/', ownerdashboard, name='owner-dashboard'),
    path('bidding/<int:property_id>', bidding, name='bidding'),
    path('view-bidded-properties/', viewbiddedproperties, name='view-bidded-properties'),
    path('student-all-properties/<int:student_id>/', studentallproperties, name='student-all-properties'),
    path('community/', views.community_posts_list, name='community_posts_list'),
    path('community/create/', views.create_community_post, name='create_community_post'),
    path('community/update/<int:pk>/', views.update_community_post, name='update_community_post'),
    path('community/delete/<int:pk>/', views.delete_community_post, name='delete_community_post'),
    path('properties/<int:property_id>/', property_detail, name='property_detail'),
    path('forget/', views.forget_password, name='forget'),

]