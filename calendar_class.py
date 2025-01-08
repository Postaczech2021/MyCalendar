from imports import *

class Calendar:
    cz_months = [
        "Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
        "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"
    ]

    cz_days = [
        "Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"
    ]

    def __init__(self, year, month, firstweekday=calendar.MONDAY):
        self.year = year
        self.month = month
        self.firstweekday = firstweekday
        self.current_date = datetime(year, month, 1)
        self.current_year = datetime.now().year
        self.current_month_number = datetime.now().month
        calendar.setfirstweekday(self.firstweekday)

    def get_prev_month(self):
        """Vrátí předchozí měsíc a rok."""
        first_day_of_month = self.current_date.replace(day=1)
        prev_month_date = first_day_of_month - timedelta(days=1)
        return prev_month_date.year, prev_month_date.month

    def get_next_month(self):
        """Vrátí následující měsíc a rok."""
        next_month_date = self.current_date.replace(day=28) + timedelta(days=4)
        next_month_date = next_month_date.replace(day=1)
        return next_month_date.year, next_month_date.month

    def get_days_matrix(self):
        """Vrátí matici dnů v měsíci."""
        cal = calendar.Calendar(firstweekday=self.firstweekday)
        return list(cal.monthdayscalendar(self.year, self.month))

    def get_cz_abbr_days(self):
        """Vrátí české zkratky dnů."""
        return ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]

    def get_current_month_name(self):
        """Vrátí název aktuálního měsíce a rok."""
        return f"{self.cz_months[self.month - 1]} {self.year}"

    def get_current_day_info(self):
        """Vrátí informace o aktuálním dni včetně dne v týdnu v češtině."""
        current_date = datetime.now()
        current_day_name = self.cz_days[current_date.weekday()]
        return f"{current_day_name}, {current_date.day}.{current_date.month}.{current_date.year}"

    def get_days_in_month(self):
        """Vrátí počet dnů v měsíci."""
        return calendar.monthrange(self.year, self.month)[1]

    @staticmethod
    def get_day_name(date):
        return Calendar.cz_days[date.weekday()]
