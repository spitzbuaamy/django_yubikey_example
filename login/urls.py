from django.conf.urls import url

from login.views import OneFactorAuthView, SuccessView, LogoutView, RegistrationView, RegisterSuccessView

urlpatterns = [
    url(r'^one/$', OneFactorAuthView.as_view(), name="OneFactorAuthentication"),
    url(r'^one/success/$', SuccessView.as_view(), name="success"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegistrationView.as_view(), name="register"),
    url(r'^register/success$', RegisterSuccessView.as_view(), name="register_success"),
]
