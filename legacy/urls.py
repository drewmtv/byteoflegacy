from django.urls import path
from django.http import HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static

from . import views

# Set handler404 at the module level (Django will use this for all 404 errors)
handler404 = 'legacy.views.page_not_found'

app_name = "legacy"

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name='about'),
    path('slots/chunk/', views.slot_chunk_view, name='slot_chunk'),
    path('claim/', views.claim_byte, name='claim'),
    path('claim/<int:slot>/', views.claim_byte, name='claim'),
    path('success/', views.claim_success, name='success'),
    # path('404/', page_not_found),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)