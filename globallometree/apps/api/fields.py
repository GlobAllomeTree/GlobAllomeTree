import decimal
from rest_framework.fields import DecimalField

class RoundingDecimalField(DecimalField):

    def validate_precision(self, value):
        """
        Override to round decimals off
        """

        if self.decimal_places is not None:
            value = decimal.Decimal(str(round(value, self.decimal_places)))

        return super(RoundingDecimalField, self).validate_precision(value)


    def quantize(self, value):
        """
        Quantize the decimal value to the configured precision.
        """
        context = decimal.getcontext().copy()
        context.prec = self.max_digits
        return value.quantize(
            decimal.Decimal('.1') ** self.decimal_places,
            context=context).normalize()
