import json
import requests
import streamlit as st

from datetime import datetime


IDENTIFIER= 'eman-bysykkel-streamlit'
API_URL = "https://gbfs.urbansharing.com/oslobysykkel.no"
INFORMATION = "station_information.json"
STATUS = "station_status.json"


def headers():
    return {'Client-Identifier': IDENTIFIER}


def request(level):
    return requests.get(f"{API_URL}/{level}", headers=headers())


def get_stations(station_info, key):
    station_list = station_info.json()["data"]["stations"]
    return {station[key]: station for station in station_list}


def get_status(station_status, station_id):
    for station in station_status.json()['data']['stations']:
        if station['station_id'] == station_id:
            return (
                station["num_bikes_available"],
                station["num_bikes_available"],
                station["last_reported"],
            )
    return -1, -1


def main():
    st.markdown("# 🚲 bysykkel-streamlit")
    st.markdown(
        "> You can use this app to see how many bikes ( 🚲) and docks ( 🏠) are available at your station of choice"
    )

    station_info = request(INFORMATION)

    if station_info.status_code != 200:
        st.error("Service unavailable 😭")

    mode = st.radio('Search by:', ['Station Name', 'Station Address'])

    if mode == 'Station Name':
        stations = get_stations(station_info, 'name')
    elif mode == 'Station Address':
        stations = get_stations(station_info, 'address')

    station_key = st.selectbox("Browse or search stations:", [''] + list(stations.keys()))

    if station_key:
        station_status = request(STATUS)
        if station_status.status_code != 200:
            st.error("Service unavailable 😭")
        else:
            n_bikes, n_docks, timestamp = get_status(station_status, stations[station_key]['station_id'])
            bikes = "🚲 " * n_bikes if n_bikes > 0 else "😩"
            docks = "🏠 " * n_docks if n_docks > 0 else "😭"
        st.markdown(f"### Available **bikes**: {n_bikes}\n # {bikes}")
        st.markdown(f"### Available **docks**: {n_docks}\n # {docks}")
        st.markdown(f"last updated: {datetime.fromtimestamp(timestamp)}")


if __name__ == "__main__":
    main()