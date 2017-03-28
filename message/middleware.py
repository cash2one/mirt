# -*- coding: utf-8 -*-


from message.models import Message, Mail

class MessageMiddleware(object):
    def process_request(self, request):
        for message in Message.objects.all():
            setattr(request,message.type,message.message)

class MailMiddleware(object):
    def process_request(self, request):
        for mail in Mail.objects.all():
            setattr(request,mail.type,mail)