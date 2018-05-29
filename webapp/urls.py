from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^index$', views.index, name='index'),
        url(r'^help', views.help, name='help'),
        url(r'^poseidon_db/$', views.poseidon_db, name='poseidon_db'),
        url(r'^online_data/$', views.online_data, name='online_data'),
        #user_authentication urls
        #url(r'^register/', views.UserCreateAPIView.as_view(), name='register'),
        #url(r'^login/', views.UserLoginAPIView.as_view(), name='login'),
        #url(r'^logout/', views.logout_user, name='logout'),
]