
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .views import (ContentUpdateView, ProjectDeleteView, ProjectListView, ProjectDetailView,
                    ProjectCreateView, ProjectUpdateView, DeleteView, AddonsListView, SecurityCreate, ServiceSubscribeListView, StorageChange, StorageCreate, StorageDetail, StorageUpdate, SupportChange, SupportCreate, SupportDetail)

app_name = 'userpanel'

urlpatterns = [
    # Home page
     path('', views.index, name='index'),
     path('list/', views.list, name='list'),
     path('new-project/', views.ProjectCreateView.as_view(), name='newproject'),



     path('projects/', ProjectListView.as_view(), name='project-list'),
     path('service-subsribes/', ServiceSubscribeListView.as_view(), name='service-subs-list'),
     #path('projects/new/', ProjectCreateView.as_view(), name='project-create'),
     path('projects/<str:pk>/', ProjectDetailView.as_view(), name='project-detail'),
     path('projects/<str:pk>/update/',
          ProjectUpdateView.as_view(), name='project-update'),

     path('support/',
          SupportCreate.as_view(), name='support-create'),
     path('support-change/',
          SupportChange.as_view(), name='support-change'),
     path('support/<str:pk>/',
          SupportDetail.as_view(), name='support-details'),

     path('storage/',
          StorageCreate.as_view(), name='storage-create'),
     path('storage-change/',
          StorageChange.as_view(), name='storage-change'),
     path('storage/<str:pk>/',
          StorageDetail.as_view(), name='storage-details'),
     path('security/',
          SecurityCreate.as_view(), name='security-create'),

     path('projects/<str:pk>/delete/',
          ProjectDeleteView.as_view(), name='project-delete'),
     path('start-project/', ProjectCreateView.as_view(), name='project-create'),
     path('projects/<str:pk>/content/',
          ContentUpdateView.as_view(), name='content-update'),
     
    

     path('projects/<str:pk>/addons/',
         AddonsListView.as_view(), name='project-addons'),


    path('projects/<str:project>/menu/', views.create_menu, name='create-menu'),
    path('projects/<pk>/menu', views.detail_menu, name="detail-menu"),
    path('projects/<pk>/menu/update/', views.update_menu, name="update-menu"),
    path('project/<pk>/menu/delete/', views.delete_menu, name="delete-menu"),
    path('project/create-menu-form/',
         login_required(views.create_menu_form), name='create-menu-form'),

#     path('projects/<str:project>/pages/',
#          views.create_pages, name='create-pages'),
#     path('projects/<pk>/pages', views.detail_pages, name="detail-pages"),
#     path('projects/<pk>/pages/update/', views.update_pages, name="update-pages"),
#     path('project/<pk>/pages/delete/', views.delete_pages, name="delete-pages"),
#     path('project/create-pages-form/',
#          login_required(views.create_pages_form), name='create-pages-form'),


    path('blogtest/', views.blogtest, name='blogest'),

    path('picture-upload/', ContentUpdateView.picupload, name="picupload"),
    path('delete-pic/<str:pk>/', ContentUpdateView.deletePic, name="delete-pic")

]
