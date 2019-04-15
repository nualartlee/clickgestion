from clickgestion.concepts import test_views
from django.utils import timezone
from django.shortcuts import reverse

app = 'service_sales'
concept = 'servicesale'


class ServiceSaleActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class ServiceSaleNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept

    def test_post_service_change(self):
        form_data = {
            'type': self.service.servicetype.id,
            'service': self.service.id,
            'adults': 2,
            'children': 0,
            'seniors': 0,
            'start_date': '{}'.format(timezone.now().date()),
            'end_date': '{}'.format(timezone.now().date() - timezone.timedelta(days=1)),
        }
        self.log_admin_in()
        response = self.client.post(
            reverse(self.url, kwargs=self.kwargs),
            form_data,
            follow=True, HTTP_REFERER='/',
        )


class ServiceSaleDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class ServiceSaleDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class ServiceSaleEditlViewTest(test_views.ConceptEditViewTest):

    app = app
    concept = concept


class ServiceSaleRowViewTest(test_views.ConceptRowViewTest):

    app = app
    concept = concept

