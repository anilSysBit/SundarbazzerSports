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


class PLAYER_POSITION(models.TextChoices):
    GOALKEEPER = 'GK', 'Goalkeeper'
    RIGHT_BACK = 'RB', 'Right Back'
    LEFT_BACK = 'LB', 'Left Back'
    LEFT_CENTER_BACK = 'LCB', 'Left Center Back'
    RIGHT_CENTER_BACK = 'RCB', 'Right Center Back'
    LEFT_MIDFIELDER = 'LM', 'Left Midfielder'
    RIGHT_MIDFIELDER = 'RM', 'Right Midfielder'
    RIGHT_WINGER = 'RW', 'Right Winger'
    LEFT_WINGER = 'LW', 'Left Winger'
    LEFT_CENTER_FORWARD = 'LCF', 'Left Center Forward'
    RIGHT_CENTER_FORWARD = 'RCF', 'Right Center Forward'


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

class BLOOD_GROUPS(models.TextChoices):
    A_POSITIVE = 'A+'
    A_NEGATIVE = 'A-'
    B_POSITIVE = 'B+'
    B_NEGATIVE = 'B-'
    AB_POSITIVE = 'AB+'
    AB_NEGATIVE = 'AB-'
    O_POSITIVE = 'O+'
    O_NEGATIVE = 'O-'


class EventStatus(models.TextChoices):
    INITIATED = 'Initiated'
    REGISTRATION = 'Registration'
    RUNNING = 'Running'
    INTERRUPTED = 'Interrupted'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'


class MatchStatus(models.TextChoices):
    INITIATED = 'Initiated'
    RUNNING = 'Running'
    INTERRUPTED = 'Interrupted'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'

class EVENT_TYPE (models.TextChoices):
        LEAGUE='League'
        KNOCKOUT='Knockout'
        FRIENDLY='Friendly'



class FoulChoices(models.TextChoices):
    HAND_BALL = 'HAND_BALL', 'Hand Ball'
    OFFSIDE = 'OFFSIDE', 'Offside'
    DANGEROUS_PLAY = 'DANGEROUS_PLAY', 'Dangerous Play'
    PUSHING = 'PUSHING', 'Pushing'
    TRIPPING = 'TRIPPING', 'Tripping'
    UNSPORTING_BEHAVIOR = 'UNSPORTING_BEHAVIOR', 'Unsporting Behavior'
    OBSTRUCTION = 'OBSTRUCTION', 'Obstruction'
    ILLEGAL_TACKLE = 'ILLEGAL_TACKLE', 'Illegal Tackle'
    OTHER = 'OTHER', 'Other'


class FoulCategory(models.TextChoices):
    NORMAL_FALL = 'NORMAL_FALL', 'Normal Fall'
    YELLOW_CARD = 'YELLOW_CARD', 'Yellow Card'
    RED_CARD = 'RED_CARD', 'Red Card'


class PlayerEventStatusType(models.TextChoices):
    FREEKICK = 'FREEKICK', 'FreeKick'
    CORNER = 'CORNER', 'Corner'
    PENALTY = 'PENALTY', 'Penalty'
    OFFSIDE = 'OFFSIDE', 'Offside'
    INJURY = 'INJURY', 'Injury'