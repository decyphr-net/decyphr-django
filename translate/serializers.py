from rest_framework.serializers import CharField, ModelSerializer
from rest_framework.serializers import Serializer as DRFSerializer

from .models import Translation


class Deserializer(DRFSerializer):
    text_to_be_translated = CharField(required=True)
    target_language_code = CharField(required=True)
    source_language_code = CharField(required=True)
    translator = CharField(required=True)


class Serializer(ModelSerializer):
    class Meta:
        model = Translation
        fields = "__all__"
