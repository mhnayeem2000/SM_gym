from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from branches.models import GymBranch


class WorkoutPlan(models.Model):
    # Creation workout plan by trainer for his branch
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.ROLE_TRAINER},
        related_name='created_plans'
    )
    
    branch = models.ForeignKey(
        GymBranch,
        on_delete=models.CASCADE,
        related_name='workout_plans'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Workout Plan"
        verbose_name_plural = "Workout Plans"

    def __str__(self):
        return f"{self.title} ({self.branch.name})"

    def clean(self):
        if self.created_by.branch != self.branch:
            raise ValidationError("Trainer must belong to the same branch as the plan.")


class WorkoutTask(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    )

    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.ROLE_MEMBER},
        related_name='workout_tasks'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)          
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', 'created_at']
        verbose_name = "Workout Task"
        verbose_name_plural = "Workout Tasks"
        unique_together = ['workout_plan', 'member']

    def __str__(self):
        return f"{self.workout_plan.title} → {self.member.email}"

    def clean(self):
        if self.workout_plan.branch != self.member.branch:
            raise ValidationError("Member must belong to the same branch as the workout plan.")