from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser

from .forms import CustomUserCreationForm
from django.shortcuts import render
from django.contrib.auth import login

from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str # force_text on older versions of Django

from .forms import token_generator

# class SignUp(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy("check-email")
#     template_name = "registration/signup.html"


class Dashboard(generic.ListView):
    context_object_name = 'custom_users'
    queryset = CustomUser.objects.all()
    template_name = "home.html"


class SettingsPage(generic.ListView):
    context_object_name = 'settings'
    queryset = CustomUser.objects.all()
    template_name = "users/settings.html"

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm 
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('check-email')

    def form_valid(self, form):
        to_return = super().form_valid(form)
        
        user = form.save()
        print(user)
        user.is_active = False # Turns the user status to inactive
        user.save()

        form.send_activation_email(self.request, user)

        return to_return
    

class ActivateView(generic.RedirectView):

    url = reverse_lazy('success')

    # Custom get method
    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request, 'users/activate_account_invalid.html')
        

class CheckEmailView(generic.TemplateView, generic.RedirectView):
    template_name = 'users/email-activation.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = '/'
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


class SuccessView(generic.TemplateView, generic.RedirectView):
    template_name = 'users/email-activation-success.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = '/'
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)
