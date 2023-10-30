from django.shortcuts import render

vinyl = [
  {'artist': 'Beach House', 'album': 'Bloom', 'tracks': 10, 'released': 2012},
  {'artist': 'Alvvays', 'album': 'Blue Rev', 'tracks': 14, 'released': 2022},
  {'artist': 'M83', 'album': 'Hurry Up, Were Dreaming', 'tracks': 22, 'released': 2011},
]
# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def vinyl_index(request):
  return render(request, 'vinyl/index.html', {
    'vinyl': vinyl
  })