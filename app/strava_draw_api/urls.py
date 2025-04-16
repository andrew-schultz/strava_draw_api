from django.urls import path

from strava_draw_api.views import activity, activity_stream, auth, strava, webhooks

activity_urlpatterns = [
    path('', activity.ActivityAPIView.as_view(), name='activity-list'),
    path('first/', activity.FirstTimeActivityAPIView.as_view(), name='activity-first'),
]

activity_stream_urlpatterns = [
    path('<int:activity_id>/', activity_stream.ActivityStreamAPIView.as_view(), name='activity-stream'),
]

auth_urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),
    path('logout/', auth.LogOutView.as_view(), name='logout'),
    path('signup/', auth.SignUpView.as_view(), name='signup'),
]

strava_urlpatterns = [
    path('auth/', strava.AuthAPIView.as_view(), name='auth'),
    path('token/', strava.TokenAPIView.as_view(), name='token'),
]

webhook_urlpatterns = [
    path('strava/', webhooks.StravaWebhookView.as_view(), name='strava-webhook'),
]
