from django.conf.urls import url

from . import views

app_name = 'analysis'
urlpatterns = [
  # route to app root
  url(r'^$', views.index, name='index'),

  # route to each API
  url(r'^confusion_matrix/', views.confusion_matrix),
  url(r'^feature_importance/', views.feature_importance),
  url(r'^pca_variance/', views.pca_variance),
  url(r'^pca_scatter/', views.pca_scatter),
  url(r'^pca_3d/', views.pca_3d),
]