#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Wallet
#from .processor import PaylineProcessor


class WalletForm(forms.ModelForm):
    """Create or update a wallet."""
    card_cvx = forms.CharField(label=_('Card CVX code'),
                               help_text=_('Security code, three numbers from '
                                           'the back of the payment card'),
                               max_length=3)

    class Meta:
        model = Wallet
        fields=("first_name","last_name","card_number","card_type","card_expiry")
