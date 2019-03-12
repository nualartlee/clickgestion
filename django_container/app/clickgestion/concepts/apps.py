from django.apps import AppConfig
from django.utils.translation import gettext_lazy


class ConceptsConfig(AppConfig):
    name = 'clickgestion.concepts'
    verbose_name = gettext_lazy('Concepts')

