from django.db import models


class GENDER_OPTIONS():
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHERS = 'OTHERS'

    CHOICES = (
        (MALE,'Male'),
        (FEMALE,'Female'),
        (OTHERS,'Others')
    )


class POSITION_OPTIONS(models.TextChoices):
    pass