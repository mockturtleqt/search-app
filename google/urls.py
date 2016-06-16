from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    #url(r'add_url/', 'google.views.add_url', name='add_url'),
    url(r'search/', views.search, name='search'),
    url(r'urls/', views.get_all_urls, name='urls'),
    url(r'add_to_index/', views.index_page, name='index a page'),


]