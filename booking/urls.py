from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.api.urls', namespace='accounts')),
    path('api/v1/flight/', include('flight.api.urls', namespace='flight')),
    path('api/v1/basket/', include('basket.api.urls', namespace='basket')),
    path('api/v1/payment/', include('payment.api.urls', namespace='payment')),
]
