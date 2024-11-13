from django.db import models

class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

class District(models.Model):
    province = models.ForeignKey(Province, related_name='districts', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.province.name if self.province else "No Province"})'

class Municipality(models.Model):
    district = models.ForeignKey(District, related_name='municipalities', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.district.name if self.district else "No District"})'

class Area(models.Model):
    municipality = models.ForeignKey(Municipality, related_name='areas', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.municipality.name if self.municipality else "No Municipality"})'
