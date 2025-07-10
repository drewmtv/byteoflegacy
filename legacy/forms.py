from django import forms
from .models import Slot

class SlotForm(forms.ModelForm):
    icon = forms.CharField(widget=forms.HiddenInput(), required=False)
    payment_proof = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Slot
        fields = [
            'slot_number',
            'name',
            'icon',
            'front_bg_color',
            'front_text_color',
            'message',
            'link',
            'back_bg_color',
            'back_text_color',
            'payment_proof',
            'email',
            'payment_amount'
        ]

        widgets = {
            'slot_number': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 1,
                'max': 20000,
                'readonly': 'readonly'
                }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name here...',
                'maxlength': '40'
            }),
            'front_bg_color': forms.TextInput(attrs={
                'type': 'color', 
                'class': 'form-control form-control-color',
                'onchange': 'colorBackgroundChange(this.value, document.getElementById("front_card"), document.getElementById("front-bg-gauge"))',
                'oninput': 'colorBackgroundChange(this.value, document.getElementById("front_card"), document.getElementById("front-bg-gauge"))'
                }),
            'front_text_color': forms.TextInput(attrs={
                'type': 'color', 
                'class': 'form-control form-control-color',
                'onchange': 'colorTextChange(this.value, document.getElementById("id_name"), document.getElementById("front-text-gauge"))',
                'oninput': 'colorTextChange(this.value, document.getElementById("id_name"), document.getElementById("front-text-gauge"))'
                }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'maxlength': '150', 
                'placeholder': 'Enter your legacy message (max 150 characters)'
                }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '(Optional): Your link...'
                }),
            'back_bg_color': forms.TextInput(attrs={
                'type': 'color', 
                'class': 'form-control form-control-color',
                'onchange': 'colorBackgroundChange(this.value, document.getElementById("back_card"), document.getElementById("back-bg-gauge"))',
                'oninput': 'colorBackgroundChange(this.value, document.getElementById("back_card"), document.getElementById("back-bg-gauge"))'
                }),
            'back_text_color': forms.TextInput(attrs={
                'type': 'color', 
                'class': 'form-control form-control-color',
                'onchange': 'colorTextChange(this.value, document.getElementById("id_name"), document.getElementById("front-text-gauge"))',
                'oninput': 'colorTextChange(this.value, document.getElementById("id_message"), document.getElementById("back-text-gauge"))'
                }),
            'payment_amount': forms.HiddenInput()
        }
