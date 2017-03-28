# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.conf import settings
# from feedback.forms import FeedbackForm

from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from error_manag.models import ErrorMessage
from flatpages.views import flatpage, advantage
from quick_links.views import link_detail

#В сеттингс APPEND_SLASH = False
class SimpleSystemMiddleware(object):
    # вместо аппенд splash
    def process_request(self, request):
        if request.method == 'GET':
            url = request.path
            if url:
                if not url.endswith('/'):
                    if '.' not in url:
                        return redirect(request.path_info+'/')



class FlatpageFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.

        try:
            return link_detail(request, request.path_info)
        except Http404:
            pass

        try:
            return advantage(request, request.path_info)
        except Http404:
            pass
        try:
            return flatpage(request, request.path_info)
        except Http404:
            pass
        if settings.DEBUG:
            raise

        if response.status_code == 404:
            try:
                content = u'%s' % ErrorMessage.objects.get(type='404').message
            except:
                content = u'404'

            return HttpResponseNotFound(render_to_string(
                'flatpages/default_for_404.html',
                {'breadcrumbs': [{"title": "404"}],
                 'flatpage': {'content': content,}
                },
                context_instance=RequestContext(request)))
        return response

