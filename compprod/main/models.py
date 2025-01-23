from django.contrib.auth import get_user_model
from django.db import models


# Модель для списка товаров
class Product(models.Model):
    name = models.CharField('Имя', max_length=255)
    description = models.TextField('Описание')
    photo = models.ImageField('Фото', upload_to='')
    category = models.ForeignKey('main.Category', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey('main.Manufacturer', on_delete=models.CASCADE)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.manufacturer.name} {self.name}"

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):
    name = models.CharField('Имя', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Attribute(models.Model):
    name = models.CharField('Имя', max_length=255)
    data_type = models.ForeignKey('main.AttributeType', on_delete=models.CASCADE)
    category = models.ForeignKey('main.Category', on_delete=models.CASCADE)
    unit_of_measurement = models.CharField('Единица измерения', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class ProductAttributeValue(models.Model):
    product = models.ForeignKey('main.Product', on_delete=models.CASCADE, verbose_name='Товар')
    attribute = models.ForeignKey('main.Attribute', on_delete=models.CASCADE, verbose_name='Характеристика')
    value = models.CharField('Значение', max_length=255)  # Значение характеристики

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}"

    class Meta:
        verbose_name = 'Значение характеристики'
        verbose_name_plural = 'Значения характеристик'

class Manufacturer(models.Model):
    name = models.CharField('Название', max_length=255)
    country = models.CharField('Страна', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

class AttributeType(models.Model):
    name = models.CharField('Имя', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип данных характеристик'
        verbose_name_plural = 'Типы данных характеристик'

class Favorites(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.product.name}"

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

class Question(models.Model):
    text = models.CharField('Текст вопроса', max_length=255)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField('Текст ответа', max_length=255)

    def __str__(self):
        return f"{self.question.text} - {self.text}"

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

