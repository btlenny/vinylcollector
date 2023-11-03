from django.db import models
from django.urls import reverse
from datetime import date



# A tuple of 2-tuples
RATINGS = (
    ('B', 'Bad'),
    ('N', 'Neutral'),
    ('G', 'Great')
)

# Create your models here.
class Turntable(models.Model):
  brand = models.CharField(max_length=50)
  model = models.CharField(max_length=50)
 
  
  def __str__(self):
    return self.brand

  def get_absolute_url(self):
    return reverse('turntables_detail', kwargs={'pk': self.id})


class Vinyl(models.Model):
  artist = models.CharField(max_length=100)
  album = models.CharField(max_length=100)
  tracks = models.IntegerField()
  year = models.IntegerField()
 
  turntables = models.ManyToManyField(Turntable)


  def __str__(self):
    return f'{self.artist} ({self.id})'
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'vinyl_id': self.id})
  
  def listened_for_today(self):
    return self.listens_set.filter(date=date.today()).count() >= len(RATINGS)

class Listens(models.Model):
  date = models.DateField('Listens Date')
  rating = models.CharField(
    max_length=1,
    choices=RATINGS,
    default=RATINGS[0][0]
)
  
  vinyl = models.ForeignKey(
    Vinyl, 
    on_delete=models.CASCADE
    )
  
  def __str__(self):
    return f"{self.get_rating_display()} on {self.date}"

  class Meta:
     ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    vinyl = models.ForeignKey(Vinyl, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for vinyl_id: {self.vinyl_id} @{self.url}"