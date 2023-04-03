from django.db import models
from django.urls import reverse
from users.models import User
# Create your models here.

class Products(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    photo = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category_mp', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

class Category_mp(models.Model):

    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def __str__(self):
        return self.title



class Goods(models.Model):
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    title = models.CharField(max_length=300, verbose_name='Наименование товара')
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('about_good', kwargs={'slug_cat': self.category.slug, 'slug_good_name': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class Gallery(models.Model):
    image = models.ImageField(upload_to='goods/%Y/%m/%d', blank=True)
    good = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='Изображение', related_name='images')


    def get_absolute_url(self, img=False):
        # current_img = self.image.url.split('/')[-1].split('.')[0]
        current_img = self.image.url.replace('/', '-').replace('.', '_')

        return reverse('current_img', kwargs={
            'slug_cat': self.good.category.slug,
            'slug_good_name': self.good.slug,
            'current_img': current_img,
        })

class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum([basket.sum() for basket in self])

    def total_quantity(self):
        return sum([basket.quantity for basket in self])

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Goods, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f"Корзина для: {self.user.username} | Продукт: {self.product.title}"

    def sum(self):
        return self.product.price * self.quantity


class Orders(models.Model):
    orders_id = models.IntegerField()
    id_of_products = models.CharField(max_length=20)
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_pay_way = models.CharField(max_length=150)
    customer_delivery_way = models.CharField(max_length=150)
    customer_comment_to_order = models.TextField()
    customer_phone_number = models.CharField(max_length=25)
    customer_data_processing = models.CharField(max_length=15)

    def __str__(self):
        return self.orders_id



