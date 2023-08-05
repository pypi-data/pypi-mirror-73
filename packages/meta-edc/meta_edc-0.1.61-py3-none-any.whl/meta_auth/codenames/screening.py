from copy import copy
from edc_auth.codenames import screening as default
from sarscov2.auth import sarscov2_codenames

screening = copy(default)
screening += [
    "meta_screening.add_screeningpartone",
    "meta_screening.add_screeningpartthree",
    "meta_screening.add_screeningparttwo",
    "meta_screening.add_subjectrefusal",
    "meta_screening.change_screeningpartone",
    "meta_screening.change_screeningpartthree",
    "meta_screening.change_screeningparttwo",
    "meta_screening.change_subjectrefusal",
    "meta_screening.delete_icpreferral",
    "meta_screening.delete_screeningpartone",
    "meta_screening.delete_screeningpartthree",
    "meta_screening.delete_screeningparttwo",
    "meta_screening.delete_subjectrefusal",
    "meta_screening.view_historicalscreeningpartone",
    "meta_screening.view_historicalscreeningpartthree",
    "meta_screening.view_historicalscreeningparttwo",
    "meta_screening.view_historicalsubjectscreening",
    "meta_screening.view_icpreferral",
    "meta_screening.view_historicalsubjectrefusal",
    "meta_screening.view_historicalicpreferral",
    "meta_screening.view_screeningpartone",
    "meta_screening.view_screeningpartthree",
    "meta_screening.view_screeningparttwo",
    "meta_screening.view_subjectscreening",
    "meta_screening.view_subjectrefusal",
]
screening.extend(sarscov2_codenames)
screening.sort()
