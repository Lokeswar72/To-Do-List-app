from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)  # Existing field
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, null=True, blank=True)  # NEW

    def __str__(self):
        return self.title
