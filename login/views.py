from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView
from django.views.generic import FormView

# Quelle: https://coderwall.com/p/sll1kw/django-auth-class-based-views-login-and-logout
from django.views.generic import RedirectView
from django.views.generic import TemplateView


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = "login.html"
    success_url = "success"


class OneFactorAuthView(FormView):
    success_url = "success"
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "login.html"

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(OneFactorAuthView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(OneFactorAuthView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('OneFactorAuthentication')

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class SuccessView(TemplateView):
    template_name = 'landing_page.html'


class RegisterSuccessView(TemplateView):
    template_name = 'register_sucess.html'