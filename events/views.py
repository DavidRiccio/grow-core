from .models import Event
from .serializers import EventSerializer


# Create your views here.
def event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, request=request)
    return serializer.json_response()


def event_detail(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    serializer = EventSerializer(event, request=request)
    return serializer.json_response()
