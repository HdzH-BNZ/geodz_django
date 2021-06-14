from  django_filters import filters
from .models import Departement

class DepartementFilter():
    filteredBuilding = filters.CharFilter(method = 'get_one_building_per_name')

    class Meta:
        model = BuildingsBis


    def get_one_building_per_name(self, queryset, name):
        query_ = BuildingsBis.objects.filter(nom=name)
        if query_:
            obj = query_.first()
            return queryset.filter(geom_within = obj.geom)
        return queryset