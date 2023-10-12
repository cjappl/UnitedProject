import datetime


def datetime_within_tolerance(time_1, time_2, tolerance_min=30):
    """ Returns true if the datetimes are within the tolarance of each other """
    tolerance_time_delta = datetime.timedelta(minutes=tolerance_min)

    if time_1 - tolerance_time_delta <= time_2 <= time_1 + tolerance_time_delta:
        return True
    else:
        return False
