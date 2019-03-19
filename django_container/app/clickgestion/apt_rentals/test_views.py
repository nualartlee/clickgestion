from clickgestion.concepts import test_views

app = 'apt_rentals'
concept = 'aptrental'


class AptRentalActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class AptRentalNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept


class AptRentalDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class AptRentalDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class AptRentalEditlViewTest(test_views.ConceptEditlViewTest):

    app = app
    concept = concept

