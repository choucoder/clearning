from django import forms


class LoginForm(forms.Form):
	username = forms.CharField(label="Nombre de usuario", required=True)
	password = forms.CharField(label="Contraseña", required=True)


class AccountRegisterForm(forms.Form):
	first_name = forms.CharField(max_length=64)
	last_name = forms.CharField(max_length=64)
	email = forms.CharField(max_length=128)
	username = forms.CharField(max_length=128)
	password = forms.CharField(max_length=128)
	password_confirm = forms.CharField(max_length=128)