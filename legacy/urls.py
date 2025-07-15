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
    path('<int:slot>/', views.claim_byte, name="index"),
    path('card-info/<int:slot>/<str:name>/', views.card_info_link, name="card-info-link"),
    path('card-info/<int:slot>/', views.card_info_link, name="card-info-link"),
    path('about/', views.about, name='about'),
    path('slots/chunk/', views.slot_chunk_view, name='slot_chunk'),
    path('claim/', views.claim_byte, name='claim'),
    path('claim/<int:slot>/', views.claim_byte, name='claim'),
    path('success/', views.claim_success, name='success'),
    path('mobile-admin/', views.mobile_admin, name='mobile-admin-login'),
    path('mobile-admin/dashboard/', views.mobile_admin_dashboard, name='mobile-admin-dashboard'),
    path('mobile-admin/logout/', views.mobile_admin_logout, name='mobile-admin-logout'),
    path('ajax/get-updated-slots/', views.get_updated_slots, name='get_updated_slots'),
    path('update-admin-remarks/', views.update_admin_remarks, name='update_admin_remarks'),
    path('admin/proof/<path:image_path>/', views.fetch_proof_image, name='fetch_proof_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)