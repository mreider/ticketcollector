from django.forms import ModelForm
from .models import Collection

class CollectionCreateForm(ModelForm):
    class Meta:
        model = Collection
        fields = ['name']