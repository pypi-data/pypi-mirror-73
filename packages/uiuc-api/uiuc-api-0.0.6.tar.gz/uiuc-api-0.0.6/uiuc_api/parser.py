import requests
import re
from lxml import etree as ET
from .structs import Course, Standing

COURSE_PATTERN = r"[A-Z]+ \d+"

# c is a placeholder for course pattern
REQ_SET_PATTERNS = (r"c/c", r"c(?:, c)* or c", r"[Oo]ne of c(?:, c)*")
DIRECT_REQ_PATTERNS = (r"c(?:, c)* and c", r"c")
REQ_PATTERNS = REQ_SET_PATTERNS + DIRECT_REQ_PATTERNS

XML_DATA = ("creditHours", "label", "description", "classScheduleInformation")


def get_course_xml(subject, number, year="2020", semester="spring"):
    url = "http://courses.illinois.edu/cisapp/explorer/catalog/{year}/{semester}/{subject}/{number}.xml"
    url = url.format(year=year, semester=semester, subject=subject, number=number)
    xml_raw = requests.get(url).content
    try:
        parsed = ET.fromstring(xml_raw)
    except ET.XMLSyntaxError:
        raise ValueError("Course {} does not exist".format(subject + number))

    course_info = {key: None for key in XML_DATA}
    course_info.update({child.tag: child.text for child in parsed})
    return course_info


def get_course(course_name):
    """
    returns parsed Course object
    :param course_name: name of course, e.g CS 225
    :return: Course object
    """
    course_name = course_name
    if not re.match(COURSE_PATTERN, course_name):
        raise ValueError(
            "Incorrect format passed for course_name. Make sure you are using e.g CS 225 and not CS225.")

    subject, number = course_name.split()
    subject = subject.upper()

    course_info = get_course_xml(subject, number)
    hours = int(re.search(r"\d+", course_info["creditHours"]).group())

    label = course_info["label"]
    description = course_info["description"]
    schedule_info = course_info["classScheduleInformation"]
    standing_match = re.search(r"(\w+) standing", description)
    if standing_match:
        standing = Standing[standing_match.group(1).upper()]
    else:
        standing = None

    redirect = re.search("See ({})".format(COURSE_PATTERN), description)
    if redirect:
        return get_course(redirect.group(1))
    else:
        prereqs, coreqs = [], []
        if re.search(r"Prerequisite:(.*)\.", description):
            prereqs, coreqs = parse_prereqs(re.search(
                r"Prerequisite:(.*)\.",
                description
            ).group())

        return Course(
            subject=subject,
            number=number,
            hours=hours,
            label=label,
            description=description,
            schedule_info=schedule_info,
            standing=standing,
            prereqs=prereqs,
            coreqs=coreqs
        )


def parse_prereqs(req_info):
    """
    Takes in prerequisite string and parses into tuple of course names
    :param req_info: the part of the course xml after the 'Prerequisite:'
    :return: tuple of course names -- sets represent a 'one of' option
              e.g (CS 125, {Math 221, Math 222}) means 'CS 125' and one of Math 221/222
    """
    # normal prereqs
    direct_prereqs = []
    direct_coreqs = []
    # prereqs of the form "one of a or b"
    prereq_sets = []
    coreq_sets = []
    # conditions are delimited by semicolons
    for req_condition in req_info.split(";"):
        for pattern in REQ_PATTERNS:
            m = re.search(pattern.replace("c", COURSE_PATTERN), req_condition)
            if m:
                courses = set(re.findall(COURSE_PATTERN, m.group()))
                if "credit or concurrent" in req_condition:
                    if pattern in REQ_SET_PATTERNS:
                        coreq_sets.append(courses)
                    else:
                        direct_coreqs.extend(courses)
                else:
                    if pattern in REQ_SET_PATTERNS:
                        prereq_sets.append(courses)
                    else:
                        direct_prereqs.extend(courses)
                break
    return (direct_prereqs, prereq_sets), (direct_coreqs, coreq_sets)
