from django.db import models

class Problem(models.Model):
     
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    constraints = models.TextField(blank=True)
    time_limit = models.IntegerField(help_text="Time limit in milliseconds")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class TestCase(models.Model):
    
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='test_cases'
    )
    input_data = models.TextField()
    expected_output = models.TextField()
    is_sample = models.BooleanField(default=False)

    def __str__(self):
        return f"TestCase for {self.problem.title} (Sample: {self.is_sample})"