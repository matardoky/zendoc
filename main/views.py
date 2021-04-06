import datetime
from django.shortcuts import render

from django.http import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseRedirect,
    JsonResponse,
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from main.serializers import CompanySerializer, RuleSerializer
from main.models.authenticate import Company, User
from main.models.rules import Rule
from main.models.calendars import Calendar
from main.models.events import Event

from main.filters import IsUserFilterBackend

from main.serializers import (
    CalendarSerializer, 
    EventSerializer,
    EventListSerializer
)


class UserMixin(object):
    permission_classes = (IsAuthenticated,)
    filter_backends = (IsUserFilterBackend, )

    def perform_create(self, serializer):
        serializer.save(user= self.request.user, company=self.request.user.company)

class CompanyListView(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)
    lookup_field = "uuid"

class RuleView(ListCreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer


class CalendarViewSet(UserMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, )


class EventAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        queryset = Event.objects.all()
        serializer = EventListSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


def api_occurrences(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    calendar_slug = request.GET.get("calendar_slug")
    timezone = request.GET.get("timezone")

    try:
        response_data = _api_occurrences(start, end, calendar_slug, timezone)
    except (ValueError, Calendar.DoesNotExist) as e:
        return HttpResponseBadRequest(e)

    return JsonResponse(response_data, safe=False)


def _api_occurrences(start, end, calendar_slug, timezone):

    if not start or not end:
        raise ValueError("Start and end parameters are required")
    # version 2 of full calendar
    # TODO: improve this code with date util package
    if "-" in start:

        def convert(ddatetime):
            if ddatetime:
                ddatetime = ddatetime.split(" ")[0]
                try:
                    return datetime.datetime.strptime(ddatetime, "%Y-%m-%d")
                except ValueError:
                    # try a different date string format first before failing
                    return datetime.datetime.strptime(ddatetime, "%Y-%m-%dT%H:%M:%S")

    else:

        def convert(ddatetime):
            return datetime.datetime.utcfromtimestamp(float(ddatetime))

    start = convert(start)
    end = convert(end)
    current_tz = False
    if timezone and timezone in pytz.common_timezones:
        # make start and end dates aware in given timezone
        current_tz = pytz.timezone(timezone)
        start = current_tz.localize(start)
        end = current_tz.localize(end)
    elif settings.USE_TZ:
        # If USE_TZ is True, make start and end dates aware in UTC timezone
        utc = pytz.UTC
        start = utc.localize(start)
        end = utc.localize(end)

    if calendar_slug:
        # will raise DoesNotExist exception if no match
        calendars = [Calendar.objects.get(slug=calendar_slug)]
    # if no calendar slug is given, get all the calendars
    else:
        calendars = Calendar.objects.all()
    response_data = []
    # Algorithm to get an id for the occurrences in fullcalendar (NOT THE SAME
    # AS IN THE DB) which are always unique.
    # Fullcalendar thinks that all their "events" with the same "event.id" in
    # their system are the same object, because it's not really built around
    # the idea of events (generators)
    # and occurrences (their events).
    # Check the "persisted" boolean value that tells it whether to change the
    # event, using the "event_id" or the occurrence with the specified "id".
    # for more info https://github.com/llazzaro/django-scheduler/pull/169
    i = 1
    if Occurrence.objects.all().count() > 0:
        i = Occurrence.objects.latest("id").id + 1
    event_list = []
    for calendar in calendars:
        # create flat list of events from each calendar
        event_list += calendar.events.filter(start__lte=end).filter(
            Q(end_recurring_period__gte=start) | Q(end_recurring_period__isnull=True)
        )
    for event in event_list:
        occurrences = event.get_occurrences(start, end)
        for occurrence in occurrences:
            occurrence_id = i + occurrence.event.id
            existed = False

            if occurrence.id:
                occurrence_id = occurrence.id
                existed = True

            recur_rule = occurrence.event.rule.name if occurrence.event.rule else None

            if occurrence.event.end_recurring_period:
                recur_period_end = occurrence.event.end_recurring_period
                if current_tz:
                    # make recur_period_end aware in given timezone
                    recur_period_end = recur_period_end.astimezone(current_tz)
                recur_period_end = recur_period_end
            else:
                recur_period_end = None

            event_start = occurrence.start
            event_end = occurrence.end
            if current_tz:
                # make event start and end dates aware in given timezone
                event_start = event_start.astimezone(current_tz)
                event_end = event_end.astimezone(current_tz)

            response_data.append(
                {
                    "id": occurrence_id,
                    "title": occurrence.title,
                    "start": event_start,
                    "end": event_end,
                    "existed": existed,
                    "event_id": occurrence.event.id,
                    "color": occurrence.event.color_event,
                    "description": occurrence.description,
                    "rule": recur_rule,
                    "end_recurring_period": recur_period_end,
                    "creator": str(occurrence.event.creator),
                    "calendar": occurrence.event.calendar.slug,
                    "cancelled": occurrence.cancelled,
                }
            )
    return response_data