from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from branches.models import GymBranch


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

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
        help_text="Determines the user's permissions and access level."
    )

    branch = models.ForeignKey(
        GymBranch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="Gym Branch",
        help_text="The gym branch this user belongs to. Leave empty for Super Admin."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',           
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        role_display = self.get_role_display() or self.role
        return f"{self.email} ({role_display})"

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

    def clean(self):
        super().clean()
        if self.role == self.ROLE_ADMIN and self.branch is not None:
            raise ValidationError(_("Super Admin should not be assigned to any branch."))
        if self.role != self.ROLE_ADMIN and self.branch is None:
            raise ValidationError(_("Non-admin users must be assigned to a branch."))