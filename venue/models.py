from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Venue(models.Model):

    TYPE_CHOICES = [
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    ]

    owner = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name='venues', 
                              limit_choices_to={'role': 'OWNER'})
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    address = models.TextField()
    description = models.TextField()
    image_url = models.URLField(max_length=1024)

    def __str__(self):
        return self.name
