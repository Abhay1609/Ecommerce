from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from account.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    def get_absolute_urls(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price=models.DecimalField(max_digits=6,decimal_places=4)
    image=models.ImageField(upload_to='uploads/',blank=True,null=True)
    thumbnail=models.ImageField(upload_to='uploads/',blank=True, null=True)
    date_added=models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name
    def get_absolute_urls(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
     if self.image:
        return 'http://127.0.0.1:8000' +self.image.url
     return ''
    def get_thumbnail(self):
     if self.thumbnail:
        return 'http://127.0.0.1:8000' +self.thumbnail.url
     else:
         if self.image:
             self.thumbnail=self.make_thumbnail(self.image)
             self.save()
             return 'http://127.0.0.1:8000'+self.thumbnail.url
         else:
             return ''
    def make_thumbnail(self, image,size=(300,200)):
        img=Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io=BytesIO()
        img.save(thumb_io,'JPEG',quality=85)
        thumbnail = File(thumb_io,name=image.name)
        return thumbnail
    @classmethod
    def updateprice(cls,product_id,price):
        product=cls.objects.filter(product_id=product_id)
        product=product.first()
        product.price=price
        product.save()
        return product
    @classmethod
    def create(cls,name,price):
        product=Product(name=name,price=price)
        product.save()
        return product
class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        u = str(self.user)
        return f"Cart (User: {u})"


class ProductInCart(models.Model):
    class Meta:
        unique_together = (('cart_id', 'name'),)

    product_in_cart_id=models.AutoField(primary_key=True)
    cart_id=models.ForeignKey(Cart,on_delete=models.CASCADE)
    name=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()

    def __str__(self):
        product=str(self.name)
        return f"Cart (Product: {product})"

class Order(models.Model):
    status_choices=(
        (1,'Not Packed'),
        (2,'Ready For Shipment'),
        (3,'Shipped'),
        (4,'Delivered')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.IntegerField(choices=status_choices,default=1)



