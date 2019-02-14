from django.contrib.auth.forms import AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from django.utils.translation import gettext
from crispy_forms.layout import Button, Div, Layout, Field, Hidden, Submit


class CoreAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the crispy form
        self.helper = FormHelper()
        self.helper.form_class='form justify-content-center'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field(
                    'username',
                    placeholder=gettext('username'),
                    title=gettext("Username"),
                    css_class='form-control',
                    wrapper_class='form-group',
                ),
                Field(
                    'password',
                    placeholder=gettext('password'),
                    title=gettext("Password"),
                    css_class='form-control',
                    wrapper_class='form-group',
                ),
                css_class="form-group"
            ),
            Submit(
                'submit',
                gettext('Login'),
                css_class='btn btn-secondary',
            ),
        )



