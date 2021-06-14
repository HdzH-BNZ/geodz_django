from django.urls import path, include
from .views import (
    buildingsList, buildingsDetail, departementDetail, testsList, testsNiveau, updateNiveaux, 
    updateStatutDetail, getAllTestsByID, getAllTestsByName, allListes, JoinLibelles, statutDetail,
    RegisterView, LoginView, UserView, LogOutView
    )

urlpatterns = [
    #path("", include(router.urls)),
    path("buildingsList/", buildingsList, name="buldingList"),
    path("allListes/", allListes, name="allListes"),
    path("JoinLibelles/", JoinLibelles, name="JoinLibelles"),
    path("buildingDetail/<int:pk>/", buildingsDetail, name="buildingDetail"),
    path("departementDetail/<str:nom_dep>/", departementDetail, name="departementDetail"),
    path("statutDetail/<int:key>/", statutDetail, name="statutDetail"),
    path("statutDetail/<int:key>/updateStatutDetail", updateStatutDetail, name="updateStatutDetail"),
    path("testsList/", testsList, name="testsList"),
    path("testsList/<int:pk_id_niveau>/niveau", testsNiveau, name="testNiveau"),
    path("testsList/<int:pk_id_niveau>/updateNiveau", updateNiveaux, name="updateNiveau"),
    path("testsList/allTestsByID/<int:id>/", getAllTestsByID, name="getAllTestsByID"),
    path("testsList/getAllTestsByName/<str:name>/", getAllTestsByName, name="getAllTestsByName"),
    path('register/', RegisterView, name="RegisterView"),
    path('login/', LoginView, name="LoginView"),
    path('user/', UserView, name="UserView"),
    path('logout/', LogOutView, name="LogOutView"),
]