from . import views
from django.conf.urls import url


urlpatterns = [
        url(r'^home/', views.home, name='home'),
        url(r'^index/', views.index, name='index'),
        url(r'^poseidon_db/$', views.poseidon_db, name='poseidon_db'),
        url(r'^gliders/$', views.gliders, name='gliders'),
        url(r'^weather_forecast/(?P<language>\w+)/', views.weather_forecast, name='weather_forecast'),
        url(r'^platforms_between/$', views.platforms_between, name='platforms_between'),
        url(r'^measurements_between/$', views.measurements_between, name='measurements_between'),
        url(r'^online_data_poseidon/(?P<language>\w+)', views.online_data, name='online_data'),
        url(r'^online_data_table/(?P<language>\w+)', views.online_data, name='online_data_table'),
        url(r'^online_data_map/', views.online_data_map, name='online_data_map'),
        url(r'^logout/', views.logout, name='logout'),
        url(r'^user_profile/', views.user_profile, name='user_profile'),
        url(r'^change_password/', views.change_password, name='change_password'),
        url(r'^access_token/', views.access_token, name='access_token'),
        url(r'^error', views.error, name='error'),
        url(r'^activate/', views.activate_user, name='activate_user'),
        url(r'^delete_user/', views.delete_user, name='delete_user'),
        url(r'^create_netcdf/', views.create_netcdf, name='create_netcdf'),
        #user_authentication urls
        #url(r'^get_session/', views.get_session, name='get_session'),
]