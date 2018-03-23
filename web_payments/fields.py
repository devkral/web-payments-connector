from calendar import monthrange
from datetime import date
import re

from wtforms import fields
from wtforms.widgets import html_params, HTMLString

from .utils import get_credit_card_issuer
from .translation import translation
_ = translation.gettext_lazy

def get_month_choices():
    month_choices = [(str(x), '%02d' % (x,)) for x in range(1, 13)]
    return [('', _('Month'))] + month_choices


def get_year_choices():
    year_choices = [(str(x), str(x)) for x in range(
        date.today().year, date.today().year + 15)]
    return [('', _('Year'))] + year_choices


class TextWidget(object):
    """
    """
    html_params = staticmethod(html_params)


    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        return HTMLString('<input %s>' % self.html_params(name=field.name, **kwargs))

class MyTextInput(TextInput):
    def __init__(self, error_class=u'has_errors'):
        super(MyTextInput, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = u'%s %s' % (self.error_class, c)
        return super(MyTextInput, self).__call__(field, **kwargs)


class CreditCardNumberField(forms.CharField):

    widget = CreditCardNumberWidget(
        attrs={'autocomplete': 'cc-number', 'required': 'required'})
    default_error_messages = {
        'invalid': _('Please enter a valid card number'),
        'invalid_type': _('We accept only %(valid_types)s')}

    def __init__(self, valid_types=None, *args, **kwargs):
        self.valid_types = valid_types
        kwargs['max_length'] = kwargs.pop('max_length', 32)
        super(CreditCardNumberField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is not None:
            value = re.sub('[\s-]+', '', value)
        return super(CreditCardNumberField, self).to_python(value)

    def validate(self, value):
        card_type, issuer_name = get_credit_card_issuer(value)
        if value in validators.EMPTY_VALUES and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        if value and not self.cart_number_checksum_validation(self, value):
            raise forms.ValidationError(self.error_messages['invalid'])
        if (value and not self.valid_types is None
                and not card_type in self.valid_types):
            valid_types = map(issuer_name, self.valid_types)
            error_message = self.error_messages['invalid_type'] % {
                'valid_types': ', '.join(valid_types)
            }
            raise forms.ValidationError(error_message)

    @staticmethod
    def cart_number_checksum_validation(cls, number):
        digits = []
        even = False
        if not number.isdigit():
            return False
        for digit in reversed(number):
            digit = ord(digit) - ord('0')
            if even:
                digit *= 2
                if digit >= 10:
                    digit = digit % 10 + digit // 10
            digits.append(digit)
            even = not even
        return sum(digits) % 10 == 0 if digits else False



class CreditCardExpiryField(forms.MultiValueField):

    default_error_messages = {
        'invalid_month': 'Enter a valid month.',
        'invalid_year': 'Enter a valid year.'}

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        fields = (
            forms.ChoiceField(
                choices=get_month_choices(),
                error_messages={'invalid': errors['invalid_month']},
                widget=forms.Select(
                    attrs={'autocomplete': 'cc-exp-month',
                           'required': 'required'})),
            forms.ChoiceField(
                choices=get_year_choices(),
                error_messages={'invalid': errors['invalid_year']},
                widget=forms.Select(
                    attrs={'autocomplete': 'cc-exp-year',
                           'required': 'required'})),
        )

        super(CreditCardExpiryField, self).__init__(fields, *args, **kwargs)
        self.widget = CreditCardExpiryWidget(widgets=[fields[0].widget,
                                                      fields[1].widget])

    def clean(self, value):
        exp = super(CreditCardExpiryField, self).clean(value)
        if exp and date.today() > exp:
            raise forms.ValidationError(
                "The expiration date you entered is in the past.")
        return exp

    def compress(self, data_list):
        if data_list:
            if data_list[1] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_year']
                raise forms.ValidationError(error)
            if data_list[0] in forms.fields.EMPTY_VALUES:
                error = self.error_messages['invalid_month']
                raise forms.ValidationError(error)
            year = int(data_list[1])
            month = int(data_list[0])
            # find last day of the month
            day = monthrange(year, month)[1]
            return date(year, month, day)
        return None


class CreditCardVerificationField(forms.CharField):

    widget = forms.TextInput(
        attrs={'autocomplete': 'cc-csc'})
    default_error_messages = {
        'invalid': _('Enter a valid security number.')}

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.pop('max_length', 4)
        super(CreditCardVerificationField, self).__init__(*args, **kwargs)

class CreditCardNameField(forms.CharField):

    widget = forms.TextInput(
        attrs={'autocomplete': 'cc-name', 'required': 'required'})
