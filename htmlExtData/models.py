# models.py
from django.db import models


class HourlyComplianceReport(models.Model):
    hour = models.IntegerField(primary_key=True)
    quantity_per_hour = models.IntegerField()
    total_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.hour} - {self.quantity_per_hour} - {self.total_quantity}"

    class Meta:
        db_table = 'HourlyComplianceReport'


class complianceReport(models.Model):
    id_entry = models.AutoField(primary_key=True)
    entryDate = models.CharField(max_length=50)
    entryTime = models.CharField(max_length=50)
    MvT = models.CharField(max_length=50)
    valType = models.CharField(max_length=50, null=True, blank=True)
    MvtTypeTxt = models.CharField(max_length=50)
    userName = models.CharField(max_length=30)
    material = models.CharField(max_length=50)
    quantity = models.CharField(max_length=20)
    EUn = models.CharField(max_length=10)
    LCAmount = models.CharField(max_length=50, null=True, blank=True)
    Crcy = models.CharField(max_length=50, null=True, blank=True)
    materialDescription = models.CharField(max_length=50)
    matDoc = models.CharField(max_length=50)
    plnt = models.CharField(max_length=50)
    numOrder = models.CharField(max_length=50)
    SLoc = models.CharField(max_length=10)
    batch = models.CharField(max_length=50)
    PO = models.CharField(max_length=30, null=True, blank=True)
    reas = models.CharField(max_length=50)
    pstngDate = models.CharField(max_length=50)
    costCtr = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id_entry} - {self.material}"

    class Meta:
        db_table = 'complianceReport'
