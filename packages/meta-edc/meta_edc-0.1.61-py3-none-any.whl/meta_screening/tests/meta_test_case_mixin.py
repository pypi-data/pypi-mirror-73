from dateutil.relativedelta import relativedelta
from django.contrib.sites.models import Site
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.models import Appointment
from edc_auth.group_permissions_updater import GroupPermissionsUpdater
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from edc_facility.models import Holiday
from edc_list_data.site_list_data import site_list_data
from edc_randomization.models.randomization_list import RandomizationList
from edc_randomization.randomization_list_importer import RandomizationListImporter
from edc_sites import get_sites_by_country, add_or_update_django_sites
from edc_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_utils.date import get_utcnow
from edc_visit_tracking.constants import SCHEDULED
from meta_auth.codenames_by_group import get_codenames_by_group
from meta_sites import fqdn
from meta_subject.models import SubjectVisit
from meta_visit_schedule.constants import DAY1
from model_bakery import baker

from ..models import (
    ScreeningPartOne,
    ScreeningPartTwo,
    ScreeningPartThree,
    SubjectScreening,
)
from .options import (
    part_one_eligible_options,
    part_two_eligible_options,
    part_three_eligible_options,
)


class MetaTestCaseMixin(SiteTestCaseMixin):

    fqdn = fqdn

    default_sites = get_sites_by_country("tanzania")

    site_names = [s.name for s in default_sites]

    import_randomization_list = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        add_or_update_django_sites(sites=get_sites_by_country("tanzania"))
        if cls.import_randomization_list:
            RandomizationListImporter(name="default", verbose=False)
        import_holidays(test=True)
        site_list_data.autodiscover()
        GroupPermissionsUpdater(
            codenames_by_group=get_codenames_by_group(), verbose=True
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        RandomizationList.objects.all().delete()
        Holiday.objects.all().delete()

    def get_subject_screening(self, report_datetime=None, eligibility_datetime=None):
        if report_datetime:
            part_one_eligible_options.update(report_datetime=report_datetime)

        part_one = ScreeningPartOne.objects.create(
            user_created="erikvw", user_modified="erikvw", **part_one_eligible_options
        )
        screening_identifier = part_one.screening_identifier
        self.assertEqual(part_one.eligible_part_one, YES)

        screening_part_two = ScreeningPartTwo.objects.get(
            screening_identifier=screening_identifier
        )
        for k, v in part_two_eligible_options.items():
            setattr(screening_part_two, k, v)
        screening_part_two.save()
        print(screening_part_two.reasons_ineligible_part_two)
        self.assertEqual(screening_part_two.eligible_part_two, YES)

        screening_part_three = ScreeningPartThree.objects.get(
            screening_identifier=screening_identifier
        )
        for k, v in part_three_eligible_options.items():
            setattr(screening_part_three, k, v)
        screening_part_three.save()
        self.assertEqual(screening_part_three.eligible_part_three, YES)

        subject_screening = SubjectScreening.objects.get(
            screening_identifier=screening_identifier
        )

        self.assertTrue(subject_screening.eligible)

        if eligibility_datetime:
            screening_part_three.eligibility_datetime = eligibility_datetime
            screening_part_three.save()
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=screening_identifier
            )
        return subject_screening

    def get_subject_consent(self, subject_screening):
        return baker.make_recipe(
            "meta_consent.subjectconsent",
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier=subject_screening.screening_identifier,
            initials=subject_screening.initials,
            dob=(
                get_utcnow().date()
                - relativedelta(years=subject_screening.age_in_years)
            ),
            site=Site.objects.get(name="hindu_mandal"),
        )

    def get_subject_visit(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        subject_identifier = subject_consent.subject_identifier

        appointment = Appointment.objects.get(
            subject_identifier=subject_identifier, visit_code=DAY1
        )
        appointment.appt_status = IN_PROGRESS_APPT
        appointment.save()
        return SubjectVisit.objects.create(appointment=appointment, reason=SCHEDULED)

    @staticmethod
    def get_next_subject_visit(subject_visit):
        appointment = subject_visit.appointment
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()
        next_appointment = appointment.next_by_timepoint
        next_appointment.appt_status = IN_PROGRESS_APPT
        next_appointment.save()
        return SubjectVisit.objects.create(
            appointment=next_appointment, reason=SCHEDULED
        )
