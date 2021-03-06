from django import forms
from django.contrib.auth.forms import UserChangeForm

from accounts.models import Payment, Profile
from django.core.exceptions import ValidationError


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'transaction_code']
        # exclude = ['transaction_time']

    def clean(self):
        super().clean()
        code = self.cleaned_data.get('transaction_code')
        amount = self.cleaned_data.get('amount')
        if code and amount:
            if int(code.split('-')[1]) != amount:
                raise ValidationError('رسید و مبلغ تراکنش هم‌خوانی ندارند')

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount % 1000 != 0:
            raise ValidationError('مبلغ پرداختی باید ضریبی از هزار تومان باشد')
        return amount

    def clean_transaction_code(self):
        code = self.cleaned_data.get('transaction_code')
        try:
            # should be in format: bank-<amount>-<TOKEN>#
            # e.g. bank-30000-UHB454GRH73BDYU#
            assert code.startswith('bank-')
            assert code.endswith('#')
            int(code.split('-')[1])
        except:
            raise ValidationError('قالب رسید تراکنش معتبر نیست')
        return code


class MyUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name', 'email']
    password = None


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile', 'gender', 'address', 'profile_image']