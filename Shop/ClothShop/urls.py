from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from ClothShop import views
from ClothShop.views import edit_product

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register_view'),
    path('create_product/', views.create_product, name='create_product'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_comment/<int:product_id>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

