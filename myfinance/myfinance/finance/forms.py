from datetime import date, datetime
import re


from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from finance.models import Account, Charge


class ChargeForm(ModelForm):

    class Meta:
        model = Charge
        fields = ['value', 'date']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('value') < 0 and \
                cleaned_data.get('date') > date.today():
            self.add_error(
                'date', 'Charges off are not supported for future days. Please, try again.')
        return cleaned_data


class AccountForm(ModelForm):
    CREDIT_CARD_RE = r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\d{11})$'

    class Meta:
        model = Account
        fields = ['name', 'card_num', 'total']

    def clean_card_number(self):
        data = self.cleaned_data['card_num']
        card_num = data.replace(' ', '').replace('-', '')
        if not re.match(self.CREDIT_CARD_RE, data):
            self.add_error(
                'card_num', "Card number you specified is not valid. Plase, specify valid card number.")

        return card_num
