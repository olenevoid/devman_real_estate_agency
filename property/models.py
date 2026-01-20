from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Flat(models.Model):
    new_building = models.BooleanField(
        'Новостройка',
        null=True,
        default=False,
        db_index=True
    )
    created_at = models.DateTimeField(
        'Когда создано объявление',
        default=timezone.now,
        db_index=True)

    description = models.TextField('Текст объявления', blank=True)
    price = models.IntegerField('Цена квартиры', db_index=True)

    town = models.CharField(
        'Город, где находится квартира',
        max_length=50,
        db_index=True)
    town_district = models.CharField(
        'Район города, где находится квартира',
        max_length=50,
        blank=True,
        help_text='Чертаново Южное')
    address = models.TextField(
        'Адрес квартиры',
        help_text='ул. Подольских курсантов д.5 кв.4')
    floor = models.CharField(
        'Этаж',
        max_length=3,
        help_text='Первый этаж, последний этаж, пятый этаж')

    rooms_number = models.IntegerField(
        'Количество комнат в квартире',
        db_index=True)
    living_area = models.IntegerField(
        'количество жилых кв.метров',
        null=True,
        blank=True,
        db_index=True)

    has_balcony = models.BooleanField(
        'Наличие балкона',
        null=True,
        blank=True,
        db_index=True
    )
    active = models.BooleanField('Активно-ли объявление', db_index=True)
    likes = models.ManyToManyField(
        User,
        verbose_name='Кто лайкнул',
        related_name='flats'
    )
    construction_year = models.IntegerField(
        'Год постройки здания',
        null=True,
        blank=True,
        db_index=True)

    def __str__(self):
        return f'{self.town}, {self.address} ({self.price}р.)'


class Complain(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Автор жалобы',
        on_delete=models.CASCADE,
        related_name='complaints'
    )
    flat = models.ForeignKey(
        Flat,
        verbose_name='Квартира',
        on_delete=models.CASCADE,
        related_name='complaints'
    )
    text = models.TextField(verbose_name='Текст жалобы')

    def __str__(self):
        return f'{self.user.username}, {self.flat.town}, {self.flat.address}'


class Owner(models.Model):
    name = models.CharField('ФИО владельца', max_length=200)
    phonenumber = models.CharField('Номер владельца', max_length=20)
    pure_phonenumber = PhoneNumberField(
        verbose_name='Нормализованный номер владельца',
        blank=True,
        null=True
    )
    flats = models.ManyToManyField(
        Flat,
        verbose_name='Квартиры в собственности',
        related_name='owned_by'
    )

    def __str__(self):
        phone = self.pure_phonenumber
        return f'{self.name}, {phone}, квартир: {self.flats.count()}'