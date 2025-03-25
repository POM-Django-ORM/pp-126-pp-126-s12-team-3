from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


class CustomUser(AbstractBaseUser):

    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length=128) 
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name']


    def __str__(self):
        return (
            f"'id': {self.id}, 'first_name': '{self.first_name}', 'middle_name': '{self.middle_name}', "
            f"'last_name': '{self.last_name}', 'email': '{self.email}', 'created_at': {self.created_at}, "
            f"'updated_at': {self.updated_at}, 'role': {self.role}, 'is_active': {self.is_active}"
        )

    def __repr__(self):
        return f"CustomUser(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None

    @staticmethod
    def delete_by_id(user_id):
        user = CustomUser.get_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        if not email or "@" not in email or len(email) > 100:
            return None
        if CustomUser.objects.filter(email=email).exists():
            return None
        if first_name is None or len(first_name) > 20:
            return None
        if middle_name is None or len(middle_name) > 20:
            return None
        if last_name is None or len(last_name) > 20:
            return None
        now = timezone.now()
        user = CustomUser(
            email=email,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            created_at=now,
            updated_at=now,
            role=0,
            is_active=False
        )
        user.save()
        return user


    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': int(self.created_at.timestamp()),
            'updated_at': int(self.updated_at.timestamp()),
            'role': self.role,
            'is_active': self.is_active
        }
        

    def update(self, *args, first_name=None, last_name=None, middle_name=None, password=None, role=None, is_active=None):
        if args:
            if len(args) != 6:
                raise TypeError("update() takes either no positional arguments or exactly 6 positional arguments")
            first_name_arg, middle_name_insert, last_name_arg, password_arg, role_arg, is_active_arg = args
            if first_name_arg is not None and len(first_name_arg) <= 20:
                self.first_name = first_name_arg
            if middle_name_insert is not None and self.middle_name:
                n = len(self.middle_name)
                half = n // 2
                self.middle_name = self.middle_name[:half] + middle_name_insert + self.middle_name[half:]
            if last_name_arg is not None and len(last_name_arg) <= 20:
                self.last_name = last_name_arg
            if password_arg is not None:
                self.password = password_arg
            if role_arg is not None:
                self.role = role_arg
            if is_active_arg is not None:
                self.is_active = is_active_arg
        else:
            if first_name is not None and len(first_name) <= 20:
                self.first_name = first_name
            if last_name is not None and len(last_name) <= 20:
                self.last_name = last_name
            if middle_name is not None and len(middle_name) <= 20:
                self.middle_name = middle_name
            if password is not None:
                self.password = password
            if role is not None:
                self.role = role
            if is_active is not None:
                self.is_active = is_active
                

        self.updated_at = timezone.now()
        self.save()

        

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        return 'admin' if self.role == 1 else 'visitor'
