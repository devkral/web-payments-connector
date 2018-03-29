
import os
from web_payments.translation import Translation

translation_path = os.path.join(os.path.dirname(__file__), "locale")

translation = Translation("web_payments_externalpayments.translation", translation_path, domain="web_payments")
