from django.conf.urls import url

from . import views

app_name = 'analysis'
urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^confusion_matrix/', views.confusion_matrix),
  url(r'^feature_importance/', views.feature_importance),
  url(r'^pca_variance/', views.pca_variance)
]