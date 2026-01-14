from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from branches.models import GymBranch


class User(AbstractUser):
    #  Different user role 
    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_TRAINER = 'trainer'
    ROLE_MEMBER = 'member'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Super Admin'),
        (ROLE_MANAGER, 'Gym Manager'),
        (ROLE_TRAINER, 'Trainer'),
        (ROLE_MEMBER, 'Member'),
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER,
        help_text="User's role in the system determines permissions."
    )

    branch = models.ForeignKey(
        GymBranch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="Gym Branch",
        help_text="Branch this user belongs to. Leave empty for Super Admin."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def is_super_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_manager(self):
        return self.role == self.ROLE_MANAGER

    @property
    def is_trainer(self):
        return self.role == self.ROLE_TRAINER

    @property
    def is_member(self):
        return self.role == self.ROLE_MEMBER