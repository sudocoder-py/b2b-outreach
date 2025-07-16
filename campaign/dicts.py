timezone_options = [
    # Americas
    ("America/Los_Angeles", "(UTC−08:00) Pacific Time — Los Angeles, Vancouver"),
    ("America/Denver", "(UTC−07:00) Mountain Time — Denver, Calgary"),
    ("America/Chicago", "(UTC−06:00) Central Time — Chicago, Mexico City"),
    ("America/New_York", "(UTC−05:00) Eastern Time — New York, Toronto, Bogota"),
    ("America/Halifax", "(UTC−04:00) Atlantic Time — Halifax, Santiago, La Paz"),
    ("America/Sao_Paulo", "(UTC−03:00) São Paulo, Buenos Aires"),
    ("Atlantic/South_Georgia", "(UTC−02:00) South Georgia and Atlantic Islands"),

    # Africa + Europe
    ("Europe/London", "(UTC±00:00) Greenwich Mean Time — London, Dublin, Accra"),
    ("Europe/Paris", "(UTC+01:00) Central Europe — Paris, Berlin, Madrid, Rome, Lagos"),
    ("Europe/Athens", "(UTC+02:00) Eastern Europe — Athens, Bucharest, Kyiv, Helsinki"),
    ("Africa/Cairo", "(UTC+02:00) Egypt, South Africa, Sudan"),
    ("Europe/Istanbul", "(UTC+03:00) Turkey"),
    ("Asia/Amman", "(UTC+03:00) Jordan, Syria, Lebanon, Palestine"),
    ("Asia/Riyadh", "(UTC+03:00) Saudi Arabia, Iraq, Kuwait, Qatar, Bahrain"),
    ("Africa/Nairobi", "(UTC+03:00) East Africa — Kenya, Ethiopia, Somalia"),
    ("Asia/Tehran", "(UTC+03:30) Iran (Tehran Time)"),
    ("Asia/Dubai", "(UTC+04:00) UAE, Oman"),

    # Central and South Asia
    ("Asia/Kabul", "(UTC+04:30) Afghanistan"),
    ("Asia/Karachi", "(UTC+05:00) Pakistan, Uzbekistan, Turkmenistan"),
    ("Asia/Tashkent", "(UTC+05:00) Central Asia — Tashkent, Ashgabat"),
    ("Asia/Calcutta", "(UTC+05:30) India, Sri Lanka"),
    ("Asia/Kathmandu", "(UTC+05:45) Nepal"),
    ("Asia/Dhaka", "(UTC+06:00) Bangladesh, Bhutan"),
    ("Asia/Bangkok", "(UTC+07:00) Thailand, Vietnam, Cambodia, Jakarta"),
    ("Asia/Shanghai", "(UTC+08:00) China, Singapore, Malaysia, Philippines, Hong Kong")
]


days_options = [
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday"),
    ]

def get_default_days():
        return ['mon', 'tue', 'wed', 'thu']


time_options= [
        ("00:00", "Midnight | 12:00 AM"),
        ("01:00", "1:00 AM"),
        ("02:00", "2:00 AM"),
        ("03:00", "3:00 AM"),
        ("04:00", "4:00 AM"),
        ("05:00", "5:00 AM"),
        ("06:00", "6:00 AM"),
        ("07:00", "7:00 AM"),
        ("08:00", "8:00 AM"),
        ("09:00", "9:00 AM"),
        ("10:00", "10:00 AM"),
        ("11:00", "11:00 AM"),
        ("12:00", "12:00 PM"), 
        ("13:00", "1:00 PM"),
        ("14:00", "2:00 PM"),
        ("15:00", "3:00 PM"),
        ("16:00", "4:00 PM"),
        ("17:00", "5:00 PM"),
        ("18:00", "6:00 PM"),
        ("19:00", "7:00 PM"),  
        ("20:00", "8:00 PM"),
        ("21:00", "9:00 PM"),
        ("22:00", "10:00 PM"),
        ("23:00", "11:00 PM"),
]
