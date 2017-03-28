# -*- coding: utf-8 -*-
from flatpages.models import FlatPage
from django.shortcuts import render

from forms import FeedbakForm
from message.models import Mail, Message
from models import Feedback
from constance import config
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.models import Site
import json


def render_contacts(request):
    try:
        flatpage = FlatPage.objects.filter(type="contacts")[0]
        breadcrumbs = flatpage.get_breadcrumbs()
    except:
        pass

    context = feedback(request)
    if context:
        if request.is_ajax():
            return HttpResponse(json.dumps(context), mimetype="application/json")
        if context.get('success'):
            return HttpResponseRedirect(request.path+"?thanks_for_feedback=show")
    return render(request, 'flatpages/contacts.html', locals())


def feedback(request):
    if request.POST:

        post = request.POST
        context = ({})
        success = False

        if post.get('name') == 'imbot':
            form = FeedbakForm(request.POST)
            if form.is_valid():
                if 'eman' in form.cleaned_data:
                    context.update({"name":form.cleaned_data['eman']})
                if 'email' in form.cleaned_data:
                    context.update({"email":form.cleaned_data['email']})
                if 'message' in form.cleaned_data:
                    context.update({"message":form.cleaned_data['message']})

                mail_to = config.MANAGER_EMAIL.replace(' ', '').split(',')
                email_from = config.EMAIL_FROM.replace(' ', '').split(',')[0]
                domain = Site.objects.get_current().domain
                context.update({"SITE": domain})
                mail_to_client = []
                mail_to_client.append(context.get("email"))
                mail_subject = Mail.objects.filter(type="contacts_email")[0].subject
                mail_template = Mail.objects.filter(type="contacts_email")[0].mail
                mail_message = Template(mail_template).render(Context(context))
                mail = EmailMessage(mail_subject, mail_message, email_from, mail_to)
                mail.content_subtype='html'
                mail.send()
                mail_client = EmailMessage(mail_subject, mail_message, email_from, mail_to_client)
                mail_client.content_subtype = 'html'
                mail_client.send()

                feedback = Feedback()
                feedback.name = context.get("name")
                feedback.email = context.get("email")
                feedback.message = context.get("message")
                feedback.save()

                success = True
                respond = {"success": success,
                           "form_errors": '',
                           }
            else:
                respond = {"success": success,
                           "message": None,
                           "form_errors": form.errors,
                           }
            if request.is_ajax():
                mess = "<p>спасибо</p>"
                try:
                    mess = Message.objects.filter(type='message_after_feedback_form')[0].message
                except:
                    pass
                respond.update({"message": mess})
                return respond
            else:

                if 'eman' in request.POST:
                    context.update({"name": request.POST['eman']})
                if 'email' in request.POST:
                    context.update({"email": request.POST['email']})
                if 'message' in request.POST:
                    context.update({"message": request.POST['message']})
                context.update({"form": form,
                                "success": success,
                                })
                return context
    return None