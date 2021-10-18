from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category', default='cat.jpg')


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category', default='cat.jpg')
    min_quant = models.IntegerField(default=1)
    max_quant = models.IntegerField()
    latest = models.BooleanField()
    best_seller = models.BooleanField()
    available = models.BooleanField()

    def __str__(self):
        return (self.title)


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    paid_item = models.BooleanField(default=True)
    cart_no = models.CharField(max_length=36)

    def __str__(self):
        return self.user.username