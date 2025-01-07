import calendar
from datetime import datetime, timedelta

class Calendar:
    cz_months = [
        "Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
        "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"
    ]

    cz_days = [
        "Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota","Neděle"
    ]
    
    cz_holidays = {
        "Nový rok": "01-01",
        "Velikonoční pondělí": "datum závisí na roku",
        "Svátek práce": "05-01",
        "Den vítězství": "05-08",
        "Den slovanských věrozvěstů Cyrila a Metoděje": "07-05",
        "Den upálení mistra Jana Husa": "07-06",
        "Den české státnosti": "09-28",
        "Den vzniku samostatného československého státu": "10-28",
        "Den boje za svobodu a demokracii": "11-17",
        "Štědrý den": "12-24",
        "1. svátek vánoční": "12-25",
        "2. svátek vánoční": "12-26"
    }

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

    def get_cz_holidays(self):
        """Vrátí slovník obsahující české svátky a jejich data."""
        return self.cz_holidays

    def get_current_day_info(self):
        """Vrátí informace o aktuálním dni včetně dne v týdnu v češtině."""
        current_date = datetime.now()  # Získání aktuálního data a času
        current_day_name = self.cz_days[current_date.weekday()]  # Přiřazení českého názvu dne
        return f"{current_day_name}, {current_date.day}.{current_date.month}.{current_date.year}"  # Výpis dne a datumu ve formátu "název dne, d.m.Y"
