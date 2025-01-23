from django.contrib import admin
from .models import Product, Category, Attribute, ProductAttributeValue, Manufacturer, AttributeType, Favorites, Question, AnswerOption

# Регистрация модели Product
admin.site.register(Product)

# Регистрация модели Category
admin.site.register(Category)

# Регистрация модели Attribute
admin.site.register(Attribute)

# Регистрация модели ProductAttributeValue
admin.site.register(ProductAttributeValue)

admin.site.register(Manufacturer)

admin.site.register(AttributeType)

admin.site.register(Favorites)

admin.site.register(Question)

admin.site.register(AnswerOption)
