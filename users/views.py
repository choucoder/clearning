from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator

from .forms import LoginForm, AccountRegisterForm, ForgotPasswordForm
from .models import UserAccount
from modules.plans.models import Plan


class LoginView(View):

	template_name = 'users/login.html'
	form = LoginForm

	def get(self, request):
		context = {}
		context['status'] = 100

		if str(request.user) != "AnonymousUser":
			return redirect(reverse('main:home'))

		return render(request, self.template_name, context)

	def post(self, request):
		context = {}
		form_data = self.form(request.POST)

		if form_data.is_valid():
			username = form_data.cleaned_data['username']
			password = form_data.cleaned_data['password']
			logged_user = authenticate(username=username, password=password)

			if logged_user is not None:
				login(request, logged_user)
				context['status'] = 200
				context['message'] = 'Autenticación exitosa'
				return redirect(reverse('main:home'))
			else:
				context['status'] = 400
				context['message'] = 'Credenciales invalidas'
				return render(request, self.template_name, context)
		else:
			context['status'] = 400
			context['message'] = "Datos ingresados invalidos"

		return render(request, self.template_name, context)


class LogoutView(View):

	def get(self, request):
		logout(request)
		return redirect(reverse('users:login'))


@method_decorator([login_required], name='dispatch')
class TeacherRegisterView(View):

	form = AccountRegisterForm
	model = UserAccount
	template_name = 'users/register.html'

	def get(self, request):
		context = {}
		context['user_type'] = User.TEACHER

		return render(request, self.template_name, context)


	def post(self, request):
		context = {}
		form_data = self.form(request.POST)

		if form_data.is_valid():
			try:
				teacher = UserAccount(**form_data.cleaned_data)
				teacher.password = make_password(teacher.password)
				teacher.save()
			except Exception as e:
				print(f"E: {e}")
				pass

		return self.get(request, context)


class AccountRegisterView(View):

	form = AccountRegisterForm
	model = UserAccount
	template_name = 'users/register.html'

	def get(self, request):
		context = {}
		context['status'] = 100
		
		if str(request.user) != "AnonymousUser":
			return redirect(reverse('main:home'))

		return render(request, self.template_name, context)

	def post(self, request):
		context = {}
		form_data = self.form(request.POST)

		if form_data.is_valid():
			email = form_data.cleaned_data['email']
			username = form_data.cleaned_data['username']
			user_account = UserAccount.objects.filter(email=email, username=username).first()
			
			if user_account:
				context['status'] = 400
				context['message'] = "Ya existe una cuenta registrada con este email/username"
			else:
				password = form_data.cleaned_data['password']
				password_confirm = form_data.cleaned_data['password_confirm']

				if not password == password_confirm:
					context['status'] = 400
					context['message'] = "Las contraseñas ingresadas no coinciden"
				else:
					account = UserAccount()
					account.email = email
					account.username = username
					account.first_name = form_data.cleaned_data['first_name']
					account.last_name = form_data.cleaned_data['last_name']
					account.password = make_password(password)
					account.user_type = UserAccount.SUBSCRIPTION
					account.save()

					# Setear plan FREE por defecto
					plan = Plan.objects.filter(name='FREE').first()
					if not plan:
						plan = Plan(name='FREE')
						plan.save()
						plan.reload()
						
					account.subscriptions.add(plan)

					context['status'] = 201
					context['message'] = "Registro exitoso, inicie sesión para continuar"

					return render(request, LoginView.template_name, context)

		else:
			context['status'] = 400
			context['message'] = "Revisa los datos ingresados e intentalo nuevamente"

		return render(request, self.template_name, context)


class ForgotPasswordView(View):

	template_name = 'users/forgot-password.html'
	form = ForgotPasswordForm

	def get(self, request):
		context = {}
		return render(request, self.template_name, context)

	def post(self, request):
		context = {}

		try:
			form = self.form(request.POST)

			if form.is_valid():
				form = form.cleaned_data
				username = form['username']
				password = form['password']
				password_confirm = form['password_confirm']

				user = UserAccount.objects.get(username=username)

				if password == password_confirm:
					user.password = make_password(password)
					user.save()

					context['status'] = 200
					context['message'] = "La contraseña ha sido actualizada"

				else:
					context['status'] = 400
					context['message'] = "Las contraseñas ingresadas no son iguales"

			else:
				context['status'] = 400
				context['message'] = "Revise los datos ingresados e intentelo nuevamente"

		except ObjectDoesNotExist:
			context['status'] = 404
			context['message'] = "No existe un usuario con ese correo"

		except Exception as e:
			context['status'] = 500
			context['message'] = f"Error interno del servidor"

		return render(request, self.template_name, context)


class AccountsView(LoginRequiredMixin, View):

	template_name = "users/index.html"


	def get(self, request):
		context = {}
		account = request.user

		try:
			users = UserAccount.objects.filter()
			context['users'] = users
			context['message'] = "Todos los usuarios"
		except:
			context['users'] = []
			context['message'] = "Error"

		return render(request, self.template_name, context)