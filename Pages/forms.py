from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'id':"registerFirstname"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'id':"registerLastname"}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'id':"registerUsername"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'id':"registerEmail"}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id':"registerPassword1"}),
        help_text="Your password can't be too similar to your other personal information. It must contain at least 8 characters, can't be a commonly used password, and can't be entirely numeric."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password', 'id':"registerPassword2"}),
        strip=False,
        help_text="Enter the same password as before, for verification."
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'id': 'loginUsername'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'loginPassword'}),
    )