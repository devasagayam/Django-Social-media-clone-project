from datetime import datetime, timedelta

from uuid import uuid4

from django.db import models
try:  # available from Django1.4
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

from django.utils.translation import ugettext_lazy as _

#from .processor import PaylineProcessor
from django.contrib.auth import get_user_model
User = get_user_model()

def get_uuid4():
    return str(uuid4())


def expiry_date_to_datetime(expiry_date):
    """Convert a credit card expiry date to a datetime object.

    The datetime is the last day of the month.

    """
    exp = datetime.strptime(expiry_date, '%m%y')  # format: MMYY
    # to find the next month
    # - add 31 days (more than a month) to the first day of the current month
    # - replace the day to be "1"
    # - substract one day
    exp += timedelta(days=31)
    exp = exp.replace(day=1)
    exp -= timedelta(days=1)
    return exp


class Wallet(models.Model):
    #Virtual Wallet: hold payment information

    CARD_TYPE_CHOICES = (
        ('CB', "Carte Bleu / VISA / Mastercard"),
        ('AMEX', "American Express"))
    user = models.ForeignKey(User, related_name="wallet",on_delete=models.CASCADE)
    wallet_id = models.CharField(
        max_length=36, default=get_uuid4,
        editable=False, db_index=True, unique=True)
    first_name = models.CharField(
        _("First name"), max_length=30, help_text=_("Card owner first name"))
    last_name = models.CharField(
        _("Last name"), max_length=30, help_text=_("Card owner last name"))
    card_number = models.CharField(_("Card number"), max_length=20)
    card_type = models.CharField(
        _("Card type"), max_length=20, choices=CARD_TYPE_CHOICES)
    card_expiry = models.CharField(
        _("Card expiry"), max_length=4,
        help_text=_("Format: MMYY (eg 0213 for february 2013)"))

    class Meta:
        verbose_name = ("wallet")
        verbose_name_plural = ("wallets")

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def is_valid(self):
        #Return True if the card expiry date is in the future.
        exp = expiry_date_to_datetime(self.card_expiry)
        today = datetime.today()
        return exp >= expiry_date_to_datetime(today.strftime('%m%y'))

    def expires_this_month(self):
        #Return True if the card expiry date is in this current month
        today = datetime.today().strftime("%m%y")
        return today == self.card_expiry
