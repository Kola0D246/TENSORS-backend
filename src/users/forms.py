from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

class LowercaseEmailMixin:
    """Lower-case the email before the uniqueness check runs."""

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

class CustomUserCreationForm(LowercaseEmailMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

class CustomUserChangeForm(LowercaseEmailMixin, UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'
