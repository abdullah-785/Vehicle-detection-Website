from django import forms


class userForm(forms.Form):
    num1 = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    num2 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))



