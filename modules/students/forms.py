from django import forms


class EnrollmentNoteForm(forms.Form):
	note = forms.IntegerField()
	enrollment_id = forms.CharField()


class EnrollmentAttendanceForm(forms.Form):
	date = forms.CharField()


class EnrollmentPaymentForm(forms.Form):
	amount = forms.DecimalField()