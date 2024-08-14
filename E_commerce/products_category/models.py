from django.db import models
from django.urls import reverse

# models for products.

class catogary(models.Model):
    catogary_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(max_length=200,blank=True)
    catogary_image = models.ImageField(upload_to='images/catagory')

    def get_url(self):
        return reverse('products_by_catogary',args=[self.slug])

    def __str__(self) -> str:
        return self.catogary_name