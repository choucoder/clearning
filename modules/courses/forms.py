from django import forms


class CourseCreateForm(forms.Form):

	name = forms.CharField(required=True)
	categories = forms.CharField(required=True)
	description = forms.CharField(required=True)


class CourseOpeningForm(forms.Form):
	
	course_name_search = forms.CharField(required=False)
	course_name = forms.CharField(required=False)
	categories = forms.CharField(required=False)
	course_price = forms.FloatField(required=False)
	course_description = forms.CharField(required=False)
	course_register_checkbox = forms.CharField(required=False)
	date_start = forms.CharField(required=True)
	date_end = forms.CharField(required=True)

	teacher_name_search = forms.CharField(required=False)
	teacher_identification_number = forms.CharField(required=False)
	teacher_names = forms.CharField(required=False)
	teacher_surnames = forms.CharField(required=False)
	teacher_email = forms.CharField(required=False)
	teacher_phone = forms.CharField(required=False)
	teacher_register_checkbox = forms.CharField(required=False)


class EnrollmentForm(forms.Form):

	student_name_search = forms.CharField(required=False)
	
	student_identification_number = forms.CharField(required=False)
	student_names = forms.CharField(required=False)
	student_surnames = forms.CharField(required=False)
	student_email = forms.CharField(required=False)
	student_phone = forms.CharField(required=False)
	student_payment = forms.FloatField(required=False)

	student_register_checkbox = forms.CharField(required=False)
