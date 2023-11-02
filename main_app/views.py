import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Vinyl, Turntable
from .forms import ListensForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def vinyls_index(request):
  vinyls = Vinyl.objects.all()
  return render(request, 'vinyls/index.html', {
    'vinyls': vinyls
     })

def vinyls_detail(request, vinyl_id):
  vinyl = Vinyl.objects.get(id=vinyl_id)
  id_list = vinyl.turntables.all().values_list('id')
  turntables_vinyl_doesnt_have = Turntable.objects.exclude(id__in=id_list)
  listens_form = ListensForm()
  return render(request, 'vinyls/detail.html', { 
    'vinyl': vinyl, 'listens_form': listens_form,
    'turntables': turntables_vinyl_doesnt_have
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
  success_url = '/vinyls'

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

class TurntableList(ListView):
  model = Turntable

class TurntableDetail(DetailView):
  model = Turntable

class TurntableCreate(CreateView):
  model = Turntable
  fields = '__all__'

class TurntableUpdate(UpdateView):
  model = Turntable
  fields = ['brand', 'model']

class TurntableDelete(DeleteView):
  model = Turntable
  success_url = '/turntable'

def assoc_turntable(request, vinyl_id, turntable_id):
  # Note that you can pass a toy's id instead of the whole toy object
  Vinyl.objects.get(id=vinyl_id).turntables.add(turntable_id)
  return redirect('detail', vinyl_id=vinyl_id)

def unassoc_turntable(request, vinyl_id, turntable_id):
  Vinyl.objects.get(id=vinyl_id).turntables.remove(turntable_id)
  return redirect('detail', vinyl_id=vinyl_id)

def add_photo(request, vinyl_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, vinyl_id=vinyl_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', vinyl_id=vinyl_id)
 