from django.db import models
from django.utils import timezone
from django.db.models import Sum

# Create your models here.


class Gift(models.Model):
    wished_by = models.ForeignKey('auth.User', related_name='wished_gifts')
    # v1: Assumed that particular gift could be bought only once
    # by one person (user)
    # v2: bought_by column need to be removed
    #     bought gifts need to be migrated into "contributions"
    bought_by = models.ForeignKey('auth.User', related_name='bought_gifts',
                                  blank=True, null=True)
    # there is no unique constraints on (wished_by, name) tuple
    # so a person could wish the same gift multiple times
    name = models.CharField(max_length=200)
    # price is limited by 99999.99 :)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    reg_date = models.DateTimeField(default=timezone.now)
    # bought date could be used to filter unfulfilled gifts
    bought_date = models.DateTimeField(blank=True, null=True)
    # contributed value, calculated by `contribute` method
    # FIXME it would be nice to have ON INSERT trigger on Contribution table
    #       to update gift.contrib_sum automatically
    #       when the record is created from Django admin
    contrib_sum = models.DecimalField(max_digits=7, decimal_places=2,
                                      default=0)

    def __str__(self):
        return "{} for {} ({} left)".format(self.name, self.wished_by,
                                            (self.price-self.contrib_sum))

    @classmethod
    def register(cls, user, name, price):
        gift = cls(wished_by=user, name=name, price=price)
        gift.save()

    @classmethod
    def browse_unfulfilled(cls, user):
        # well, we have 2 options:
        # - filter by bought_date is NULL
        # - compare price to contrib_sum
        # for scalability of RDBM engine it's better to have simple
        # query on single column, so we can build index on it
        # or index by (wished_by, bought_date)
        return cls.objects.filter(bought_date__isnull=True).\
            exclude(wished_by=user)

    def buy(self, user):
        self.bought_by = user
        self.bought_date = timezone.now()
        self.save()

    @classmethod
    def contribute(cls, gift, user, value):
        ctb = Contribution(gift=gift, contributed_by=user, value=value)
        ctb.save()
        contrib_sum = Contribution.objects.filter(gift=gift).aggregate(
            contrib_sum=Sum('value')
        )
        if contrib_sum >= gift.price:
            gift.bought_date = timezone.now()
        gift.contrib_sum = contrib_sum
        gift.save()


class Contribution(models.Model):
    gift = models.ForeignKey('gifts.gift', related_name='contributions')
    contributed_by = models.ForeignKey('auth.User',
                                       related_name='contributed_gifts')
    # sometime it could be useful to order records by contribution date
    contrib_date = models.DateTimeField(default=timezone.now)
    value = models.DecimalField(max_digits=7, decimal_places=2)
