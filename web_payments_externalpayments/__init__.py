from .forms import OrderIdForm, IBANBankingForm
from web_payments import RedirectNeeded, NotSupported
from web_payments.status import PaymentStatus
from web_payments.logic import BasicProvider

__all__ = ["DirectPaymentProvider", "BankTransferProvider"]

class DirectPaymentProvider(BasicProvider):
    '''
        Payment is done manually e.g. cash on delivery, voucher in restaurant.
        Payments are just a placeholder; to allow every further operation set to CONFIRMED.

        :param bool skipform: doesn't show form with data
        :param bool usetoken: if you don't verify the name; don't allow people supplying others order numbers (use token) because it is much longer it defaults to off
        :param str prefix: add prefix to payment id as reference
        :param bool confirm: set PaymentStatus to CONFIRMED when get_form completes
    '''

    def __init__(self, skipform=True, confirm=False,
                 usetoken=False, prefix="", **kwargs):
        super(DirectPaymentProvider, self).__init__(**kwargs)
        self.skipform = skipform
        self.prefix = prefix
        self.usetoken = usetoken
        self.confirm = confirm
        if not self._capture:
            raise NotSupported(
                'Direct Payments do not support pre-authorization.')

    def get_form(self, payment, data=None):
        if not payment.id:
            payment.save()
        if not payment.transaction_id:
            if self.usetoken:
                payment.transaction_id = "{}{}-{}".format(self.prefix, payment.id, payment.token)
            else:
                payment.transaction_id = "{}{}".format(self.prefix, payment.id)
            payment.save()
        if not self.skipform:
            if not data or not data.get("order", None):
                return OrderIdForm(data={"order": payment.transaction_id},
                                   payment=payment,
                                   provider=self)
        if self.confirm:
            payment.change_status(PaymentStatus.CONFIRMED)
        else:
            payment.change_status(PaymentStatus.WAITING)
        raise RedirectNeeded(payment.get_success_url())

    def refund(self, payment, amount=None):
        if not amount:
            amount = payment.total
        payment.change_status(PaymentStatus.REFUNDED)
        return amount

class BankTransferProvider(BasicProvider):
    '''
        Banking software or human confirms transaction.
        Because there is no security problems if somebody pays for somebody else and references can not hold many characters, only the id is required.
        The form is used to show the user the data he has to send.

        :param str iban: IBAN number
        :param str bic: BIC number
        :param str prefix: add prefix to payment id as reference
        :param bool confirm: set PaymentStatus to CONFIRMED when get_form completes
    '''

    def __init__(self, iban, bic, confirm=False,
                 prefix="", **kwargs):
        if len(iban) <= 10 or len(bic) <= 4:
            raise NotSupported("Wrong IBAN or BIC")
        self.iban = iban.upper()
        self.bic = bic.upper()
        self.confirm = confirm
        self.prefix = prefix
        super(BankTransferProvider, self).__init__(**kwargs)
        if not self._capture:
            raise NotSupported(
                'Advance Payment does not support pre-authorization.')

    def get_fields(self, payment):
        return {
            'iban': self.iban,
            'bic': self.bic,
            'order': payment.transaction_id
        }

    def get_form(self, payment, data=None):
        if not payment.id:
            payment.save()
        if not payment.transaction_id:
            payment.transaction_id = "{}{}".format(self.prefix, payment.id)
            payment.save()
        if not data or not data.get("order", None):
            return IBANBankingForm(data=self.get_fields(payment), payment=payment, provider=self)
        if self.confirm:
            payment.change_status(PaymentStatus.CONFIRMED)
        else:
            payment.change_status(PaymentStatus.WAITING)
        raise RedirectNeeded(payment.get_success_url())

    def refund(self, payment, amount=None):
        if not amount:
            amount = payment.total
        payment.change_status(PaymentStatus.REFUNDED)
        return amount
