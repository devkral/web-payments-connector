.. _refunding:

Refunding a payment
===================

If you need to refund a payment, you can do this by calling the ``refund()`` method on your :class:`Payment` instance::

      >>> payment = Payment.objects.get()
      >>> payment.refund()

By default, the total amount would be refunded. You can perform a partial refund, by providing the ``amount`` parameter::

      >>> from decimal import Decimal
      >>> refunded_amount = payment.refund(amount=Decimal(10.0))

.. note::

    Only payments with the ``confirmed`` status can be refunded.
