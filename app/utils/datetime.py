from datetime import datetime

import pytz


def get_brazil_current_datetime():
    brasilian_tz = pytz.timezone("America/Sao_Paulo")
    current_brasilian_datetime = datetime.now(brasilian_tz)
    return current_brasilian_datetime
