from clickgestion.concepts import test_views

app = 'safe_rentals'
concept = 'saferental'


class SafeRentalActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class SafeRentalNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept


class SafeRentalDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class SafeRentalDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class SafeRentalEditlViewTest(test_views.ConceptEditViewTest):

    app = app
    concept = concept


class SafeRentalRowViewTest(test_views.ConceptRowViewTest):

    app = app
    concept = concept

