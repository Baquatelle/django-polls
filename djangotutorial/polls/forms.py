from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    A custom registration form that uses email as the username.
    """

    email = forms.EmailField(
        required=True, help_text="Required. A valid email address."
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    def save(self, commit=True):
        """
        Save the provided email as the username.
        """
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
