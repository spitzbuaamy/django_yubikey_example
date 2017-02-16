from django.conf.urls import url

from login.views import OneFactorAuthView, SuccessView, LogoutView

urlpatterns = [
    url(r'^one/$', OneFactorAuthView.as_view(), name="OneFactorAuthentication"),
    url(r'^one/success/$', SuccessView.as_view(), name="success"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
]
