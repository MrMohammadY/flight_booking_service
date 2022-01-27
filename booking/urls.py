from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="FT Booking",
        default_version='v1',
        description="FT Booking(Flight Ticket Booking) is a platform for flight ticket booking.",
        contact=openapi.Contact(email="mehdy.work@gmail.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.api.urls', namespace='accounts')),
    path('api/v1/flight/', include('flight.api.urls', namespace='flight')),
    path('api/v1/basket/', include('basket.api.urls', namespace='basket')),
    path('api/v1/payment/', include('payment.api.urls', namespace='payment')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
