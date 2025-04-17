from rest_framework import serializers
from .models import Habit
from .validators import validate_pleasant_habit_fields, validate_reward_or_linked_habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        habit = Habit(**data)
        validate_pleasant_habit_fields(habit)
        validate_reward_or_linked_habit(habit)
        return data
