# student_app/models.py

from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    grade = models.IntegerField(help_text="e.g., 9, 10, 11, 12")
    major = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Science, Arts, Commerce")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"