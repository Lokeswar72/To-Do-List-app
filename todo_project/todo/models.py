from django.db import models

# models.py
class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=[
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low')
    ], blank=True)
    position = models.PositiveIntegerField(default=0)  # New field

    class Meta:
        ordering = ['position']  # Default sort

