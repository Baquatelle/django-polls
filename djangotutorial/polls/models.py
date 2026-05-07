"""
Models for the polls application.
"""

import datetime

from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


class Question(models.Model):
    """
    Represents a poll question.
    """

    id: int
    objects = models.Manager()
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self) -> str:
        """Return a string representation of the question."""
        return str(self.question_text)

    def was_published_recently(self):
        """
        Check if the question was published within the last 24 hours.
        """
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    """
    Represents a choice for a poll question.
    """

    class DoesNotExist(ObjectDoesNotExist):
        """A placeholder for the static checker."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        """Return a string representation of the choice."""
        return str(self.choice_text)
