from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import meta_subject_admin
from ..forms import FollowupVitalsForm
from ..models import FollowupVitals
from .modeladmin import CrfModelAdminMixin


@admin.register(FollowupVitals, site=meta_subject_admin)
class FollowupVitalsAdmin(
    CrfModelAdminMixin, FormLabelModelAdminMixin, SimpleHistoryAdmin
):

    form = FollowupVitalsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Vitals",
            {
                "description": "To be completed by the research nurse",
                "fields": (
                    "weight",
                    "sys_blood_pressure",
                    "dia_blood_pressure",
                    "heart_rate",
                    "temperature",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ()

    radio_fields = {}
