from django import forms
from edc_constants.constants import NO, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import FormValidator

from ..models import MalariaTest


class MalariaTestFormValidator(FormValidator):
    def clean(self):

        self.applicable_if(YES, field="performed", field_applicable="diagnostic_type")

        self.required_if(NO, field="performed", field_required="not_performed_reason")

        self.applicable_if(YES, field="performed", field_applicable="result")


class MalariaTestForm(CrfModelFormMixin, forms.ModelForm):

    form_validator_cls = MalariaTestFormValidator

    class Meta:
        model = MalariaTest
        fields = "__all__"
