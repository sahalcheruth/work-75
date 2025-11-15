from django import forms
from django.contrib.auth.models import User
import re
from .models import Address, Company

class RegisterForm(forms.ModelForm):
    # Password
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput
    )

    # Address fields
    street = forms.CharField(max_length=100)
    suite = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    zipcode = forms.CharField(max_length=20)

    # Company fields
    company_name = forms.CharField(max_length=100)
    company_catchPhrase = forms.CharField(max_length=200)
    company_bs = forms.CharField(max_length=200)

    # Profile fields
    phone = forms.CharField(max_length=50)
    website = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email']

    # -------------------- VALIDATIONS --------------------

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already used.")
        return email

    # PASSWORD RULE VALIDATION
    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match!")

        if len(p1) != 11:
            raise forms.ValidationError("Password must be exactly 11 characters.")

        pattern = r'^[A-Z]{5}[0-9]{6}$'
        if not re.match(pattern, p1):
            raise forms.ValidationError(
                "Password must start with 5 CAPITAL LETTERS followed by 6 digits (Example: ABCDE123456)."
            )

        return p2

    # -------------------- SAVE --------------------
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


# from django import forms
# from django.contrib.auth.models import User
# import re

# class RegisterForm(forms.ModelForm):
#     password1 = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput
#     )
#     password2 = forms.CharField(
#         label='Confirm Password',
#         widget=forms.PasswordInput
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'email']

#     # Username validation
#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError("Username already taken.")
#         return username

#     # Email validation
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Email already used.")
#         return email

#     # Password validation
#     def clean_password2(self):
#         p1 = self.cleaned_data.get('password1')
#         p2 = self.cleaned_data.get('password2')

#         # Match check
#         if p1 and p2 and p1 != p2:
#             raise forms.ValidationError("Passwords do not match!")

#         # Length check
#         if len(p1) != 11:
#             raise forms.ValidationError("Password must be exactly 11 characters.")

#         # Format check: 5 uppercase + 6 digits
#         pattern = r'^[A-Z]{5}[0-9]{6}$'
#         if not re.match(pattern, p1):
#             raise forms.ValidationError(
#                 "Password must start with 5 CAPITAL LETTERS followed by 6 digits (Example: ABCDE123456)."
#             )

#         return p2

#     # Save user with hashed password
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password1'])
#         if commit:
#             user.save()
#         return user
