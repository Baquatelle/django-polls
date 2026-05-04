"""
Models for the polls application.
"""

import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Represents a poll question.
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        """Return a string representation of the question."""
        return self.question_text

    def was_published_recently(self):
        """
        Check if the question was published within the last 24 hours.
        """
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    """
    Represents a choice for a poll question.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return a string representation of the choice."""
        return self.choice_text
