#!/usr/bin/env python3

"""
polar_progress.py queries flow.polar.com and reports your
progress towards this years goal.

Requires a setting file with the following contents:

{
    "login": "FLOW_USERNAME",
    "password": "FLOW_PASSWORD",
    "goal": 1000
}

"""

import argparse
import datetime
import json
import re
import requests

FLOW_URL = 'https://flow.polar.com'
FLOW_LOGIN_POST_URL = "{}/login".format(FLOW_URL)
FLOW_LOGIN_GET_URL = FLOW_LOGIN_POST_URL
FLOW_GETREPORT_URL = "{}/progress/getReportAsJson".format(FLOW_URL)

def obtain_csrf(session):
    """
    Obtain the CSRF token from the login page.
    """
    resp = session.get(FLOW_LOGIN_GET_URL)
    contents = str(resp.content)
    match = re.search(r'csrfToken" value="([a-z0-9\-]+)"', contents)
    return match.group(1)

def login(username, password):
    """
    Logs in to the Polar flow webservice and returns
    a requests session to be used for further calls.
    """
    session = requests.session()
    csrf = obtain_csrf(session)
    postdata = {
        'csrfToken': csrf,
        'email': username,
        'password': password,
        'returnURL': '/'
    }

    resp = session.post(FLOW_LOGIN_POST_URL, data=postdata)
    if resp.status_code != 200:
        resp.raise_for_status()

    return session

def query_yearly_stats(session, year):
    """
    Users an active requests session to query
    the yearly stats for a given year.
    Returns the JSON information received from
    Polar flow on success.
    """
    params = {
        "from": "01-01-{}".format(year),
        "to": "31-12-{}".format(year),
        "sport":["RUNNING"],
        "barType":"distance",
        "group":"week",
        "report":"time",
        "reportSubtype":"training",
        "timeFrame":"year"
    }

    headers = {
        "x-requested-with": "XMLHttpRequest",
    }

    resp = session.post(FLOW_GETREPORT_URL, json=params, headers=headers)

    summary = resp.json()
    return summary

def write_summary(target, achieved_km):
    """
    Given the target for the current year and the achieved
    distance, it will print out a summary to standard out.
    """
    print("Target: {:d} km".format(target))
    daily_target = target / 365.
    print("Daily target: {:.2f} km/day".format(daily_target))
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    current_target_km = daily_target * day_of_year
    print("Expected distance to date: {:.1f} km".format(current_target_km))
    print("Achieved distance: {:.1f} km or {:.1f}%".format(achieved_km,
                                                           100.0 * achieved_km / target))
    if achieved_km > current_target_km:
        print("You are {:.1f} km or {:.1f} days ahead of schedule".format(
            achieved_km - current_target_km,
            (achieved_km - current_target_km) / daily_target))
    else:
        print("You are {:.1f} km behind schedule".format(current_target_km - achieved_km))
    print("Extrapolated result: {:.1f} km at the end of the year".format(
        365. * achieved_km / day_of_year))


def main():
    """
    Main entrypoint parses startup arguments.
    """
    parser = argparse.ArgumentParser(description="Polar Flow progress reporter",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--config", dest="config", help="the configuration file",
                        type=str, default="./progress_settings.json")
    args = parser.parse_args()

    with open(args.config, 'r') as settings_file:
        settings = json.load(settings_file)

    session = login(settings["login"], settings["password"])
    year_stats = query_yearly_stats(session, datetime.datetime.now().year)
    achieved_distance_km = \
        year_stats["progressContainer"]["trainingReportSummary"]["totalDistance"] / 1000.
    write_summary(settings["goal"], achieved_distance_km)


if __name__ == "__main__":
    main()
