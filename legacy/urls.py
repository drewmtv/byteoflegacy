from django.urls import path

from . import views

app_name = "legacy"

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name='about'),
    path('slots/chunk/', views.slot_chunk_view, name='slot_chunk'),
    path('claim/', views.claim_byte, name='claim'),
    path('claim/<int:slot>', views.claim_byte, name='claim'),
    path('success/', views.claim_success, name='success')
]