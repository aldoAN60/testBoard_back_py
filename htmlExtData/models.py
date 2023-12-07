# models.py
from django.db import models


from django.db import models

class HourlyComplianceReport(models.Model):
    """
    Modelo que representa los informes de cumplimiento por hora.

    Attributes:
        hour (IntegerField): La hora del informe (clave primaria).
        quantity_per_hour (IntegerField): Cantidad por hora en el informe.
        total_quantity (IntegerField): Cantidad total acumulada en el informe.
    """

    hour = models.IntegerField(primary_key=True)
    quantity_per_hour = models.IntegerField()
    total_quantity = models.IntegerField()

    def __str__(self):
        """
        Representación de cadena del objeto HourlyComplianceReport.

        Returns:
            str: Representación de cadena del objeto.
        """
        return f"{self.hour} - {self.quantity_per_hour} - {self.total_quantity}"

    class Meta:
        """
        Clase Meta para configuraciones adicionales del modelo.

        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
        """
        db_table = 'HourlyComplianceReport'



from django.db import models

class complianceReport(models.Model):
    """
    Modelo que representa un informe de cumplimiento.

    Attributes:
        id_entry (AutoField): Identificador único del informe.
        entryDate (CharField): Fecha de entrada del informe.
        entryTime (CharField): Hora de entrada del informe.
        MvT (CharField): Campo MvT del informe.
        valType (CharField): Tipo de valor del informe (opcional).
        MvtTypeTxt (CharField): Campo MvtTypeTxt del informe.
        userName (CharField): Nombre de usuario del informe.
        material (CharField): Material del informe.
        quantity (CharField): Cantidad del informe.
        EUn (CharField): Unidad de medida del informe.
        LCAmount (CharField, opcional): Monto en LC del informe (opcional).
        Crcy (CharField, opcional): Moneda del informe (opcional).
        materialDescription (CharField): Descripción del material del informe.
        matDoc (CharField): Documento de material del informe.
        plnt (CharField): Campo plnt del informe.
        numOrder (CharField): Número de orden del informe.
        SLoc (CharField): Campo SLoc del informe.
        batch (CharField): Lote del informe.
        PO (CharField, opcional): Orden de compra del informe (opcional).
        reas (CharField): Campo reas del informe.
        pstngDate (CharField): Fecha de contabilización del informe.
        costCtr (CharField): Centro de costos del informe.
    """

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
        """
        Representación de cadena del objeto ComplianceReport.

        Returns:
            str: Representación de cadena del objeto.
        """
        return f"{self.id_entry} - {self.material}"

    class Meta:
        """
        Clase Meta para configuraciones adicionales del modelo.

        Attributes:
            db_table (str): Nombre de la tabla en la base de datos.
        """
        db_table = 'complianceReport'

