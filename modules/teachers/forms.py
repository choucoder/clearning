from django import forms


class TeacherCreateForm(forms.Form):

	identification_number = forms.CharField(max_length=16)
	names = forms.CharField(max_length=32)
	surnames = forms.CharField(max_length=32)
	email = forms.EmailField()
	phone = forms.CharField()