from rest_framework.serializers import CharField, ModelSerializer
from rest_framework.serializers import Serializer as DRFSerializer

from translate.models import Translation


class Deserializer(DRFSerializer):
    text_to_be_translated = CharField(required=True)
    target_language_code = CharField(required=False)
    source_language_code = CharField(required=False)
    translator = CharField(required=False)


class Serializer(ModelSerializer):
    class Meta:
        model = Translation
        fields = "__all__"
