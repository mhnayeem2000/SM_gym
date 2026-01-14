from django.db import models
from django.utils.translation import gettext_lazy as _


class GymBranch(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name of the gym branch (Ex:  'Dhakkhin Khan GYM')"
    )
    location = models.CharField(
        max_length=200,
        help_text="Address of the GYM (Ex:  ' 89/2, Dhakkhin Khan, Dhaka' )"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Gym Branch"
        verbose_name_plural = "Gym Branches"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.location})"

    def trainer_count(self):
        from accounts.models import User
        return User.objects.filter(branch=self, role=User.ROLE_TRAINER).count()