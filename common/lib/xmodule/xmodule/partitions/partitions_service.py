"""
This is a service-like API that assigns tracks which groups users are in for various
user partitions.  It uses the user_service key/value store provided by the LMS runtime to
persist the assignments.
"""
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import logging

from openedx.core.lib.cache_utils import request_cached
from openedx.features.content_type_gating.partitions import create_content_gating_partition
from xmodule.partitions.partitions import (
    UserPartition,
    UserPartitionError,
    ENROLLMENT_TRACK_PARTITION_ID,
)
from xmodule.modulestore.django import modulestore


log = logging.getLogger(__name__)

FEATURES = getattr(settings, 'FEATURES', {})


@request_cached()
def get_all_partitions_for_course(course, active_only=False):
    """
    A method that returns all `UserPartitions` associated with a course, as a List.
    This will include the ones defined in course.user_partitions, but it may also
    include dynamically included partitions (such as the `EnrollmentTrackUserPartition`).

    Args:
        course: the course for which user partitions should be returned.
        active_only: if `True`, only partitions with `active` set to True will be returned.

        Returns:
            A List of UserPartitions associated with the course.
    """
    all_partitions = course.user_partitions + _get_dynamic_partitions(course)
    if active_only:
        all_partitions = [partition for partition in all_partitions if partition.active]
    return all_partitions


def _get_dynamic_partitions(course):
    """
    Return the dynamic user partitions for this course.
    If none exists, returns an empty array.
    """
    return [
        partition
        for partition in [
            _create_enrollment_track_partition(course),
            create_content_gating_partition(course),
        ]
        if partition
    ]


def _create_enrollment_track_partition(course):
    """
    Create and return the dynamic enrollment track user partition.
    If it cannot be created, None is returned.
    """
    if not FEATURES.get('ENABLE_ENROLLMENT_TRACK_USER_PARTITION'):
        return None

    try:
        enrollment_track_scheme = UserPartition.get_scheme("enrollment_track")
    except UserPartitionError:
        log.warning("No 'enrollment_track' scheme registered, EnrollmentTrackUserPartition will not be created.")
        return None

    used_ids = set(p.id for p in course.user_partitions)
    if ENROLLMENT_TRACK_PARTITION_ID in used_ids:
        log.warning(
            "Can't add 'enrollment_track' partition, as ID {id} is assigned to {partition} in course {course}.".format(
                id=ENROLLMENT_TRACK_PARTITION_ID,
                partition=_get_partition_from_id(course.user_partitions, ENROLLMENT_TRACK_PARTITION_ID).name,
                course=unicode(course.id)
            )
        )
        return None

    partition = enrollment_track_scheme.create_user_partition(
        id=ENROLLMENT_TRACK_PARTITION_ID,
        name=_(u"Enrollment Track Groups"),
        description=_(u"Partition for segmenting users by enrollment track"),
        parameters={"course_id": unicode(course.id)}
    )
    return partition


class PartitionService(object):
    """
    This is an XBlock service that returns information about the user partitions associated
    with a given course.
    """

    def __init__(self, course_id, cache=None):
        self._course_id = course_id
        self._cache = cache

    def get_course(self):
        """
        Return the course instance associated with this PartitionService.
        This default implementation looks up the course from the modulestore.
        """
        return modulestore().get_course(self._course_id)

    @property
    def course_partitions(self):
        """
        Return the set of partitions assigned to self._course_id (both those set directly on the course
        through course.user_partitions, and any dynamic partitions that exist). Note: this returns
        both active and inactive partitions.
        """
        return get_all_partitions_for_course(self.get_course())

    def get_user_group_id_for_partition(self, user, user_partition_id):
        """
        If the user is already assigned to a group in user_partition_id, return the
        group_id.

        If not, assign them to one of the groups, persist that decision, and
        return the group_id.

        Args:
            user_partition_id -- an id of a partition that's hopefully in the
                runtime.user_partitions list.

        Returns:
            The id of one of the groups in the specified user_partition_id (as a string).

        Raises:
            ValueError if the user_partition_id isn't found.
        """
        cache_key = "PartitionService.ugidfp.{}.{}.{}".format(
            user.id, self._course_id, user_partition_id
        )

        if self._cache and (cache_key in self._cache):
            return self._cache[cache_key]

        user_partition = self.get_user_partition(user_partition_id)
        if user_partition is None:
            raise ValueError(
                "Configuration problem!  No user_partition with id {0} "
                "in course {1}".format(user_partition_id, self._course_id)
            )

        group = self.get_group(user, user_partition)
        group_id = group.id if group else None

        if self._cache is not None:
            self._cache[cache_key] = group_id

        return group_id

    def get_user_partition(self, user_partition_id):
        """
        Look for a user partition with a matching id in the course's partitions.
        Note that this method can return an inactive user partition.

        Returns:
            A UserPartition, or None if not found.
        """
        return _get_partition_from_id(self.course_partitions, user_partition_id)

    def get_group(self, user, user_partition, assign=True):
        """
        Returns the group from the specified user partition to which the user is assigned.
        If the user has not yet been assigned, a group will be chosen for them based upon
        the partition's scheme.
        """
        return user_partition.scheme.get_group_for_user(
            self._course_id, user, user_partition, assign=assign,
        )


def _get_partition_from_id(partitions, user_partition_id):
    """
    Look for a user partition with a matching id in the provided list of partitions.

    Returns:
        A UserPartition, or None if not found.
    """
    for partition in partitions:
        if partition.id == user_partition_id:
            return partition

    return None
