from django.contrib.gis import admin
from .models import BuildingsBis
from leaflet.admin import LeafletGeoAdmin

class BuildingsBisAdmin(LeafletGeoAdmin):
    # fields to show in admin listview
    list_display = ('id', 'data', 'the_geom')

# Register your models here.
admin.site.register(BuildingsBis, BuildingsBisAdmin)
