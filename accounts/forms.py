from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'role', 'password1', 'password2')

    # FIX: Added clean_email to check for existing users
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if username or email already exists to prevent IntegrityError
        if CustomUser.objects.filter(username=email).exists() or CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists. Please log in.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
    profile_picture = forms.ImageField(required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'profile_picture')