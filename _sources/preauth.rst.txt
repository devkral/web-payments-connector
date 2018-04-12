.. _capture-payments:

Authorization and capture
=========================

Some gateways offer a two-step payment method known as Authorization & Capture, which allows you to collect the payment manually after the buyer has authorized it. To enable this payment type, you have to set the ``capture`` parameter to ``False`` in the configuration of payment backend::

      # settings.py
      PAYMENT_VARIANTS_API = {
          'default': ('web_payments_dummy.DummyProvider', {'capture': False}, {})}

      # as PaymentVariant
          ...
          PaymentVariant('web_payments_dummy.DummyProvider', {'capture': False}, {})
          ....


Capturing the payment
---------------------
To capture the payment from the buyer, call the ``capture()`` method on the :class:`Payment` instance::

      >>> payment = Payment.objects.get()
      >>> payment.capture()

By default, the total amount will be captured and the capture will be finalized. You can capture a lower amount, by providing the ``amount`` parameter and take multiple captures by providing final::

      >>> from decimal import Decimal
      >>> captured_amount = payment.capture(amount=Decimal(10.0), final=False)
      >>> payment.capture(amount=Decimal(10.0), final=True)

.. note::

  Only payments with the ``preauth`` status can be captured.


Releasing the payment
---------------------
To release the payment to the buyer, call the ``release()`` method on your :class:`Payment` instance::

      >>> payment = Payment.objects.get()
      >>> payment.release()

.. note::

  Only payments with the ``preauth`` status can be released (voiding transaction).
