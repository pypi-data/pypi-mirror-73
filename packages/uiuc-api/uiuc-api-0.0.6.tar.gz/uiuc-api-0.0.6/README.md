About
=====
`uiuc-api` is a simple python package which wraps UIUC's official REST API for querying data about courses. In addition, it deals with some of the annoyances of using the official API by providing some convient structures. Data from the official API is available in XML form, however, it is in an inconvienent-to-parse format. For instance, take the XML data for CS 125:
```xml
<label>Discrete Structures</label>

<description>Discrete mathematical structures frequently encountered in the study of Computer Science. Sets, propositions, Boolean algebra, induction, recursion, relations, functions, and graphs. Credit is not given for both CS 173 and MATH 213. Prerequisite: One of CS 125, ECE 220; one of MATH 220, MATH 221.</description>

<creditHours>3 hours.</creditHours>

<courseSectionInformation>Credit is not given for both CS 173 and MATH 213. Prerequisite: One of CS 125, ECE 220; one of MATH 220, MATH 221.</courseSectionInformation>

<classScheduleInformation>Students must register for a lecture and discussion section.</classScheduleInformation>
```
It is tedious to accurately parse out the prerequisites in a easy-to-manipulate form. `uiuc-api` does this for the user:
```py
import uiuc_api as ua
repr(ua.get_course("CS 173"))
```
Output:
```py
Course(
    subject='CS',
    number='173',
    name='CS173',
    hours=3,
    label='Discrete Structures',
    description='Discrete mathematical structures frequently encountered in the study of Computer Science. Sets, propositions, Boolean algebra, induction, recursion, relations, functions, and graphs. Credit is not given for both CS 173 and MATH 213. Prerequisite: One of CS 125, ECE 220; one of MATH 220, MATH 221.',
    schedule_info='Students must register for a lecture and discussion section.',
    standing=None,
    direct_prereqs=[],
    prereq_sets=[{'ECE 220', 'CS 125'}, {'MATH 220', 'MATH 221'}],
    direct_coreqs=[],
    coreq_sets=[]
)

```
Installation
=========
Install the `uiuc_api`  module via pip:
```bash
pip install uiuc_api
```
Data Model
=========
`uiuc_api's` primary offering is the `Course` data structure which has the following attributes:
```py
"""  
:param subject: subject name  
:param number: course number
:param hours: number of credit hours course is
:param label: label for the course
:param description: description for the course  
:param schedule_info: course scheduling information
:param direct_prereqs: list of course names of direct prereqs
:param prereq_sets: list of sets each representing a "one of" option
:param direct_coreqs: analogous to direct_coreqs except for corequisite classes
:param coreq_sets: analogous to coreq_sets except for corequisite classes
:param standing: the standing required to take the course as a Standing enum (freshman, sophomore, junior senior)  
"""
```
`Course` objects also have a `serialize()` method which converts them to a YAML representation. `get_course` constructs a `Course` object from a name (e.g `CS 225`). `Standing` is a very simple enum datatype whose members are `Standing.FRESHMAN`, `Standing.SOPHMORE`, and so on. `Standing` also supports comparison, so e.g `Standing.SENIOR > Standing.FRESHMAN`.
