from app1.models import Heart
from django import forms
# form CRUD
class HeartForm(forms.ModelForm):
    class Meta:
        model = Heart
        fields = "__all__"
