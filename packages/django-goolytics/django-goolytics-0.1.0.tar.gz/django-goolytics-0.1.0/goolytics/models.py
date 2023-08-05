import datetime
import logging
import operator
import sys
import uuid
from functools import reduce
from django.db import models
from django.db.models import Q, Count, F

log = logging.getLogger("lytics")


def fetch_list(values, model_name, attribute_name="name"):
    if not values:
        print("returning no values")
        return None

    mod_class = getattr(sys.modules[__name__], model_name)

    results = mod_class.objects.filter(**{attribute_name + "__in": values})

    if results.count() >= len(values):  # > in case there are duplicates
        return results
    else:
        tag_results = set(results.values_list(attribute_name, flat=True))
        to_create = set(values) - tag_results
        additions = []
        for attribute in to_create:
            logging.debug("Creating new model " + model_name + ":" + str(attribute))
            additions.append(mod_class(**{attribute_name: attribute}))
        mod_class.objects.bulk_create(additions)

        return mod_class.objects.filter(**{attribute_name + "__in": values})


class Session(models.Model):
    """
        Represents a clients particular 'session' on a site. Should
            expire after tab close or expiration time period. IE: If
            user X, re-visits site. We should track their behavior as
            a new session and not one long continuous session.
    """
    sed = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    last_seen = models.DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def find(sed):
        s = Session.objects.filter(sed=sed)
        if len(s) == 0:
            s = Session()
            s.save()
            return s
        return s[0]


    """
        LOH
        how to tell if a sesison ended
        how to sort hits by session in onrder to generate the 'story board' 
    
    """


class Client(models.Model):
    """
        Tries to be the most consistent representation of a particular person
    """
    cid = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    first_seen = models.DateTimeField(default=datetime.datetime.now)
    last_seen = models.DateTimeField(default=datetime.datetime.now)

    # User Agent parsing
    description = models.CharField(max_length=256, blank=True, null=True)
    layout = models.CharField(max_length=256, blank=True, null=True)
    manufacturer = models.CharField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    prerelease = models.CharField(max_length=256, blank=True, null=True)
    product = models.CharField(max_length=256, blank=True, null=True)
    ua = models.CharField(max_length=256, blank=True, null=True)
    version = models.CharField(max_length=256, blank=True, null=True)
    architecture = models.CharField(max_length=256, blank=True, null=True)
    family = models.CharField(max_length=256, blank=True, null=True)
    version = models.CharField(max_length=256, blank=True, null=True)

    sessions = models.ManyToManyField(Session)

    @staticmethod
    def uniqueSessions(field='name'):
        return Client.objects.all().values(field).annotate(total=Count(field)).order_by('total')

    @staticmethod
    def browserByHitCunt(sid, field='name'):
        return TrackHit.objects.exclude(client__description=None).filter(site__sid=sid).values('client__description') \
            .annotate(total=Count('client__description'),
                      browser=F('client__description'),)\
            .order_by('-total').values("browser", "total")

    @staticmethod
    def find(cid=""):
        if cid == "":
            client = Client.objects.create()
            log.debug("Created new client")
        else:
            client = Client.objects.filter(cid=cid)
            if client.count() == 0:
                log.debug("Invalid client id:" + cid)
                return None
            client = client[0]

        return client

    def update_ua(self, ua):
        self.description = ua["description"]
        self.layout = ua["layout"]
        self.manufacturer = ua["manufacturer"]
        self.name = ua["name"]
        self.prerelease = ua["prerelease"]
        self.product = ua["product"]
        self.ua = ua["ua"]
        self.version = ua["version"]
        self.architecture = ua["os"]["architecture"]
        self.family = ua["os"]["family"]
        self.version = ua["os"]["version"]
        self.save()

    def __str__(self):
        return self.cid


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=32)
    sid = models.CharField(max_length=64, default=uuid.uuid4)

    def activity(self, by="hour", range=datetime.datetime.now() - datetime.timedelta(14)):
        results = TrackHit.objects.filter(site=self, time__gte=range).extra({"time": "date_trunc('" + by + "', time)"}). \
            values("time").order_by().annotate(hits=Count("id"))

        return results

    def __str__(self):
        return self.name


class TrackHit(models.Model):
    message = models.CharField(max_length=32)
    categories = models.ManyToManyField(Category, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    url = models.CharField(max_length=512, default="None", blank=True, null=True)
    time = models.DateTimeField(default=datetime.datetime.now)

    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)
    #   rely on client to refresh session
    #   start new session if non given or last seen se

    @staticmethod
    def hit(client, site, message, categories, tags, sed, url=None):
        """

        :param client:
        :param site:
        :param message:
        :param categories:
        :param tags:
        :return:
        """

        tags = fetch_list(tags, model_name="Tag", attribute_name="name")
        cats = fetch_list(categories, model_name="Category")

        t = TrackHit.objects.create(message=message,
                                    site=site,
                                    client=client,
                                    url=url,
                                    session=sed)
        if categories:
            logging.debug("set cats: ", cats)
            t.categories.set(cats)
        if tags:
            logging.debug("set tags: ", tags)
            t.tags.set(tags)
        t.save()

        client.last_seen = datetime.datetime.now()
        client.save()

        return t

    def __str__(self):
        return str(self.client) + "  :  " + str(self.site) + \
               " : " + self.message + " " + str(self.tags) + " | " + str(self.categories) + "@" + str(self.time)


class ErrorHit(models.Model):
    message = models.CharField(max_length=32)
    site = models.ForeignKey(Site, on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)


