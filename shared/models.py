from django.contrib.auth.models import User
from django.db import models

class HistoryDates(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


class ItemBase(HistoryDates):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_related"
    )
    title = models.CharField(max_length=250)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title