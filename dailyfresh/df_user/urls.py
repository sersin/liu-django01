from django.conf.urls import url
from . import views

urlpatterns = [
    url('^register/$',views.register),
    url('^register_handle/$',views.register_handle),
    url('^register_exist/$',views.register_exist),
    url('^login/$',views.login),
    url('^logout/$', views.logout),
    url('^login_handle/$',views.login_handle),
    url('^user_center_info/$',views.user_center_info),
    url('^user_center_order(\d*)/$',views.user_center_order),
    url('^user_center_site/$',views.user_center_site),
]