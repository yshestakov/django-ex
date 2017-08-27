from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from welcome.views import index, health
from blog.views import post_list

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),

    url(r'^blog/', include('blog.urls')),
    # url(r'^$', index),
    url(r'^$', post_list),
    url(r'^welcome$', index, name='welcome'),
    url(r'^health$', health, name='health'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout',
        kwargs={'next_page': '/'}),
]
