from enum import Enum


#
#   ALL FREQUENCIES SUPPORTED BY CHRONOSDB
#


class Freq(Enum):
    Annual = "A"  # * `A`      Annual = `A-DEC`
    AnnualEndingDec = "A-DEC"  # * `A-DEC`  Annual - December year end
    AnnualEndingJan = "A-JAN"  # * `A-JAN`  Annual - January year end
    AnnualEndingFeb = "A-FEB"  # * `A-FEB`  Annual - February year end
    AnnualEndingMar = "A-MAR"  # * `A-MAR`  Annual - March year end
    AnnualEndingApr = "A-APR"  # * `A-APR`  Annual - April year end
    AnnualEndingMay = "A-MAY"  # * `A-MAY`  Annual - May year end
    AnnualEndingJun = "A-JUN"  # * `A-JUN`  Annual - June year end
    AnnualEndingJul = "A-JUL"  # * `A-JUL`  Annual - July year end
    AnnualEndingAug = "A-AUG"  # * `A-AUG`  Annual - August year end
    AnnualEndingSep = "A-SEP"  # * `A-SEP`  Annual - September year end
    AnnualEndingOct = "A-OCT"  # * `A-OCT`  Annual - October year end
    AnnualEndingNov = "A-NOV"  # * `A-NOV`  Annual - November year end

    Quarterly = "Q"
    QuarterlyEndingDec = "Q"
    QuarterlyEndingJan = "Q-JAN"
    QuarterlyEndingFeb = "Q-FEB"
    QuarterlyEndingMar = "Q-MAR"
    QuarterlyEndingApr = "Q-APR"
    QuarterlyEndingMay = "Q-MAY"
    QuarterlyEndingJun = "Q-JUN"
    QuarterlyEndingJul = "Q-JUL"
    QuarterlyEndingAug = "Q-AUG"
    QuarterlyEndingSep = "Q-SEP"
    QuarterlyEndingOct = "Q-OCT"

    Monthly = "M"  # * `M`      Monthly

    Weekly = "W"  # * `W`      Weekly - Sunday end of week
    WeeklyEndingSun = "W"  # * `W-SUN`  Weekly - Sunday end of week
    WeeklyEndingMon = "W-MON"  # * `W-MON`  Weekly - Monday end of week
    WeeklyEndingTue = "W-TUE"  # * `W-TUE`  Weekly - Tuesday end of week
    WeeklyEndingWed = "W-WED"  # * `W-WED`  Weekly - Wednesday end of week
    WeeklyEndingThu = "W-THU"  # * `W-THU`  Weekly - Thursday end of week
    WeeklyEndingFri = "W-THU"  # * `W-FRI`  Weekly - Friday end of week
    WeeklyEndingSat = "W-SAT"  # * `W-SAT`  Weekly - Saturday end of week

    BusinessDaily = "B"  # * `B`  Business days
    CustomBusinessDaily = "C"  # * `C`  Custom business day frequency
    Daily = "D"  # * `D`  Daily, calendar day frequency

    # Hourly = "H"                # * `H`  Hourly
    # Minutely = "T"              # * `T`  Minutely
    # Secondly = "S"          # * `S`  Secondly
    # Millisecondly = "L"     # * `L`  Millisecondly
    # Microsecondly = "U"     # * `U`  Microsecondly

    @staticmethod
    def keys():
        return [name for name, _ in Freq.__members__.items()]

    @staticmethod
    def values():
        return [val.value for _, val in Freq.__members__.items()]


pandas_freq_to_chronos_freq = {
    "A": "A",
    "A-JAN": "A-JAN",
    "A-FEB": "A-FEB",
    "A-MAR": "A-MAR",
    "A-APR": "A-APR",
    "A-MAY": "A-MAY",
    "A-JUN": "A-JUN",
    "A-JUL": "A-JUL",
    "A-AUG": "A-AUG",
    "A-SEP": "A-SEP",
    "A-OCT": "A-OCT",
    "A-NOV": "A-NOV",
    "A-DEC": "A",
    "Q": "Q",
    "Q-JAN": "Q-JAN",
    "Q-FEB": "Q-FEB",
    "Q-MAR": "Q-MAR",
    "Q-APR": "Q-APR",
    "Q-MAY": "Q-MAY",
    "Q-JUN": "Q-JUN",
    "Q-JUL": "Q-JUL",
    "Q-AUG": "Q-AUG",
    "Q-SEP": "Q-SEP",
    "Q-OCT": "Q-OCT",
    "Q-DEC": "Q",
    "M": "M",
    "W": "W",
    "W-MON": "W-MON",
    "W-TUE": "W-TUE",
    "W-WED": "W-WED",
    "W-THU": "W-THU",
    "W-THU": "W-THU",
    "W-SAT": "W-SAT",
    "W-SUN": "W",
    "B": "B",
    "C": "C",
    "D": "D"
}

all_freqencies_abbriviations = Freq.values()
