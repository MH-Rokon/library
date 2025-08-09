from django.contrib import admin
from django.urls import path, include
from .views import home_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('author.urls')), 
    path('library/', include('book.urls')), 
    path('borrow/', include('borrow.urls')), 
     path('', home_view, name='index'),
]
