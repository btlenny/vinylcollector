from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Vinyl
from .forms import ListensForm


# vinyl = [
#   {'artist': 'Beach House', 'album': 'Bloom', 'tracks': 10, 'released': 2012},
#   {'artist': 'Alvvays', 'album': 'Blue Rev', 'tracks': 14, 'released': 2022},
#   {'artist': 'M83', 'album': 'Hurry Up, Were Dreaming', 'tracks': 22, 'released': 2011},
# ]
# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def vinyl_index(request):
  vinyl = Vinyl.objects.all()
  return render(request, 'vinyl/index.html', {
    'vinyl': vinyl
     })

def vinyl_detail(request, vinyl_id):
  vinyl = Vinyl.objects.get(id=vinyl_id)

  listens_form = ListensForm()
  return render(request, 'vinyl/detail.html', { 
    'vinyl': vinyl, 'listens_form': listens_form,
    })

class VinylCreate(CreateView):
  model = Vinyl
  fields = '__all__'

class VinylUpdate(UpdateView):
  model = Vinyl
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['artist', 'album', 'tracks', 'year']

class VinylDelete(DeleteView):
  model = Vinyl
  success_url = '/vinyl'

def add_listens(request, vinyl_id):
  # create a ModelForm instance using 
  # the data that was submitted in the form
  form = ListensForm(request.POST)
  # validate the form
  if form.is_valid():
    # We want a model instance, but
    # we can't save to the db yet
    # because we have not assigned the
    # cat_id FK.
    new_listens = form.save(commit=False)
    new_listens.vinyl_id = vinyl_id
    new_listens.save()
  return redirect('detail', vinyl_id=vinyl_id)

 