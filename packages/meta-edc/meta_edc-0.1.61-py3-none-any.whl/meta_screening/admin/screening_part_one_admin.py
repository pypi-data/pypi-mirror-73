from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import meta_screening_admin
from ..forms import (
    ScreeningPartOneForm,
    part_two_fields,
    part_three_fields,
    calculated_fields,
)
from ..models import ScreeningPartOne
from .fieldsets import (
    get_part_one_fieldset,
    get_part_two_fieldset,
    get_part_three_fieldset,
)
from .subject_screening_admin import SubjectScreeningAdmin


@admin.register(ScreeningPartOne, site=meta_screening_admin)
class ScreeningPartOneAdmin(SubjectScreeningAdmin):

    form = ScreeningPartOneForm

    fieldsets = (
        get_part_one_fieldset(),
        get_part_two_fieldset(collapse=True),
        get_part_three_fieldset(collapse=True),
        audit_fieldset_tuple,
    )

    readonly_fields = (*part_two_fields, *part_three_fields, *calculated_fields)
