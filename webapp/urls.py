from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^home/', views.home, name='home'),
        url(r'^index/', views.index, name='index'),
        url(r'^poseidon_db/$', views.poseidon_db, name='poseidon_db'),
        url(r'^online_data/$', views.online_data, name='online_data'),
        url(r'^logout/', views.logout, name='logout'),
        url(r'^access_token/', views.access_token, name='access_token'),
        url(r'^error', views.error, name='error'),
        #user_authentication urls
        url(r'^get_session/', views.get_session, name='get_session'),
]