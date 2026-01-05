from django.db import models
from django.conf import settings
from apps.problems.models import Problem

class ProgrammingLanguage(models.TextChoices):
    # Popular / Core
    PYTHON = 'python', 'Python'
    JAVA = 'java', 'Java'
    CPP = 'cpp', 'C++'
    C = 'c', 'C'
    JAVASCRIPT = 'javascript', 'JavaScript'

    # JVM & Modern
    KOTLIN = 'kotlin', 'Kotlin'
    SCALA = 'scala', 'Scala'

    # Microsoft
    CSHARP = 'csharp', 'C#'
    FSHARP = 'fsharp', 'F#'

    # System / Performance
    RUST = 'rust', 'Rust'
    GO = 'go', 'Go'

    # Scripting
    PHP = 'php', 'PHP'
    RUBY = 'ruby', 'Ruby'
    PERL = 'perl', 'Perl'
    LUA = 'lua', 'Lua'

    # Functional
    HASKELL = 'haskell', 'Haskell'
    CLOJURE = 'clojure', 'Clojure'
    ERLANG = 'erlang', 'Erlang'
    ELIXIR = 'elixir', 'Elixir'

    # Data / Scientific
    R = 'r', 'R'
    JULIA = 'julia', 'Julia'

    # Others (optional but nice)
    SWIFT = 'swift', 'Swift'
    DART = 'dart', 'Dart'
    OBJECTIVEC = 'objectivec', 'Objective-C'

class SubmissionStatus(models.TextChoices):
    PENDING = 'pending','Pending'
    ACCEPTED = 'accepted','Accepted'
    FAILED = 'failed','Failed'
    ERROR = 'error','Error'


class Submission(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
    )

    language = models.CharField(
        max_length=20,
        choices=ProgrammingLanguage.choices
    )

    code = models.TextField()
    result = models.CharField(
        max_length=20,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.PENDING
    )
    execution_time = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.problem.title} in {self.language}"



