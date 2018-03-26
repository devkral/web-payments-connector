from django.dispatch import Signal
__all__ = ["status_changed"]

# Signal sent whenever status is changed for a Payment. This usually happens
# when a transaction is either accepted or rejected.
status_changed = Signal()
