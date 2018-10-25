"""
API Serializers
"""
from collections import defaultdict

from rest_framework import serializers


# pylint: disable=abstract-method
class GradingPolicySerializer(serializers.Serializer):
    """
    Serializer for course grading policy.
    """
    assignment_type = serializers.CharField(source='type')
    count = serializers.IntegerField(source='min_count')
    dropped = serializers.IntegerField(source='drop_count')
    weight = serializers.FloatField()

    def to_representation(self, instance):
        """
        Return a representation of the grading policy.
        """
        # Backwards compatibility with the behavior of DRF v2.
        # When the grader dictionary was missing keys, DRF v2 would default to None;
        # DRF v3 unhelpfully raises an exception.
        return dict(
            super(GradingPolicySerializer, self).to_representation(
                defaultdict(lambda: None, instance)
            )
        )


class SectionBreakdownSerializer(serializers.Serializer):
    """
    Serializer for the `section_breakdown` portion of a gradebook entry.
    """
    are_grades_published = serializers.BooleanField()
    auto_grade = serializers.BooleanField()
    category = serializers.CharField()
    chapter_name = serializers.CharField()
    comment = serializers.CharField()
    detail = serializers.CharField()
    displayed_value = serializers.CharField()
    is_graded = serializers.BooleanField()
    grade_description = serializers.CharField()
    is_ag = serializers.BooleanField()
    is_average = serializers.BooleanField()
    is_manually_graded = serializers.BooleanField()
    label = serializers.CharField()
    letter_grade = serializers.CharField()
    module_id = serializers.CharField()
    percent = serializers.FloatField()
    score_earned = serializers.FloatField()
    score_possible = serializers.FloatField()
    section_block_id = serializers.CharField()
    subsection_name = serializers.CharField()


class SimpleSerializer(serializers.BaseSerializer):
    """
    A Serializer intended to take a dictionary of data and simply spit
    that same dictionary back out as the "serialization".
    """
    def to_representation(self, instance):
        return instance


class StudentGradebookEntrySerializer(serializers.Serializer):
    """
    Serializer for student gradebook entry.
    """
    course_id = serializers.CharField()
    email = serializers.CharField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    full_name = serializers.CharField()
    passed = serializers.BooleanField()
    percent = serializers.FloatField()
    letter_grade = serializers.CharField()
    progress_page_url = serializers.CharField()
    section_breakdown = SectionBreakdownSerializer(many=True)
    aggregates = SimpleSerializer()
