from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL

class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, related_name='borrows')
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)

    def is_returned(self):
        return self.return_date is not None

    def is_late(self):
        if self.is_returned():
            return self.return_date > self.due_date
        return timezone.now() > self.due_date

    def days_late(self):
        if self.is_returned() and self.return_date > self.due_date:
            delta = self.return_date - self.due_date
            return delta.days
        elif not self.is_returned() and timezone.now() > self.due_date:
            delta = timezone.now() - self.due_date
            return delta.days
        return 0
