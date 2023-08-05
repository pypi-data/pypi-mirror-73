import json
import uuid
from django.db import models
from django.utils import timezone

UUID_16 = 16

def unique_id():
    """ Returns the first 8 bytes of unique id.
    """
    return uuid.uuid4().hex[:UUID_16]


class TimeStampedModel(models.Model):
    """
    # django abstract model class which defines

    - uuid16 primary key
    - created_on and modified_on date fields

    you may define your real model e.g.:

    class MyJsonModel(TimeStampedModel):
        ...
    """
    # created_on = models.DateTimeField(auto_now_add=True)
    # according to
    # http://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
    # auto_now_add is buggy - worked only once at a session.

    # 00a60ab62d004be2a93a5635e1014c51 -> 00a60ab62d004be2
    id = models.CharField(
        primary_key=True,
        max_length=UUID_16,
        default=unique_id,
        editable=False
    )

    created_on = models.DateTimeField(default=timezone.now, editable=False)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TimeStampedDataModel(TimeStampedModel):
    """
    # django abstract model class which defines

    - uuid16 primary key
    - created_on and modified_on date fields
    - a json field for custom data

    you may define your real model e.g.:

    class MyJsonModel(TimeStampedDataModel):
        obj_type = models.CharField(max_length=100)

        def __str__(self):
            return self.obj_type
    """

    # custom data
    json_data = models.TextField(blank=True)

    class Meta:
        abstract = True

    @property
    def data(self):
        if self.json_data:
            return json.loads(self.json_data)
        else:
            return {}

    @property
    def list_data(self):
        if self.json_data:
            return self.data
        else:
            return []

    @data.setter
    def data(self, data):
        self.json_data = json.dumps(data)
