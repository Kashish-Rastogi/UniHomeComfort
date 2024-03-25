from django.urls import path
from .import views

from .views import (landingpage, loginpage, community_posts_list, update_community_post,
                    delete_community_post, property_detail, viewbiddedproperties, studentallproperties,
                    bidding, property_listing, register_student_user, owner_view_all_properties,
                    owner_delete_property, property_owner_register, owner_add_property, create_community_post, aboutus,
                    owner_settings, user_property_visits,
                    owner_property_bids, owner_edit_property, student_settings, view_my_posts, view_chat, send_message,
                    notification_list, send_payment_request, do_payment, success_page)

myapp_name = 'mainapp'

urlpatterns = [
# ################# Kashish #################
    path('', landingpage, name='landing-page'),
    path('owner-view-all-properties/', owner_view_all_properties, name='owner-view-all-properties'),
    path('owner-add-property/', owner_add_property, name='owner-add-property'),
    path('delete/<int:property_id>/', owner_delete_property, name='owner-delete-property'),
    path('edit/<int:property_id>/', owner_edit_property, name='owner-edit-property'),
    path('owner-property-bids/', owner_property_bids, name='owner-property-bids'),
    path('user-property-visits/', user_property_visits, name='user-property-visits'),
# ################# Kashish #################

# ################# Tanvi #################
    path('login/', loginpage, name='login-page'),
    path('settings/', student_settings, name='student_settings'),
    path('register/', property_owner_register, name='register'),
    path('property_listing/', property_listing, name='property_listing'),
# ################# Tanvi #################

# ################# Parth #################
    path('bidding/<int:property_id>', bidding, name='bidding'),
    path('owner-settings/', owner_settings, name='owner_settings'),
    path('aboutus/', aboutus, name='aboutus'),
# ################# Parth #################

# ################# Jainam #################
    path('register-student-user/', register_student_user, name='register-student-user'),
    path('view-bidded-properties/', viewbiddedproperties, name='view-bidded-properties'),
    path('student-all-properties/<int:student_id>/', studentallproperties, name='student-all-properties'),
    path('chat/<int:post_id>', view_chat, name='view_chat'),
    path('send-message/', send_message, name='send_message'),
    path('success/', success_page, name='success'),
# ################# Jainam #################

# ################# Hetansh #################
    path('community/', community_posts_list, name='community_posts_list'),
    path('my-posts/', view_my_posts, name='view_my_posts'),
    path('community/create/', create_community_post, name='create_community_post'),
    path('community/update/<int:pk>/', update_community_post, name='update_community_post'),
    path('community/delete/<int:pk>/', delete_community_post, name='delete_community_post'),
    path('property_detail/<int:property_id>/', property_detail, name='property_detail'),
    path('notifications/', notification_list, name='notification-list'),
    path('send-payment-request/', send_payment_request, name='send_payment_request'),
    path('do-payment/<int:payment_id>/', do_payment, name='do_payment'),
    path('send-payment-request/<int:property_id>/', views.send_payment_request, name='send_payment_request'),
# ################# Hetansh #################




###################### Haseeb ##################
    path('forget/', views.forget_password, name='forget'),

###################### Haseeb ##################
]


