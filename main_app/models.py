from django.db import models
from django.urls import reverse

# A tuple of 2-tuples
RATINGS = (
    ('B', 'Bad'),
    ('N', 'Neutral'),
    ('G', 'Great')
)

# Create your models here.
class Vinyl(models.Model):
  artist = models.CharField(max_length=100)
  album = models.CharField(max_length=100)
  tracks = models.IntegerField()
  year = models.IntegerField()

  def __str__(self):
    return f'{self.artist} ({self.id})'
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'vinyl_id': self.id})

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

  # Changing this instance method
  # does not impact the database, therefore
  # no makemigrations is necessary
