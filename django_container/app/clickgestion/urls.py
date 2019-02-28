"""clickgestion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings

urlpatterns = [
    url(r'^', include('clickgestion.core.urls')),
    url(r'^transactions/', include('clickgestion.transactions.urls')),
    url(r'^apt-rentals/', include('clickgestion.apt_rentals.urls')),
    url(r'^cash-desk/', include('clickgestion.cash_desk.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))


handler400 = 'clickgestion.core.views.badrequest'
handler403 = 'clickgestion.core.views.forbidden'
handler404 = 'clickgestion.core.views.notfound'
handler500 = 'clickgestion.core.views.servererror'

