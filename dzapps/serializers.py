from rest_framework import serializers
from rest_framework_gis.serializers import (GeoFeatureModelSerializer, GeoFeatureModelListSerializer)
from .models import (BuildingsBis, Departement, Test, LibelleBis, Libelle, StatutWorkflow, User)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'email', 'password', 'username']
        #pour cacher le mot de passe dans le retour du POST
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    #pour le haching :
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


#to get un vrai geoJSON avec un CRS :
class GeoFeatureModelListSerializerCRS(GeoFeatureModelListSerializer):
    def to_representation(self, instance):
        data=super().to_representation(instance)
        data.update({'crs':{
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:EPSG::2154"
            }
        }})
        data.move_to_end('crs', last = False)
        data.move_to_end('type', last = False)
        return data

class GeoFeatureModelSerializerCRS(GeoFeatureModelSerializer):
    @classmethod
    def many_init(cls, *args, **kwargs):
        child_serializer = cls(*args, **kwargs)
        list_kwargs = {'child': child_serializer}
        list_kwargs.update(
            {
                key: value
                for key, value in kwargs.items()
                if key in LIST_SERIALIZER_KWARGS
            }
        )
        meta = getattr(cls, 'Meta', None)
        list_serializer_class = getattr(
            meta, 'list_serializer_class', GeoFeatureModelListSerializerCRS
        )
        return list_serializer_class(*args, **list_kwargs)

    def to_representation(self, instance):
        data=super().to_representation(instance)
        return data


#liste des models à serializer et exporter vers views.py
class BuildingsBisSerializer(GeoFeatureModelSerializerCRS):
    name = serializers.CharField(source="data")

    class Meta():
        model = BuildingsBis
        geo_field = "the_geom"
        fields = ('id', 'name')

class DepartementSerializer(serializers.ModelSerializer):
    id_dep = serializers.CharField(source="code_departement")

    class Meta():
        model = Departement
        fields = ('id_dep', 'nom_departement', 'code_departement', 'statut_workflow')

class TestSerializer(serializers.ModelSerializer):
    compteur= serializers.IntegerField()
    libelle_content = serializers.CharField(source="id_libelle.libelle")

    class Meta():
        model = Test
        fields = '__all__'

class LibelleSerializer(serializers.ModelSerializer):

    class Meta():
        model = Libelle
        fields = '__all__'

class LibelleBisSerializer(serializers.ModelSerializer):

    class Meta():
        model = LibelleBis
        fields = '__all__'


class StatutWorkflowSerializer(serializers.ModelSerializer):

    class Meta():
        model = StatutWorkflow
        fields = ('id', 'cle', 'libelle')

    def create(self, validated_data):
        return StatutWorkflow.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.cle = validated_data.get('cle', instance.cle)
        instance.libelle = validated_data.get('libelle', instance.libelle)
        return super().update(instance, validated_data)
