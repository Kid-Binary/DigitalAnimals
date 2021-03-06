from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class OrderForm(forms.Form):
    name = forms.CharField(
        min_length=3, max_length=250,
    )
    email = forms.EmailField(max_length=254,)
    phone = forms.CharField(
        max_length=19,
    )
    message = forms.CharField(
        min_length=5, max_length=500, widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        # Name
        self.fields['name'].label = _('order.name.label')
        self.fields['name'].widget.attrs = {
            'placeholder': _('order.name.placeholder'),
            'data-rule-required': 'true',
            'data-msg-required': _('error_messages.name.required'),
            'data-rule-minlength': 3,
            'data-msg-minlength': _('error_messages.name.min_length'),
            'data-rule-maxlength': 250,
            'data-msg-maxlength': _('error_messages.name.max_length'),
        }
        self.fields['name'].error_messages = {
            'required': _('error_messages.name.required'),
            'min_length': _('error_messages.name.min_length'),
            'max_length': _('error_messages.name.max_length'),
        }

        # E-mail
        self.fields['email'].label = _('order.email.label')
        self.fields['email'].widget.attrs = {
            'placeholder': _('order.email.placeholder'),
            'data-rule-required': 'true',
            'data-msg-required': _('error_messages.email.required'),
            'data-rule-email': 'true',
            'data-msg-email': _('error_messages.email.invalid'),
            'data-rule-maxlength': 254,
            'data-msg-maxlength': _('error_messages.email.max_length'),
        }
        self.fields['email'].error_messages = {
            'required': _('error_messages.email.required'),
            'invalid': _('error_messages.email.invalid'),
            'max_length': _('error_messages.email.max_length'),
        }

        # Phone
        self.fields['phone'].label = _('order.phone.label')
        self.fields['phone'].widget.attrs = {
            'placeholder': _('order.phone.placeholder'),
            'data-rule-required': 'true',
            'data-msg-required': _('error_messages.phone.required'),
            'data-rule-maxlength': 19,
            'data-msg-maxlength': _('error_messages.phone.max_length'),
            'data-mask': '+380 (99) 999-9999',
        }
        self.fields['phone'].error_messages = {
            'required': _('error_messages.phone.required'),
            'max_length': _('error_messages.phone.max_length'),
        }

        # Message
        self.fields['message'].widget.attrs = {
            'placeholder': _('order.message.placeholder'),
            'data-rule-required': 'true',
            'data-msg-required': _('error_messages.message.required'),
            'data-rule-minlength': 5,
            'data-msg-minlength': _('error_messages.message.min_length'),
            'data-rule-maxlength': 500,
            'data-msg-maxlength': _('error_messages.message.max_length'),
        }
        self.fields['message'].error_messages = {
            'required': _('error_messages.message.required'),
            'min_length': _('error_messages.message.min_length'),
            'max_length': _('error_messages.message.max_length'),
        }

    def send_email(self):
        html = render_to_string('website/emails/order.html', {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'phone': self.cleaned_data['phone'],
            'message': self.cleaned_data['message'],
        })

        message = EmailMessage(
            ''.join(_('email.order.subject'), self.cleaned_data['name']),
            html,
            'webmaster@digital-animals.in.ua',
            ['makeweb@digital-animals.in.ua']
        )
        message.content_subtype = 'html'
        message.send()
