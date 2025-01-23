from django.urls import path, include
from django.conf.urls.static import static
from . import views
from .views import product_list, product_detail, index
from django.contrib.auth import views as auth_views

from compprod import settings

urlpatterns = [
    path('', index, name='index'),
    path('products/', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('products/<int:product_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites/remove/<int:favorite_id>/', views.remove_favorite, name='remove_favorite'),
    path('expert_system/', views.expert_system, name='expert_system'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
