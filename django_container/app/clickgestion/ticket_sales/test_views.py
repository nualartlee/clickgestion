from clickgestion.concepts import test_views

app = 'ticket_sales'
concept = 'ticketsale'


class TicketSaleActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class TicketSaleNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept


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

