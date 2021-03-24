from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from flowcode import views

app_name = 'flow'

urlpatterns = [
    path('', views.index, name='index'),
    path('flow/', views.get_flowchart, name='flow'),
    path('yt/', views.yt, name='yt'),
    path('viz/', views.viz, name='viz'),
    path('stock/', views.stock, name="stock")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
