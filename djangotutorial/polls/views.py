"""
Views for the polls application.
"""

from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login
from .forms import RegisterForm

from .models import Choice, Question


def register(request):
    """
    Handle user registration using the custom RegisterForm.
    If the request is POST, validate the form, save the user (using email as username),
    log the user in, and redirect to the index page.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("polls:index")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


class IndexView(generic.ListView):
    """
    Display the latest five published questions.
    """

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    """
    Display a specific question's text and a voting form.
    """

    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    """
    Display the results for a specific question.
    """

    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    """
    Handle voting for a particular choice in a specific question.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
