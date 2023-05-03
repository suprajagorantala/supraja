from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name



class Item(models.Model):
    LABELS = (
        ('Best Selling Foods', 'Best Selling Foods'),
        ('New Food', 'New Food'),
        ('Spicy Foods🔥', 'Spicy Foods🔥'),
    )

    LABEL_COLOUR = (
        ('danger', 'danger'),
        ('success', 'success'),
        ('primary', 'primary'),
        ('info', 'info'),
        ('warning', 'warning'),
    )
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=25000, blank=True)
    price = models.FloatField()
    instructions = models.CharField(max_length=25000, default="Available")
    image = models.ImageField(default='default.png', upload_to='images/')
    labels = models.CharField(max_length=25, choices=LABELS, blank=True)
    label_colour = models.CharField(max_length=15, choices=LABEL_COLOUR, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(default="foods")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:dishes", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_item_delete_url(self):
        return reverse("main:item-delete", kwargs={
            'slug': self.slug
        })

    def get_update_item_url(self):
        return reverse("main:item-update", kwargs={
            'slug': self.slug
        })




class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rslug = models.SlugField()
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.review


class CartItems(models.Model):
    ORDER_STATUS = (
        ('Active', 'Active'),
        ('Delivered', 'Delivered')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(default=timezone.now,null=True,blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Active')


    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return self.item.title

    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={
            'pk': self.pk
        })

    def update_status_url(self):
        return reverse("main:update_status", kwargs={
            'pk': self.pk
        })



from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Table(models.Model):
    TABLE_NUMBERS = (
        (1, 'Table 1'),
        (2, 'Table 2'),
        (3, 'Table 3'),
        (4, 'Table 4'),
        (5, 'Table 5'),
        (6, 'Table 6'),
        (7, 'Table 7'),
        (8, 'Table 8'),
        (9, 'Table 9'),
        (10, 'Table 10'),
        (11, 'Table 11'),
        (12, 'Table 12'),
        (13, 'Table 13'),
        (14, 'Table 14'),
        (15, 'Table 15'),
        (16, 'Table 16'),
    )
    TABLE_CAPACITIES = (
        (2, '2'),
        (2, '2'),
        (2, '2'),
        (4, '4'),
        (4, '4'),
        (2, '2'),
        (4, '4'),
        (4, '4'),
        (4, '4'),
        (6, '6'),
        (6, '6'),
        (4, '4'),
        (10, '10'),
        (4, '4'),
        (4, '4'),
        (10, '10'),
    )


    number = models.IntegerField(choices=TABLE_NUMBERS)
    capacity = models.IntegerField(choices=TABLE_CAPACITIES)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.get_number_display()} ({self.capacity} seats)'

    def is_available(self, date, time):
        """Returns True if this table is available at the given date and time."""
        end_time = timezone.datetime.combine(date, time) + timezone.timedelta(hours=1)
        reservations = Reservation.objects.filter(
            table=self,
            date=date,
            time__lt=end_time.time(),
            end_time__gt=time,
        )
        return not reservations.exists()


class Reservation(models.Model):
    TABLE_NUMBERS = (
        (1, 'Table 1'),
        (2, 'Table 2'),
        (3, 'Table 3'),
        (4, 'Table 4'),
        (5, 'Table 5'),
        (6, 'Table 6'),
        (7, 'Table 7'),
        (8, 'Table 8'),
        (9, 'Table 9'),
        (10, 'Table 10'),
        (11, 'Table 11'),
        (12, 'Table 12'),
        (13, 'Table 13'),
        (14, 'Table 14'),
        (15, 'Table 15'),
        (16, 'Table 16'),
    )
    TABLE_CAPACITIES = (
        (2, '2'),
        (2, '2'),
        (2, '2'),
        (4, '4'),
        (4, '4'),
        (2, '2'),
        (4, '4'),
        (4, '4'),
        (4, '4'),
        (6, '6'),
        (6, '6'),
        (4, '4'),
        (10, '10'),
        (4, '4'),
        (4, '4'),
        (10, '10'),
    )
    RESERVATION_TYPES = (
        ('Lunch', 'Lunch'),
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
        ('Private Dinner', 'Private Dinner'),
        ('Wedding', 'Wedding'),
        ('Corporate', 'Corporate'),
        ('Rooftop Dinner', 'Rooftop Dinner'),
        ('Dinner', 'Dinner'),
    )
    TIME_CHOICES = (
        ('11:00', '11:00 AM'),
        ('11:30', '11:30 AM'),
        ('12:00', '12:00 PM'),
        ('12:30', '12:30 PM'),
        ('13:00', '1:00 PM'),
        ('13:30', '1:30 PM'),
        ('18:00', '6:00 PM'),
        ('18:30', '6:30 PM'),
        ('19:00', '7:00 PM'),
        ('19:30', '7:30 PM'),
        ('20:00', '8:00 PM'),
        ('20:30', '8:30 PM'),
        ('21:00', '9:00 PM'),
        ('21:30', '9:30 PM'),
    )

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    guests = models.IntegerField()
    date = models.DateField()
    time = models.CharField(max_length=5, choices=TIME_CHOICES)
    special_requests = models.TextField(blank=True)
    reservation_type = models.CharField(max_length=15, choices=RESERVATION_TYPES)

    def clean(self):
        if self.guests > self.table.capacity:
            raise ValidationError("Number of guests cannot exceed table capacity.")

    def __str__(self):
        return f'{self.name} reserved {self.table.get_number_display()} ({self.table.capacity} seats) for {self.guests} guests ({self.get_reservation_type_display()}) on {self.date} at {self.time}'

    def save(self, *args, **kwargs):
        """Override the save method to set the datetime field."""
        datetime_str = f'{self.date} {self.time}'
        self.datetime = timezone.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        super().save(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)
    comments = models.CharField(max_length=100)
    phone=models.IntegerField(null=True)

    def __str__(self):
        return self.name



