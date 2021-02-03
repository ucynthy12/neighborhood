from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('account/',include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('accounts/register/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), {"next_page": '/'}),
    path('profile/<username>/', views.profile, name='profile'),
    path('hood/<hood_id>', views.hood, name='hood'),
    path('all/',views.all_hoods,name='all'),
    path('join/<hood_id>', views.join, name='join'),
    path('leave/<hood_id>', views.leave, name='leave'),
    path('upload_business/<hood_id>', views.upload_business, name='upload_busines'),
    path('post/<hood_id>', views.add_post, name='post'),
    path('search/', views.search_results, name='search_results'),

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)