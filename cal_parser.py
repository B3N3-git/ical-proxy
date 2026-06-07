import logging
from datetime import timedelta
from typing import Tuple
from icalendar import Calendar, vDuration
import requests

def remove_duplicate_uids(cal):
    new_cal = Calendar()

    #Header
    for name, value in cal.items():
        new_cal.add(name, value)

    seen_uids = set()
    for component in cal.walk():
        if component.name == 'VEVENT':
            uid = component.get('UID')

            if uid in seen_uids:
                logging.debug(f"Removed duplicate: {uid}")
                continue

            seen_uids.add(uid)
            new_cal.add_component(component)

    return new_cal

def unfold_ics(ics):
    unfolded = ics.replace('\n ', '')
    return unfolded

def is_key(s: str) -> bool:
    return len(s) > 0 and all(c.isupper() or c == '-' for c in s)

def find_key(line: str) -> str | None:
    if line.startswith(' '):
        return None
    # Find the index of the first occurrence of ':' or ';'
    delimiters = [line.find(':'), line.find(';')]

    # Filter out cases where the delimiter was not found (-1)
    valid_indices = [idx for idx in delimiters if idx != -1]

    key = None
    if valid_indices:
        # The split point is the first occurrence of either ':' or ';'
        key = line[:min(valid_indices)]
        if not is_key(key):
            key = None

    return key

def fix_wrong_keys(content):
    lines = content.splitlines()
    if not lines:
        logging.error(f"Something went wrong in fix_wrong_keys")
        return ""

    result = [lines[0]]

    if find_key(lines[0]) is None:
        logging.error(f"Line {lines[0]} has not a valid key")
        return ""

    for line in lines[1:]:
        key = find_key(line)
        if key is None:
            result[-1] += line
            logging.debug(f"Line {line} append to {find_key(result[-1])}.")
        else:
            result.append(line)

    return "\n".join(result)

def generate_ics(url : str) -> Tuple[str, str]:
    cal_name = "no_name"
    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f"Error fetching {url} \n Status code: {response.status_code}")
        return "", ""

    ics = response.content.decode('utf-8')

    cal = Calendar.from_ical(ics)

    if 'X-WR-CALNAME' in cal:
        cal_name = cal['X-WR-CALNAME']

    #new_interval = vDuration(timedelta(minutes=25))
    #if cal.get('REFRESH-INTERVAL') != new_interval:
    #    cal['REFRESH-INTERVAL'] = new_interval
    #    logging.debug(f"REFRESH-INTERVAL auf {new_interval} gesetzt.")
    if 'REFRESH-INTERVAL' in cal:
        logging.debug(f"REFRESH-INTERVAL: {cal['REFRESH-INTERVAL']} entfernt")
        del cal['REFRESH-INTERVAL']

    if 'X-PUBLISHED-TTL' in cal:
        logging.debug(f"X-PUBLISHED-TTL: {cal['X-PUBLISHED-TTL']} entfernt")
        del cal['X-PUBLISHED-TTL']

    cal = remove_duplicate_uids(cal)

    ics = cal.to_ical().decode('utf-8').replace("\r\n", "\n").strip()
    ics = unfold_ics(ics)
    ics = fix_wrong_keys(ics)

    return ics, cal_name