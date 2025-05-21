import requests
import json
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from strava_draw_api.models import Activity, Integration, ActivityStream


STRAVA_CLIENT_ID = settings.STRAVA_CLIENT_ID
STRAVA_CLIENT_SECRET = settings.STRAVA_CLIENT_SECRET
TOKEN_ENDPOINT = "https://www.strava.com/api/v3/oauth/token"
ATHLETES_ENDPOINT = "https://www.strava.com/api/v3/athletes/"


def refresh_tokens(integration):
    body = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'refresh_token': integration.refresh_token,
        'grant_type': "refresh_token",
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }
    response = requests.post(TOKEN_ENDPOINT, headers=headers, json=body)
    data = response.json()
    if data.get('errors', False):
        print('error refreshing tokens for ', integration.user)
        print('error', data.__dict__)
    else:
        integration.access_token = data['access_token']
        integration.refresh_token = data['refresh_token']
        integration.expires_at = data['expires_at']
        integration.save()
    return integration


def get_access_token(refresh_token):
    body = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }

    response = requests.post(TOKEN_ENDPOINT, headers=headers, json=body)
    print(response)
    return response.json()


def get_authorization(code, user, scope):
    """request to trade an auth code from the FE authorization for tokens"""

    body = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'code': code,
        'grant_type': "authorization_code",
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }
    response = requests.post(TOKEN_ENDPOINT, headers=headers, data=json.dumps(body))

    if response.status_code == 200:
        data = response.json()
        athlete_data = data['athlete']

        # create an integration
        new_integration_data = {
            'account_id': athlete_data['id'],
            'scope': scope,
            'user': user,
            'refresh_token': data['refresh_token'],
            'access_token': data['access_token'],
            'expires_at': data['expires_at'],
            'first_name': athlete_data['firstname'],
            'last_name': athlete_data['lastname'],
            'auto_import': True,
        }
        new_integration = Integration(**new_integration_data)
        new_integration.save()
        print('new_integration', new_integration)
        return new_integration
    else:
        print('houston we have a problem')
        # could return the error from strava here
        return False


def get_activities(athlete_id, access_token, refresh_token, user, page=1, retry=False):
    """the initial activities pull after creating an account and authorizing Strava"""

    headers = {
        'Accept': "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }
    url = f'https://www.strava.com/api/v3/athletes/{athlete_id}/activities?access_token={access_token}&per_page=100&page={page}'
    response = requests.get(url, headers=headers)
    # print(response.json())

    activities = []
    for strava_activity in response.json():
        # print('strava_activity', strava_activity['id'])
        # if 'run' or 'ride' or 'walk' in strava_activity['sport_type'].lower():
        map = strava_activity.get('map', None)
        polyline = map.get('summary_polyline', None)
        if polyline:
            new_activity_data = {
                'user': user,
                'integration': user.integration,
                'external_id': strava_activity['id'],
                'activity_type': strava_activity['sport_type'],
                'duration': strava_activity['moving_time'],
                'distance': strava_activity.get('distance', None),
                'avg_watts': strava_activity.get('average_watts', None),
                'avg_speed': strava_activity.get('average_speed', None),
                'work_done': strava_activity.get('kilojoules', None),
                'elev_gain': strava_activity['total_elevation_gain'],
                'polyline': polyline,
                'name': strava_activity['name'],
                'start_date': strava_activity['start_date'],
                'weighted_average_watts': strava_activity.get('weighted_average_watts', None),
            }
            
            activity = None
            try:
                activity = Activity.objects.get(user=user, integration=user.integration, external_id=strava_activity['id'])
            except Activity.DoesNotExist:
                pass

            if activity:
                activities.append(activity)
                create_activity_stream(activity, user.integration, 'altitude')
            else:
                new_activity = Activity(**new_activity_data)
                new_activity.save()
                create_activity_stream(new_activity, user.integration, 'altitude')
                activities.append(new_activity)
    return activities


def get_all_activities(athlete_id, access_token, refresh_token, user, page=1, retry=False):
    """the initial activities pull after creating an account and authorizing Strava"""

    activities = []
    more_activities = True
    while more_activities:
        print('getting page', page)
        activities_batch = get_activities(athlete_id, access_token, refresh_token, user, page, False)
        activities.extend(activities_batch)
        page += 1
        # 30 is the default (max?) count per request strava allows
        if len(activities_batch) < 100:
            more_activities = False
    print('all activities', activities)
    print('total activity count', len(activities))
    return activities


def get_single_activity(activity_id, integration):
    """request an Activity object after a webhook is received"""

    if integration.expires_at < datetime.now().timestamp():
        integration = refresh_tokens(integration)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {integration.access_token}",
    }
    url = f"https://www.strava.com/api/v3/activities/{activity_id}"
    response = requests.get(url, headers=headers)
    strava_activity = response.json()
    return strava_activity


