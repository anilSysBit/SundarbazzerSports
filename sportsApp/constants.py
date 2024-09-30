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


class GOAL_TYPE(models.TextChoices):
    OPEN_PLAY = 'Open Play'
    HEADER = 'Header'
    PENALTY = 'Penalty Goal'
    FREE_KICK = 'Free-Kick Goal'
    OWN_GOAL = 'Own Goal'
    VOLLEY = 'Volley'
    TAP_IN = 'Tap-In'
    LONG_RANGE = 'Long-Range Goal'
    CHIP = 'Chip'
    BICYCLE_KICK = 'Bicycle Kick'