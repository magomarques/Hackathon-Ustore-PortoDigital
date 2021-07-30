from django.db import models

# Create your models here.

# 0 'bill/InvoiceId'
# 1 'bill/PayerAccountId'
# 2 'bill/BillingPeriodStartDate'
# 3 'bill/BillingPeriodEndDate'
# 4 'lineItem/UsageAccountId'
# 5 'lineItem/UsageStartDate'
# 6 'lineItem/UsageEndDate'
# 7 'lineItem/ProductCode'
# 8 'lineItem/UsageAmount'
# 9 'lineItem/BlendedRate'
#10 'lineItem/BlendedCost'


class Data(models.Model):
    invoiceId = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    payerAccountId = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    billingPeriodStartDate = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    billingPeriodEndDate = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    usageAccountId = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    usageStartDate = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    usageEndDate = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    productCode = models.CharField(
        default=0,
        max_length=255,
        null=False,
        blank=False
    )

    usageAmount = models.CharField(
        default=0,
        max_length=20,
        null=False,
        blank=False
    )

    blendedRate = models.CharField(
        default=0,
        max_length=20,
        null=False,
        blank=False
    )

    blendedCost = models.CharField(
        default=0,
        max_length=20,
        null=False,
        blank=False
    )

    