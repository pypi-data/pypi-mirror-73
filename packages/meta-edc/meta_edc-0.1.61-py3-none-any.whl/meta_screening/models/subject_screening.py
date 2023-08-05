from edc_constants.constants import QUESTION_RETIRED
from edc_model.models import BaseUuidModel
from edc_screening.model_mixins import ScreeningModelMixin
from edc_screening.screening_identifier import ScreeningIdentifier

from .calculated_model_mixin import CalculatedModelMixin
from .eligibility_model_mixin import EligibilityModelMixin
from .part_one_fields_model_mixin import PartOneFieldsModelMixin
from .part_two_fields_model_mixin import PartTwoFieldsModelMixin
from .part_three_fields_model_mixin import PartThreeFieldsModelMixin


class SubjectScreeningModelError(Exception):
    pass


class ScreeningIdentifier(ScreeningIdentifier):

    template = "S{random_string}"


class SubjectScreening(
    PartOneFieldsModelMixin,
    PartTwoFieldsModelMixin,
    PartThreeFieldsModelMixin,
    EligibilityModelMixin,
    CalculatedModelMixin,
    ScreeningModelMixin,
    BaseUuidModel,
):

    identifier_cls = ScreeningIdentifier

    def save(self, *args, **kwargs):
        if self._meta.label_lower == "meta_screening.subjectscreening":
            raise SubjectScreeningModelError(
                "Unable to save. Save via P1-3 proxy models."
            )
        self.consent_ability = QUESTION_RETIRED
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
