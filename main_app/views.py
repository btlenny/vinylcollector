import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Vinyl, Turntable, Photo
from .forms import ListensForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def vinyls_index(request):
  vinyls = Vinyl.objects.filter(user=request.user)
  return render(request, 'vinyls/index.html', {
    'vinyls': vinyls
     })

@login_required
def vinyls_detail(request, vinyl_id):
  vinyl = Vinyl.objects.get(id=vinyl_id)
  id_list = vinyl.turntables.all().values_list('id')
  turntables_vinyl_doesnt_have = Turntable.objects.exclude(id__in=id_list)
  listens_form = ListensForm()
  return render(request, 'vinyls/detail.html', { 
    'vinyl': vinyl, 'listens_form': listens_form,
    'turntables': turntables_vinyl_doesnt_have
    })

class VinylCreate(LoginRequiredMixin, CreateView):
  model = Vinyl
  fields = ['artist', 'album', 'tracks', 'year']
  
   # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class VinylUpdate(UpdateView):
  model = Vinyl
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['artist', 'album', 'tracks', 'year']
  
class VinylDelete(DeleteView):
  model = Vinyl
  success_url = '/vinyls'

@login_required
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

@login_required
def assoc_turntable(request, vinyl_id, turntable_id):
  # Note that you can pass a toy's id instead of the whole toy object
  Vinyl.objects.get(id=vinyl_id).turntables.add(turntable_id)
  return redirect('detail', vinyl_id=vinyl_id)

@login_required
def unassoc_turntable(request, vinyl_id, turntable_id):
  Vinyl.objects.get(id=vinyl_id).turntables.remove(turntable_id)
  return redirect('detail', vinyl_id=vinyl_id)

@login_required
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
 
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)