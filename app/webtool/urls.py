from django.conf.urls import url

from . import views


app_name = 'webtool'
urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^confusion_matrix/', views.return_all_data),
]