from ..core import WesternCalendar
from ..registry_tools import iso_register


@iso_register('IT')
class Italy(WesternCalendar):
    'Italy'

    FIXED_HOLIDAYS = WesternCalendar.FIXED_HOLIDAYS + (
        (4, 25, "Liberation Day"),
        (5, 1, "International Workers' Day"),
        (6, 2, "Republic Day"),
    )
    include_immaculate_conception = True
    include_epiphany = True
    include_easter_monday = True
    include_assumption = True
    include_all_saints = True
    include_boxing_day = True
    boxing_day_label = "St Stephen's Day"
