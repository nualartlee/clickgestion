from clickgestion.concepts import test_views

app = 'parking_rentals'
concept = 'parkingrental'


class ParkingRentalActionViewTest(test_views.ConceptActionsViewTest):

    app = app
    concept = concept


class ParkingRentalNewViewTest(test_views.ConceptNewViewTest):

    app = app
    concept = concept


class ParkingRentalDeleteViewTest(test_views.ConceptDeleteViewTest):

    app = app
    concept = concept


class ParkingRentalDetailViewTest(test_views.ConceptDetailViewTest):

    app = app
    concept = concept


class ParkingRentalEditlViewTest(test_views.ConceptEditViewTest):

    app = app
    concept = concept


class ParkingRentalRowViewTest(test_views.ConceptRowViewTest):

    app = app
    concept = concept

