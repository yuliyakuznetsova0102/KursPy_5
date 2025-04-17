from django.core.exceptions import ValidationError


def validate_pleasant_habit_fields(habit):
    if habit.is_pleasant:
        if habit.reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")
        if habit.linked_habit:
            raise ValidationError("У приятной привычки не может быть связанной привычки.")


def validate_reward_or_linked_habit(habit):
    if habit.reward and habit.linked_habit:
        raise ValidationError("Нельзя указывать одновременно вознаграждение и связанную привычку.")

    if habit.linked_habit and not habit.linked_habit.is_pleasant:
        raise ValidationError("В связанные привычки могут попадать только привычки с признаком приятной привычки.")
