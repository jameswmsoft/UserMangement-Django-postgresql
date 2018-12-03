from django.urls import path

from polls.views import views
from polls.views import admin_views

urlpatterns = [
    path('', views.index, name='index'),

    path('admin/', admin_views.index, name='adminIndex'),
    path('admin/login', admin_views.adminLogin, name='adminLogin'),
    path('admin/Logout', admin_views.adminLogout, name='adminLogout'),
    path('admin/customer/', admin_views.customerIndex, name='customer'),
    path('admin/customer/edit/<int:user_id>', admin_views.customerEdit, name='customerEdit'),
    path('admin/customer/<int:user_id>', admin_views.customerEditPage, name='customerEditPage'),
    path('admin/adminUser/<int:admin_id>/', admin_views.adminUserIndex, name='adminUser'),
    path('admin/adminEdit/', admin_views.adminUserEdit, name='editAdmin'),
    path('admin/index/ajaxTable/', admin_views.AjaxTable, name='ajaxTable'),
    path('admin/index/addNew/', admin_views.addNew, name='add_new'),
    path('admin/index/addUser/', admin_views.addUser, name='addUser'),
    path('admin/index/userDel/', admin_views.UserDelete, name='userDelete'),
    path('admin/index/status/', admin_views.UserStatus, name='userStatus'),

    path('admin/User/', admin_views.GUserIndex, name='GUser'),
]