def get_activity_streams(activity_id, integration, stream_type):
    """
    request an Activity stream object, pass a type to specify the stream (elevation, distance, etc)
    generally at least 2 streams will be returned, the stream_type that was requested and either 'time' or 'distance',
    which are used to chart the requested stream data
    """

    if integration.expires_at < datetime.now().timestamp():
        integration = refresh_tokens(integration)

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {integration.access_token}",
    }
    url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?key_by_type=true&keys={stream_type}"
    response = requests.get(url, headers=headers)
    stream_resp = response.json()
    # stream_resp = [ {
    #     "type" : "distance",
    #     "data" : [ 2.9, 5.8, 8.5, 11.7, 15, 19, 23.2, 28, 32.8, 38.1, 43.8, 49.5 ],
    #     "series_type" : "distance",
    #     "original_size" : 12,
    #     "resolution" : "high"
    # } ]
    return stream_resp


def create_activity_stream(activity, integration, stream_type):
    print('stream_type', stream_type)
    strava_streams = get_activity_streams(activity.external_id, integration, stream_type)
    activity_streams = []
    for stream in strava_streams:
        print('stream', stream)
        new_stream_data = {
            'activity': activity,
            'stream_type': stream,
            'data': strava_streams[stream]['data'],
            'original_size': strava_streams[stream]['original_size'],
        }

        activity_stream = ActivityStream(**new_stream_data)
        activity_stream.save()
        activity_streams.append(activity_stream)

    return activity_streams


def create_strava_activity(activity_id, integration, user):
    strava_activity = get_single_activity(activity_id, integration)
    # if 'run' or 'ride' or 'walk' in strava_activity['sport_type'].lower():
    map = strava_activity.get('map', None)
    polyline = map.get('summary_polyline', None)
    # only create activities that have a map
    if polyline:
        new_activity_data = {
            'user': user,
            'integration': integration,
            'external_id': activity_id,
            'activity_type': strava_activity['sport_type'],
            'duration': strava_activity['moving_time'],
            'distance': strava_activity.get('distance', None),
            'avg_watts': strava_activity.get('average_watts', None),
            'avg_speed': strava_activity.get('average_speed', None),
            'work_done': strava_activity.get('kilojoules', None),
            'elev_gain': strava_activity['total_elevation_gain'],
            'polyline': polyline,
            'name': strava_activity['name'],
            'start_date': strava_activity['start_date'],
            'weighted_average_watts': strava_activity.get('weighted_average_watts', None),
        }
        activity = Activity(**new_activity_data)
        activity.save()
        return activity
    return


def update_strava_activity(activity_id, integration, activity):
    strava_activity = get_single_activity(activity_id, integration)
    map = strava_activity.get('map', None)
    activity.activity_type = strava_activity['sport_type']
    activity.duration = strava_activity['moving_time']
    activity.distance = strava_activity.get('distance', None)
    activity.avg_watts = strava_activity.get('average_watts', None)
    activity.avg_speed = strava_activity.get('average_speed', None)
    activity.work_done = strava_activity.get('kilojoules', None)
    activity.elev_gain = strava_activity['total_elevation_gain']
    activity.polyline = map.get('summary_polyline', None)
    activity.name = strava_activity['name']
    activity.start_date = strava_activity['start_date']
    activity.weighted_average_watts = strava_activity.get('weighted_average_watts', None)
    activity.save()
    return activity
