from django.http.response import HttpResponse
from django.http.response import JsonResponse
from rest_framework import serializers, viewsets, status
from .serializers import (
    BuildingsBisSerializer, DepartementSerializer, TestSerializer, LibelleBisSerializer, LibelleSerializer,
    StatutWorkflowSerializer, UserSerializer
)
from .models import (BuildingsBis, Departement, Libelle, Test, LibelleBis, StatutWorkflow, User)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from rest_framework.renderers import JSONRenderer
from django.core.serializers import serialize
from django.db.models import Count
import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.


@api_view(['POST'])
def RegisterView(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def LoginView(request):
    username = request.data['username']
    password = request.data['password']

    user = User.objects.filter(username=username).first()

    if user is None:
        raise AuthenticationFailed('Utilisateur non-trouvé')

    if not user.check_password(password):
        raise AuthenticationFailed('Mot de passe incorrect')

    payload= {
        "id" : user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }

    return response


@api_view(['GET'])
def UserView(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Non-authentifié')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Jeton expiré, vous êtes non-authentifié')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def LogOutView(request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "details" : "jeton supprimé avec succès"
        }
        return response


@api_view(['GET'])
def allListes(request):
    all_serializer = list()
    all_serializer.append(
        LibelleSerializer(
            Libelle.objects.raw("SELECT * FROM libelle;"), many=True
            ).data
        )
    all_serializer.append(
        LibelleBisSerializer(
            LibelleBis.objects.raw("SELECT * FROM libelle_bis;"), many=True
            ).data
        )
    #liste_count = LibelleBis.objects.count()
    liste_count = LibelleBis.objects.raw("SELECT * FROM libelle_bis;")
    all_serializer.append({'compteur' : len(list(liste_count))})
    return Response(all_serializer)

@api_view(['GET'])
def JoinLibelles(request):
    join_lib = Departement.objects.raw("SELECT d.id, d.nom_departement FROM departement AS d, libelle AS l WHERE d.id = l.pk_id;")
    serializer = DepartementSerializer(join_lib, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def buildingsList(request):
    buildings = BuildingsBis.objects.all()
    #buildings = BuildingsBis.objects.raw("SELECT b.id, b.data, %s FROM buildings_bis AS b;", ['b.the_geom'])
    serializer = BuildingsBisSerializer(buildings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def buildingsDetail(request, pk):
    try:
        building = BuildingsBis.objects.filter(id=pk)
    except BuildingsBis.DoesNotExist:
        return Response({
            "error": "Not found",
            "error_description": "Aucun élément trouvé"
        })
    else :
    #building = BuildingsBis.objects.raw("SELECT id, data AS nom, %s FROM buildings_bis WHERE id = %s;", ['the_geom', pk])
        serializer = BuildingsBisSerializer(building, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def departementDetail(request, nom_dep):
    departement = Departement.objects.get(nom_departement=nom_dep)
    serializer = DepartementSerializer(departement, many=False)
    return Response(serializer.data)

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def statutDetail(request, key):
    if request.method == 'GET':
        stat = StatutWorkflow.objects.get(cle=key)
        serializer = StatutWorkflowSerializer(stat, many=False)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['PATCH'])
def updateStatutDetail(request, key):
    #select statut à patch
    updated_statut = StatutWorkflow.objects.get(cle=key)
    #recup les data JSON à patch
    data = request.data

    serializer = StatutWorkflowSerializer(updated_statut, data, partial=True)
    if serializer.is_valid():
        #print(serializer.data)
        #print(JSONRenderer().render(serializer.data))
        #print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def testsList(request):
    tps1 = time.clock()
    test_liste = []
    #tests = Test.objects.all()
    
    #tests = Test.objects.filter(nom_structure='jawad').values('nom_structure')
    #tests = Test.objects.raw("SELECT id, id_niveau_test, id_libelle, nom_structure AS nom FROM test")
    #tests = Test.objects.filter(nom_structure='jawad')
    
    #tests = Test.objects.values('nom_structure').annotate(compteur=Count('nom_structure'))
    tests = Test.objects.filter(id_libelle=4).values(
        'nom_structure', #'id_libelle__libelle', 'id_niveau_test'
        ).annotate(
            compteur=Count('nom_structure') 
        ).order_by("compteur")
    print(tests)
    for test in tests:
        print(test)
        test_liste.append(test)
    #serializer = TestSerializer(tests, many=True)
    #return Response(serializer.data)
    print(test_liste)
    tps2 = time.clock()
    tps3 = tps2 - tps1
    return Response({
        "details" : "success",
        "temps1" : tps1,
        "temps2" : tps2,
        "temps d'exécution" : tps3,
        "reponse" : test_liste
    })
    #return Response(test_liste)

@api_view(['GET'])
def testsNiveau(request, pk_id_niveau):
    #libelles_niveau = LibelleBis.objects.get(id_niveau=pk_id_niveau)
    libelles_niveau = LibelleBis.objects.raw("SELECT * FROM libelle_bis WHERE id_niveau = %s", [int(pk_id_niveau)])
    serializer = LibelleBisSerializer(libelles_niveau, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllTestsByID(request, id):
    allTestsByID = Test.objects.filter(id_libelle = id)
    serializer = TestSerializer(allTestsByID, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllTestsByName(request, name):
    allTestsByName = Test.objects.filter(nom_structure = name)
    serializer = TestSerializer(allTestsByName, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def updateNiveaux(request, pk_id_niveau):
    niveaux = LibelleBis.objects.get(id_niveau=pk_id_niveau)
    serializer = LibelleBisSerializer(instance=niveaux, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

class BuildingsBisViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingsBisSerializer
    queryset = BuildingsBis.objects.all()

class DepartementViewSet(viewsets.ModelViewSet):
    serializer_class = DepartementSerializer
    queryset = Departement.objects.all()

class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    for e in queryset:
        print(e)