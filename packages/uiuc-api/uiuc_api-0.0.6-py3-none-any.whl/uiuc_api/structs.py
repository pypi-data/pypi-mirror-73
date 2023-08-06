from enum import Enum
from yaml import dump


class Standing(Enum):
    """
    Simple class which represents class standing and provides comparisons
    """
    FRESHMAN = 0
    SOPHOMORE = 1
    JUNIOR = 2
    SENIOR = 3

    def __eq__(self, other):
        return self.value == other.value

    def __neq__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value


class Course:
    def __init__(self, subject, number, hours, label, description, schedule_info, standing,
                 prereqs, coreqs):
        """
        :param subject: subject name
        :param number: course number
        :param hours: number of credit hours course is
        :param label: label for the course
        :param description: description for the course
        :param schedule_info: info about course scheduling
        :param prereqs: tuple with list of prereqs and list of sets of prereq options
        :param coreqs: analogous to prereqs
        :param standing: standing required (None if no standing required, else Standing instance)
        """
        self.subject = subject
        self.number = number
        self.name = self.subject + self.number

        self.hours = hours
        self.label = label
        self.description = description
        self.schedule_info = schedule_info
        self.standing = standing

        self.direct_prereqs, self.prereq_sets = prereqs
        self.direct_coreqs, self.coreq_sets = coreqs

    def serialize(self):
        attrs = {k: v for k, v in self.__dict__.items() if k != self.name}
        return dump({self.name: attrs}, sort_keys=False)

    def __str__(self):
        return "<Course object <{}>>".format(self.name)

    def __repr__(self):
        return repr(self.__dict__)
