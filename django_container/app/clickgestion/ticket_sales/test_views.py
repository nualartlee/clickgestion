from clickgestion.concepts import test_views
from django.utils import timezone
from django.shortcuts import reverse

app = 'ticket_sales'
concept = 'ticketsale'


class TicketSaleActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class TicketSaleNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept

    def test_post_show_change(self):
        form_data = {
            'show': self.show.id,
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


class TicketSaleDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class TicketSaleDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class TicketSaleEditlViewTest(test_views.ConceptEditViewTest):

    app = app
    concept = concept


class TicketSaleRowViewTest(test_views.ConceptRowViewTest):

    app = app
    concept = concept

