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
    GOAL_KEEPER = 'GK', 'Goal_Keeper'  # Stored as 'GK', displayed as 'Goal Keeper'
    DEFENSE_CENTER_LEFT = 'LCB', 'Defense Center-Left'  # LCB stays the same
    DEFENSE_CENTER_RIGHT = 'RCB', 'Defense Center-Right'
    DEFENSE_LEFT = 'LB', 'Defense Left'
    DEFENSE_RIGHT = 'RB', 'Defense Right'
    MIDDLE_LEFT = 'LM', 'Middle Left'
    MIDDLE_RIGHT = 'RM', 'Middle Right'
    FRONT_RIGHT = 'RW', 'Front Right'
    FRONT_LEFT = 'LW', 'Front Left'
    FRONT_CENTER_LEFT = 'LCF', 'Front Center-Left'
    FRONT_CENTER_RIGHT = 'RCF', 'Front Center-Right'


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
    ONGOING = 'Ongoing'
    INTERRUPTED = 'Interrupted'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'
    SCHEDULED = 'Scheduled'
    EXPIRED = 'Expired'

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