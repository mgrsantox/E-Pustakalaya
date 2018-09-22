from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter the date between 5 week defaul is 2')
    def clean_renewal_date(self):

        data = self.cleaned_data['renewal_date']
#         Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

         # Check if a date is in the allowed range (+5 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=5):
            raise ValidationError(_('Invalid date - renewal more than 5 weeks ahead'))
        return data
