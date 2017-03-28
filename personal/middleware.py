# -*- coding: utf-8 -*-

from accounts.forms import AuthenticationForm, RegistrationForm

class AccountsMiddleware(object):
    def process_request(self, request):
        request.auth_form = AuthenticationForm()
        request.reg_form = RegistrationForm()
