from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve
admin.autodiscover()

from faceguessing.views import index, updatestats, jsonform, get_user_image, updatesites
from stats.views import hall_of_fame
from nameguessing.views import nameguessing, get_thumbnail, check_hash, json_thumbnails

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^updatestats/', updatestats, name="updatestats"),
    url(r'^jsonform/', jsonform, name="jsonform"),
    url(r'^image/current/thumb/', get_thumbnail, name="image_current"),
    url(r'^image/current/', get_user_image, name="image_current_user"),
    url(r'^hall_of_fame$', hall_of_fame, name="hall_of_fame"),
    url(r'^name/updatestats', check_hash, name="name_updatestats"),
    url(r'^name/', nameguessing, name="nameguessing"),
    url(r'^json_thumbnails/', json_thumbnails, name="json_thumbnails"),
    url(r'^updatesites/', updatesites, name="updatesites"),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
