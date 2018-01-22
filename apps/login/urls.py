from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="landing"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^register$', views.register, name="register"),
    url(r'^home$', views.home, name="home"),
    url(r'^add_friends/(?P<id>\d+)$', views.add, name="add_friends"),
    url(r'^remove_friends/(?P<id>\d+)$', views.remove, name="remove_friends"),
    url(r'^user_profile/(?P<id>\d+)$', views.user, name="user_profile"),



]
