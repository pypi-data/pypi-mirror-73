from django.test import TestCase, tag

from ..visit_schedules.schedule import schedule
from ..visit_schedules.visit_schedule import visit_schedule


class TestVisitSchedule(TestCase):
    def test_visit_schedule_models(self):

        self.assertEqual(visit_schedule.death_report_model, "meta_ae.deathreport")
        self.assertEqual(visit_schedule.offstudy_model, "edc_offstudy.subjectoffstudy")
        self.assertEqual(visit_schedule.locator_model, "edc_locator.subjectlocator")

    def test_schedule_models(self):
        self.assertEqual(schedule.onschedule_model, "meta_prn.onschedule")
        self.assertEqual(schedule.offschedule_model, "meta_prn.endofstudy")
        self.assertEqual(schedule.consent_model, "meta_consent.subjectconsent")
        self.assertEqual(schedule.appointment_model, "edc_appointment.appointment")

    def test_visit_codes(self):
        self.assertEqual(
            ["1000", "1005", "1010", "1030", "1060", "1090", "1120"],
            [visit for visit in schedule.visits],
        )

    def test_requisitions(self):
        prn = [
            "blood_glucose",
            "blood_glucose_poc",
            "chemistry",
            "fbc",
            "hba1c",
            "hba1c_poc",
        ]
        expected = {
            "1000": ["chemistry", "fbc"],
            "1005": [],
            "1010": [],
            "1030": ["chemistry"],
            "1060": ["chemistry", "hba1c_poc"],
            "1090": ["chemistry"],
            "1120": ["blood_glucose_poc", "chemistry", "fbc", "hba1c_poc"],
        }
        for visit_code, visit in schedule.visits.items():
            actual = [requisition.name for requisition in visit.requisitions]
            actual.sort()
            self.assertEqual(
                expected.get(visit_code),
                actual,
                msg=f"see requisitions for visit {visit_code}",
            )
            actual = [requisition.name for requisition in visit.requisitions_prn]
            actual.sort()
            self.assertEqual(
                prn, actual, msg=f"see PRN requisitions for visit {visit_code}"
            )

    @tag("1")
    def test_crfs(self):
        prn = [
            "meta_subject.bloodresultsfbc",
            "meta_subject.bloodresultsglu",
            "meta_subject.bloodresultshba1c",
            "meta_subject.bloodresultslft",
            "meta_subject.bloodresultslipid",
            "meta_subject.bloodresultsrft",
            "meta_subject.healtheconomics",
            "meta_subject.malariatest",
            "meta_subject.urinedipsticktest",
        ]
        expected = {
            "1000": [
                "meta_subject.physicalexam",
                "meta_subject.patienthistory",
                "meta_subject.bloodresultsfbc",
                "meta_subject.bloodresultslft",
                "meta_subject.bloodresultslipid",
                "meta_subject.bloodresultsrft",
                "meta_subject.malariatest",
                "meta_subject.urinedipsticktest",
            ],
            "1005": [
                "meta_subject.followupvitals",
                "meta_subject.followupexamination",
                "meta_subject.healtheconomics",
                "meta_subject.medicationadherence",
            ],
            "1010": [
                "meta_subject.followupvitals",
                "meta_subject.followupexamination",
                "meta_subject.medicationadherence",
            ],
            "1030": [
                "meta_subject.bloodresultslft",
                "meta_subject.bloodresultsrft",
                "meta_subject.followupvitals",
                "meta_subject.followupexamination",
                "meta_subject.medicationadherence",
            ],
            "1060": [
                "meta_subject.followupvitals",
                "meta_subject.followupexamination",
                "meta_subject.medicationadherence",
                "meta_subject.glucose",
                "meta_subject.bloodresultshba1c",
                "meta_subject.bloodresultslft",
                "meta_subject.bloodresultsrft",
            ],
            "1090": [
                "meta_subject.bloodresultslft",
                "meta_subject.bloodresultsrft",
                "meta_subject.followupvitals",
                "meta_subject.followupexamination",
                "meta_subject.medicationadherence",
            ],
            "1120": [
                "meta_subject.followupvitals",
                "meta_subject.followupexamination",
                "meta_subject.medicationadherence",
                "meta_subject.glucose",
                "meta_subject.bloodresultshba1c",
                "meta_subject.bloodresultsfbc",
                "meta_subject.bloodresultslipid",
                "meta_subject.bloodresultslft",
                "meta_subject.bloodresultsrft",
                "meta_subject.malariatest",
            ],
        }
        for visit_code, visit in schedule.visits.items():
            actual = [crf.model for crf in visit.crfs]
            actual.sort()
            expected.get(visit_code).sort()
            self.assertEqual(
                expected.get(visit_code), actual, msg=f"see CRFs for visit {visit_code}"
            )

            actual = [crf.model for crf in visit.crfs_prn]
            actual.sort()
            self.assertEqual(prn, actual, msg=f"see PRN CRFs for visit {visit_code}")
