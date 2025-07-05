from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser, OTP
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    OTPVerificationForm,
    PasswordResetRequestForm,
    PasswordResetForm, ProfileForm
)


class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Check if user already exists but not verified
            user = CustomUser.objects.filter(email=email).first()
            if user and user.is_verified:
                messages.error(request, 'Email already registered and verified.')
                return render(request, self.template_name, {'form': form})

            if not user:
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    is_verified=False
                )

            # Generate and save OTP
            otp_code = OTP.generate_otp()
            OTP.objects.filter(user=user).delete()  # Remove any existing OTPs
            OTP.objects.create(user=user, otp=otp_code)

            # Send OTP email
            send_mail(
                'Verify your email for JobFinder',
                f'Your OTP code is: {otp_code}',
                'noreply@jobfinder.com',
                [email],
                fail_silently=False,
            )

            request.session['email_for_verification'] = email
            return redirect('verify_otp')

        return render(request, self.template_name, {'form': form})


class VerifyOTPView(View):
    template_name = 'accounts/verify_otp.html'
    form_class = OTPVerificationForm

    def get(self, request):
        if 'email_for_verification' not in request.session:
            return redirect('register')

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            email = request.session.get('email_for_verification')

            if not email:
                messages.error(request, 'Session expired. Please register again.')
                return redirect('register')

            user = CustomUser.objects.filter(email=email).first()
            if not user:
                messages.error(request, 'User not found. Please register again.')
                return redirect('register')

            otp_obj = OTP.objects.filter(user=user, otp=otp_code).first()

            if otp_obj and otp_obj.is_valid():
                user.is_verified = True
                user.save()
                otp_obj.delete()
                del request.session['email_for_verification']

                login(request, user)
                messages.success(request, 'Email verified successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid or expired OTP.')

        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            try:
                user = form.get_user()
                auth_login(request, user)
                return redirect('home')
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('verify_otp')

        # Forma valid emas yoki autentifikatsiya muvaffaqiyatsiz
        messages.error(request, 'Invalid email or password')
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('home')


class PasswordResetRequestView(View):
    template_name = 'accounts/password_reset_request.html'
    form_class = PasswordResetRequestForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email, is_verified=True).first()

            if user:
                # Generate and save OTP
                otp_code = OTP.generate_otp()
                OTP.objects.filter(user=user).delete()  # Remove any existing OTPs
                OTP.objects.create(user=user, otp=otp_code)

                # Send OTP email
                send_mail(
                    'Password Reset OTP',
                    f'Your password reset OTP is: {otp_code}',
                    'noreply@jobfinder.com',
                    [email],
                    fail_silently=False,
                )

                request.session['email_for_password_reset'] = email
                return redirect('password_reset')
            else:
                messages.error(request, 'No verified user found with this email.')

        return render(request, self.template_name, {'form': form})


class PasswordResetView(View):
    template_name = 'accounts/password_reset.html'
    form_class = PasswordResetForm

    def get(self, request):
        if 'email_for_password_reset' not in request.session:
            return redirect('password_reset_request')

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password1']
            email = request.session.get('email_for_password_reset')

            if not email:
                messages.error(request, 'Session expired. Please try again.')
                return redirect('password_reset_request')

            user = CustomUser.objects.filter(email=email).first()
            if not user:
                messages.error(request, 'User not found. Please try again.')
                return redirect('password_reset_request')

            otp_obj = OTP.objects.filter(user=user, otp=otp_code).first()

            if otp_obj and otp_obj.is_valid():
                user.set_password(new_password)
                user.save()
                otp_obj.delete()
                del request.session['email_for_password_reset']

                messages.success(request, 'Password reset successfully! You can now login.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid or expired OTP.')

        return render(request, self.template_name, {'form': form})

class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, self.template_name, {'form': form, 'profile': profile})

    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form, 'profile': profile})