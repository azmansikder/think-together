from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as acc_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('student/', include('studentpanel.urls', namespace='studentpanel')),
    path('research/', include('researchpanel.urls', namespace='researchpanel')),
    path('', acc_views.signup_view, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
