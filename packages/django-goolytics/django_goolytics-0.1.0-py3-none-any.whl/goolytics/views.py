import json
import logging
import random

from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from goolytics.models import Site, Client, TrackHit, Session
from django.core.serializers.json import DjangoJSONEncoder
from .security import report_authorization

log = logging.getLogger("lytics")

def random_rgb():
    return 'rgba('+str(random.randint(0, 256))+","+str(random.randint(0, 256))+","+str(random.randint(0, 256))+")"

@csrf_exempt
def startSession(request):

    if request.method != "POST":
        return HttpResponse(json.dumps({"message": "invalid sid"}),
                            content_type="application/json",
                            status=400)

    data = json.loads(request.body)

    cid = data.get("cid", "")
    sid = data.get("sid", "")
    url = data.get("url", None)
    ua = data.get("ua", None)

    sed = request.session.get("sed", None)

    log.debug("Starting session")
    if not sed:
        sed = Session()
        sed.save()
    else:
        sed = Session.find(sed)


    if sid == "":
        log.debug("No site id provided")
        return HttpResponse(json.dumps({"message": "invalid sid"}),
                            content_type="application/json")
    else:
        site = Site.objects.filter(sid=sid)
        if site.count() == 0:
            log.debug("Invalid site id "+sid)
            return HttpResponse(json.dumps({"message": "invalid sid"}),
                            content_type="application/json")
        site = site[0]

    client = Client.find(cid)
    if not client:
        return HttpResponse(json.dumps({"message": "invalid cid"}),
                            content_type="application/json")

    client.sessions.add(sed)

    if ua is not None:
        client.update_ua(ua)

    TrackHit.hit(client=client,
                 site=site,
                 categories=["start", "page-load"],
                 tags = [],
                 url=url,
                 message="start",
                 sed=sed
                 )

    return HttpResponse(json.dumps({"message": str(client.cid)}),
                        content_type="application/json")


@csrf_exempt
def track(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"message": "invalid sid"}),
                            content_type="application/json",
                            status=400)
    print(request.method)
    data = json.loads(request.body)

    cid = data.get("cid", "")
    sid = data.get("sid", "")
    message = data.get("message", "")
    url = data.get("url", None)
    properties = data.get("properties", [])
    cats = properties["categories"]
    tags = properties["tags"]



    sed = request.session.get("sed", None)

    log.debug("Starting session")
    if not sed:
        sed = Session()
        sed.save()
    else:
        sed = Session.find(sed)



    if sid == "":
        log.debug("No site id provided")
        return HttpResponse(json.dumps({"message": "invalid sid"}),
                            content_type="application/json")
    else:
        site = Site.objects.filter(sid=sid)
        if site.count() == 0:
            log.debug("Invalid site id "+sid)
            return HttpResponse(json.dumps({"message": "invalid sid"}),
                            content_type="application/json")
        site = site[0]

    client = Client.find(cid)
    if not client:
        return HttpResponse(json.dumps({"message": "invalid cid"}),
                            content_type="application/json")

    TrackHit.hit(client=client,
                 site=site,
                 categories=cats,
                 tags=tags,
                 url=url,
                 message=message,
                 sed=sed
                 )

    return HttpResponse(json.dumps({"message": str(client.cid)}),
                        content_type="application/json")


@report_authorization
def get_browser_data(request):


    field = request.GET.get("field", "description")
    sid = request.GET.get("sid", None)

    if not sid:
        return HttpResponse(json.dumps({
            "message": "Missing SID"
        }))

    site = Site.objects.filter(sid=sid)

    if site.count == 0:
        return HttpResponse(json.dumps({
            "message": "Invalid SID"
        }))

    data = Client.browserByHitCunt(sid, field=field)

    # TODO - pretty up the ugly timestamp
    labels = [point['browser']for point in data]
    data_totals = [point['total'] for point in data]
    bar_color = [random_rgb() for point in data]

    chartjs = {
        "dataset": [
            {
                "fill": False
            }
        ],
        "labels": labels,
        "datasets": [{
           "label": site[0].name,
            "fill": False,
            "data": data_totals,
            "borderColor": bar_color,
            "backgroundColor": bar_color,
            "borderWidth": 1
        }]
    }

    return HttpResponse(json.dumps(chartjs), content_type="application/json")

@report_authorization
def get_site_activity(request):
    by = request.GET.get("by", "hour")
    sid = request.GET.get("sid", None)
    # TODO - add support for range

    if not sid:
        return HttpResponse(json.dumps({
            "message": "Missing SID"
        }))

    site = Site.objects.filter(sid=sid)

    if site.count == 0:
        return HttpResponse(json.dumps({
            "message": "Invalid SID"
        }))

    data = site[0].activity(by=by)
    # TODO - pretty up the ugly timestamp
    labels = [point['time']for point in data]
    data = [point['hits'] for point in data]

    chartjs = {
        "dataset": [
            {
                "fill": False
            }
        ],
        "labels": labels,
        "datasets": [{
           "label": site[0].name,
            "fill": False,
            "data": data,
            "borderColor": [
                'rgba(255, 99, 132, 1)',
            ],
            "borderWidth": 3
        }]
    }


    return HttpResponse(json.dumps(
        chartjs,
        sort_keys=True,
        indent=1,
        cls=DjangoJSONEncoder
    ), content_type="application/json")




# grab all clients seen within X time period
#    foreach client
"""
        events [{
            'name': 'step 1'
            'tag1':<num hits>
            'tag2':<num hits>
        }, {
            'name': 'step 2'
            'tag 4': <num>
            'tag 9': <num>
        }]
        i = 0
        
        
        
        foreach step x
            if x in events[i]
                events[i]+=1
            else:
                events[i] = 1

"""