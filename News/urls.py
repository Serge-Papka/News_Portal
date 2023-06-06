
from django.contrib import admin
from django.urls import path, include
from News_Portal.views import upgrade_me, downgrade_me



urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('News_Portal.urls')),
    # path('', RedirectView.as_view(url='/about/'), name='about'),
    path('', include('News_Portal.protect_urls')),
    path('article/', include('News_Portal.article_urls')),
    path('accounts/', include('allauth.urls')),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('downgrade/', downgrade_me, name='downgrade'),
]
