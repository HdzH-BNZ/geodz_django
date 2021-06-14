# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    '''
    class Meta:
        db_table = 'auth_user'
    '''
    first_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=150, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    

class BuildingsBis(models.Model):
    id = models.AutoField(primary_key=True)
    data = models.TextField(blank=True, null=True)
    the_geom = models.PolygonField(srid=2154, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'buildings_bis'
        verbose_name = 'building'


class Departement(models.Model):
    nom_departement = models.TextField(blank=True, null=True)
    code_departement = models.ForeignKey('StatDepartement', models.DO_NOTHING, db_column='code_departement')
    statut_workflow = models.ForeignKey('StatutWorkflow', models.DO_NOTHING, db_column='statut_workflow')

    class Meta:
        managed = False
        db_table = 'departement'

    def __str__(self):
        return self.nom_departement


class Detection(models.Model):
    nom = models.TextField(blank=True, null=True)
    id_detection = models.ForeignKey('DetectionContour', models.DO_NOTHING, db_column='id_detection')

    class Meta:
        managed = False
        db_table = 'detection'


class DetectionContour(models.Model):
    id_detection = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'detection_contour'


class Libelle(models.Model):
    pk_id = models.AutoField(primary_key=True)
    libelle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'libelle'


class LibelleBis(models.Model):
    id_niveau = models.AutoField(primary_key=True)
    libelle = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'libelle_bis'


class StatDepartement(models.Model):
    code_departement = models.TextField(unique=True)
    type_statistique = models.TextField(blank=True, null=True)
    valeur = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stat_departement'


class StatutWorkflow(models.Model):
    cle = models.IntegerField(unique=True)
    libelle = models.TextField()

    class Meta:
        managed = False
        db_table = 'statut_workflow'


class Test(models.Model):
    nom_structure = models.TextField(blank=True, null=True)
    id_libelle = models.ForeignKey(Libelle, models.DO_NOTHING, db_column='id_libelle')
    id_niveau_test = models.ForeignKey(LibelleBis, models.DO_NOTHING, db_column='id_niveau_test')

    class Meta:
        managed = False
        db_table = 'test'


class TestKb(models.Model):

    class Meta:
        managed = False
        db_table = 'test_kb'
