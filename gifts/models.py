from django.db import models
from django.utils import timezone

# Create your models here.


class Gift(models.Model):
    wished_by = models.ForeignKey('auth.User', related_name='wished_gifts')
    # Assumed that particular gift could be bought only once
    # by one person (user)
    bought_by = models.ForeignKey('auth.User', related_name='bought_gifts',
                                  blank=True, null=True)
    # there is no unique constraints on (wished_by, name) tuple
    # so a person could wish the same gift multiple times
    name = models.CharField(max_length=200)
    # price is limited by 99999.99 :)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    reg_date = models.DateTimeField(default=timezone.now)
    bought_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} for {}".format(self.name, self.wished_by)

    @classmethod
    def register(cls, user, name, price):
        gift = cls(wished_by=user, name=name, price=price)
        gift.save()

    @classmethod
    def browse_unfulfilled(cls, user):
        return cls.objects.filter(bought_by__isnull=True).\
            exclude(wished_by=user)

    def buy(self, user):
        self.bought_by = user
        self.bought_date = timezone.now()
        self.save()
