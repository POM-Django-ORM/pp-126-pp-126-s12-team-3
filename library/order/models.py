from django.db import models
from django.utils.timezone import now
import datetime


class Order(models.Model):
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)  # Зв’язок з книгою
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення замовлення
    end_at = models.DateTimeField(blank=True, null=True)  # Дата повернення (timestamp)
    plated_end_at = models.DateTimeField(blank=True, null=True) # Планована дата повернення (timestamp)

    def __str__(self):
        created_at_str = str(self.created_at)
        plated_end_at_str = str(self.plated_end_at) if self.plated_end_at is not None else "None"
        end_at_str = f"'{self.end_at}'" if self.end_at is not None else "None"
        return (f"'id': {self.id}, 'user': CustomUser(id={self.user.id if self.user else 'None'}), "
                f"'book': Book(id={self.book.id}), 'created_at': '{created_at_str}', "
                f"'end_at': {end_at_str}, 'plated_end_at': '{plated_end_at_str}'")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            'id': self.id,
            'book': self.book.id,
            'user': self.user.id if self.user else None,
            'created_at': int(self.created_at.timestamp()),
            'end_at': int(self.end_at.timestamp()) if self.end_at else None,
            'plated_end_at': int(self.plated_end_at.timestamp()) if self.plated_end_at else None
        }

    @staticmethod
    def create(user, book, plated_end_at):
        if user is not None and not user.pk:
            return None
        active_orders = Order.objects.filter(book=book, end_at__isnull=True).count()
        if active_orders >= book.count:
            return None
        order = Order(user=user, book=book, plated_end_at=plated_end_at)
        order.save()
        return order

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at is not None:
            self.plated_end_at = plated_end_at
        if end_at is not None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return list(Order.objects.all())

    @staticmethod
    def get_not_returned_books():
        return list(Order.objects.filter(end_at__isnull=True))

    @staticmethod
    def delete_by_id(order_id):
        order = Order.get_by_id(order_id)
        if order:
            order.delete()
            return True
        return False
