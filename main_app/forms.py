from django.forms import ModelForm
from .models import Listens

class ListensForm(ModelForm):
  class Meta:
    model = Listens
    fields = ['date', 'rating']

