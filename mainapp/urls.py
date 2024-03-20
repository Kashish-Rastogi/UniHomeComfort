from django.urls import path
from .views import (landingpage, loginpage, community_posts_list, update_community_post,
                    delete_community_post, property_detail, viewbiddedproperties, studentallproperties,
                    bidding, property_listing, register_student_user, ownerviewallproperties,
                    delete_property, property_owner_register, owneraddproperty, create_community_post)

myapp_name = 'mainapp'

urlpatterns = [
# ################# Kashish #################
    path('', landingpage, name='landing-page'),
    path('owner-view-all-properties/', ownerviewallproperties, name='owner-view-all-properties'),
    path('owner-add-property/', owneraddproperty, name='owner-add-property'),
    path('delete/<int:property_id>/', delete_property, name='delete-property'),
# ################# Kashish #################

# ################# Tanvi #################
    path('login/', loginpage, name='login-page'),
# ################# Tanvi #################

# ################# Parth #################
    path('bidding/<int:property_id>', bidding, name='bidding'),
# ################# Parth #################

# ################# Jainam #################
    path('register-student-user/', register_student_user, name='register-student-user'),
    path('register/', property_owner_register, name='register'),
    path('view-bidded-properties/', viewbiddedproperties, name='view-bidded-properties'),
    path('student-all-properties/<int:student_id>/', studentallproperties, name='student-all-properties'),

# ################# Jainam #################

# ################# Hetansh #################
    path('property_listing/', property_listing, name='property_listing'),
    path('community/', community_posts_list, name='community_posts_list'),
    path('community/create/', create_community_post, name='create_community_post'),
    path('community/update/<int:pk>/', update_community_post, name='update_community_post'),
    path('community/delete/<int:pk>/', delete_community_post, name='delete_community_post'),
    path('property_detail/', property_detail, name='property_detail'),
# ################# Hetansh #################
]