from django.db import models
from django.utils.timezone import now


class Order(models.Model):
    user = models.ForeignKey('authentication.CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)  # Зв’язок з книгою
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення замовлення
    end_at = models.IntegerField(null=True, blank=True)  # Дата повернення (timestamp)
    plated_end_at = models.IntegerField(default=0)  # Планована дата повернення (timestamp)

    def __str__(self):
        return f"Order(id={self.id}, user={self.user.id if self.user else 'None'}, book={self.book.id}, created_at={self.created_at}, end_at={self.end_at}, plated_end_at={self.plated_end_at})"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    def to_dict(self):
        return {
            'id': self.id,
            'book': self.book.id,
            'user': self.user.id if self.user else None,
            'created_at': self.created_at.timestamp(),
            'end_at': self.end_at,
            'plated_end_at': self.plated_end_at
        }

    @staticmethod
    def create(user, book, plated_end_at):
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
        return Order.objects.all()

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at__isnull=True)

    @staticmethod
    def delete_by_id(order_id):
        order = Order.get_by_id(order_id)
        if order:
            order.delete()
            return True
        return False
