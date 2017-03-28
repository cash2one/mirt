# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/',include('personal.urls', namespace='personal')),
    url(r'^order/', include('order.urls',  namespace='order')),
    url(r'^dismiss_under_development_banner/$',
        'main.views.disable_under_development_banner',
        name="dismiss-under-development-banner"),
    url(r'^', include('feedback.urls')),
    url(r'^', include('announce.urls',  namespace='announce')),
    url(r'^', include('news.urls',  namespace='news')),
    url(r'^', include('services.urls',  namespace='services')),
)

if 'tinymce' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^tinymce/', include('tinymce.urls')),
    )

if 'filebrowser' in settings.INSTALLED_APPS:
    from filebrowser.sites import site
    urlpatterns += patterns('',
        url(r'^admin/filebrowser/', include(site.urls)),
    )

if 'grappelli' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^grappelli/', include('grappelli.urls')),
    )


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )

urlpatterns += patterns('main.views',
    url(r'^change_theme/$', 'change_theme', name='change-theme'),
    url(r'^sitemap.xml$', 'sitemap_gen',),
)

urlpatterns += patterns('',
        url(r'^', include('catalog.urls',  namespace='catalog')),
        url(r'^', include('flatpages.urls', namespace='fpc')),
)

urlpatterns += patterns('quick_links.views',
    url(r'^(?P<slug>.*)$', 'link_detail', name='quick_link'),
)
