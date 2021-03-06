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
    url(r'^apt-rentals/', include('clickgestion.apt_rentals.urls')),
    url(r'^concepts/', include('clickgestion.concepts.urls')),
    url(r'^cash-desk/', include('clickgestion.cash_desk.urls')),
    url(r'^deposits/', include('clickgestion.deposits.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^parking-rentals/', include('clickgestion.parking_rentals.urls')),
    url(r'^refunds/', include('clickgestion.refunds.urls')),
    url(r'^safe-rentals/', include('clickgestion.safe_rentals.urls')),
    url(r'^service-sales/', include('clickgestion.service_sales.urls')),
    url(r'^ticket-sales/', include('clickgestion.ticket_sales.urls')),
    url(r'^transactions/', include('clickgestion.transactions.urls')),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))


handler400 = 'clickgestion.core.views.badrequest'
handler403 = 'clickgestion.core.views.forbidden'
handler404 = 'clickgestion.core.views.notfound'
handler500 = 'clickgestion.core.views.servererror'

