import re
import datetime
from io import StringIO
from html.parser import HTMLParser
import uuid
# Django
from .models import Schedules, Sections, Subjects, InstructionMediums, Instructors, Courses, Locations, Terms
import json
from html import unescape

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()

def _strip_tags(html):
    s = MLStripper()
    html = html.split("<body>")[1]
    html = html.split("</body>")[0]
    html = html.replace("&amp;", "&")
    # Clean &amp; and such
    html = re.sub(re.compile('&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'), '', html)
    s.feed(html)
    return s.get_data()


def parseData(file, termname):
    # req = requests.get(url)
    # req.encoding = 'utf-8'
    # f = open(filename)
    decode = unescape(str(file.read().decode("ISO 8859-1")))
    rawDataList = re.split(r"-----------------*", _strip_tags(decode))


    #Make a Term
    try:
        term = Terms.objects.get(name=termname)
        termUUID = term.id
    except Terms.DoesNotExist:
        termUUID = uuid.uuid4()
    instructors = list(Instructors.objects.all().values())
    courses = list(Courses.objects.all().values())
    subjects = list(Subjects.objects.all().values())
    mediums = list(InstructionMediums.objects.all().values())
    sections = list(Sections.objects.all().values())
    schedules = list()
    locations = list(Locations.objects.all().values())

    # termUUID = uuid.uuid4()
    # instructors = list()
    # courses = list()
    # subjects = list()
    # mediums = list()
    # sections = list()
    # schedules = list()
    # locations = list()


    o_instructors = list(instructors)
    o_courses = list(courses)
    o_subjects = list(subjects)
    o_mediums = list(mediums)
    o_sections = list(sections)
    o_locations = list(locations)


    courseSubject = ""
    failed = []
    for item in rawDataList:
        item = str(item)

        easyString = item.replace("\n", "‼").replace("\t", "⁇").replace("  ", "±")
        pattern = r"(.*)\s+⁇([A-Z0-9\s\/@.±:&,-∩┐╜']*)‼⁇⁇⁇⁇⁇⁇⁇⁇\s?([A-Z].*)"

        match = re.match(pattern, easyString)

        if match:
            courseCode = match.group(1)
            if courseCode.find("‼‼") > -1:
                courseSubject = courseCode.split("‼‼")[0].replace("‼", "")
                courseCode = courseCode.split("‼‼")[1]
            elif courseCode.find("‼⁇") > -1:
                courseSubject = courseCode.split("‼⁇")[0].replace("‼", "")
                courseCode = courseCode.split("‼⁇")[1]

            courseCode = courseCode.replace(
                "‼", "").replace("±", " ").replace("⁇", "")
            try:
                ############################
                # Database Subjects Insert
                if courseCode.split(" ")[0] not in [v['id'] for v in subjects]:
                    subjects.append(dict(name=courseSubject, id=courseCode.split(" ")[0]))
                ###########################
            except:
                raise ValueError(subjects)
            courseName = match.group(2)
            courseCredit = 0.0
            if "±" in courseName:
                lastE = courseName.split("±")[-1].strip()
                try:
                    courseCredit = float(lastE)
                    courseName = courseName.split("±")[-2]
                except ValueError:
                    pass
            elif "⁇" in courseName:
                lastE = courseName.split("⁇")[-1].strip()
                try:
                    courseCredit = float(lastE)
                    courseName = courseName.split("⁇")[-2]
                except ValueError:
                    pass
            coursePreReqs = match.group(3).split("‼‼⁇")[0]
            coursePreReqs = re.sub(r"\s+", " ", coursePreReqs.replace("⁇", " ").replace("‼", " "))

            #############################
            # Database Course Insert
            if (courseName,courseCode.split(" ")[1]) not in [(v['name'],v['code']) for v in courses]:
                courseUUID = uuid.uuid4()
                courses.append(dict(
                            id=courseUUID,
                            code=courseCode.split(" ")[1],
                            name=courseName,
                            credits=courseCredit,
                            subject=courseCode.split(" ")[0],
                            prereqs=coursePreReqs.replace("Prerequisite(s):","").split("Corequisite(s):")[0].replace("±", " ").strip(),
                            coreqs=coursePreReqs.split("corequisite(s):")[1].replace("±", " ").strip() if "corequisite(s):" in coursePreReqs else "",
                            note=""))
            else:
                courseUUID = next(item for item in courses if item["name"] == courseName and  item["code"] == courseCode.split(" ")[1])['id']
            ############################

            tJ = match.group(3)[match.group(3).find("‼‼⁇"):]
            sects = tJ.split("‼‼⁇⁇")
            raw = tJ.replace("±", "  ").replace("⁇", "\t").replace("‼", "\n")
            pattern = r'([0-9]*)\s([A-Z#]{1,3}[0-9]{0,4})\s([\D\s.]*)\t([A-Z][A-Z0-9-\s]*)\s\s+([A-Za-z0-9\':&\s]*)(I[A-Za-z0-9-.,&:\s]*)'


            for sect in sects:
                bb = sect.strip()
                sect = sect.replace("UFV⁇","UFV±± ",1).replace("M⁇","M",1).replace("T⁇","T",1).replace("W⁇","W",1).replace("R⁇","R",1).replace("F⁇","F",1).replace("S⁇","S",1).replace("⁇⁇⁇⁇ ONLINE UFV","⁇⁇±⁇ONLINE UFV")
                sect = sect.replace("±", "  ").replace("⁇", "\t").replace("‼", "\n")
                matches = re.findall(pattern, sect)
                if matches:
                    for match in matches:
                        sectionDict = dict()
                        sectionDict['sectionCRN'] = match[0]
                        sectionDict['sectionName'] = match[1]
                        sectionDict['sectionProf'] = re.sub(r"[\n\t]*", "", match[2]).strip()
                        ###########################
                        # Instructors Database List
                        if sectionDict['sectionProf'] not in [v['name'] for v in instructors]:
                            instructorUUID = uuid.uuid4()
                            instructors.append(dict(
                                id=instructorUUID,
                                name=sectionDict['sectionProf']
                                )
                            )
                        else:
                            instructorUUID = next(item for item in instructors if item["name"] == sectionDict['sectionProf'])['id']
                        ############################
                        sectionDict['sectionSchedule'] = []
                        enrolled = 0;
                        for sch in match[3].split("\n"):
                            timePattern = r'([0-9]{4}\s[0-9]{4})'
                            datePattern = r'([0-9]{2}-[A-Z]{3}-[0-9]{4}\s+[0-9]{2}-[A-Z]{3}-[0-9]{4})'
                            locationPattern = r'([A-Z#]{2,10}\s+[A-Z0-9]{2,5})'
                            subSectDict = dict()
                            matchTime = re.findall(timePattern, sch)
                            if matchTime and len(matchTime) > 0:
                                subSectDict['time'] = matchTime[0]
                            else:
                                subSectDict['time'] = "-"
                            matchDate = re.findall(datePattern, sch)
                            if matchDate and len(matchDate) > 0:
                                subSectDict['date'] = matchDate[0]
                            else:
                                subSectDict['date'] = ""
                            matchLocation = re.findall(locationPattern, sch)
                            if matchLocation and len(matchLocation) > 0:
                                subSectDict['location'] = matchLocation[0]
                            else:
                                subSectDict['location'] = ""
                            leftover = sch.replace(subSectDict['time'], "").replace(
                                subSectDict['date'], "").replace(subSectDict['location'], "")
                            subSectDict['days'] = leftover.replace(
                                "\t", "").replace(" ", "")
                            subSectDict['days'] = ''.join(
                                [i for i in subSectDict['days'] if not i.isdigit()])
                            subSectDict['enrolled'] = leftover.replace(
                                "\t", "").replace(" ", "").replace(
                                subSectDict['days'], "")
                            subSectDict['time'] = subSectDict['time'].replace(
                                "\t", "-")
                            if len(subSectDict['days']) > 0:
                                sectionDict['sectionSchedule'].append(subSectDict)
                            try:
                                enrolled = max(int(enrolled),int(subSectDict['enrolled'].strip()))
                            except ValueError:
                                pass
                            ##########################
                            ### Database Location List
                            if len(subSectDict['location']) > 0:
                                if subSectDict['location'] == "ONLINE UFV":
                                    campus = subSectDict['location']
                                    building = ""
                                    room = ""
                                else:
                                    try:
                                        campus = subSectDict['location'].split(" ")[0][:-1]
                                        building = subSectDict['location'].split(" ")[0][-1]
                                        room= subSectDict['location'].split(" ")[1]
                                    except IndexError:
                                        campus = "TBA"
                                        building = ""
                                        room = ""
                                try:
                                    locationUUID = next(item for item in locations if item["campus"] == campus and item["building"] == building and item["room"] == room)['id']
                                except (StopIteration, KeyError):
                                    locationUUID = uuid.uuid4()
                                    locations.append(dict(
                                        id=locationUUID,
                                        campus=campus,
                                        building=building,
                                        room=room
                                    ))
                                # Database Schedule Insert
                                if set("aeiou").isdisjoint(subSectDict['days'].lower()):
                                    # MTWRFSS does not contain vowel, but month names do
                                    for d in list(subSectDict['days']):
                                        schedules.append(dict(
                                            id=uuid.uuid4(),
                                            location=locationUUID,
                                            crn=sectionDict['sectionCRN'],
                                            weekday=d,
                                            time_start=subSectDict['time'].split("-")[0].strip() or 0,
                                            time_end=subSectDict['time'].split("-")[1].strip() or 0,
                                            date_start=datetime.datetime.strptime((subSectDict['date'].split(" ")[0]),'%d-%b-%Y').strftime('%Y%m%d'),
                                            date_end=datetime.datetime.strptime((subSectDict['date'].split(" ")[1]),'%d-%b-%Y').strftime('%Y%m%d'),
                                            is_weekly=(subSectDict['date'].split(" ")[0] != subSectDict['date'].split(" ")[1])
                                        ))
                                else:
                                    schedules.append(dict(
                                            id=uuid.uuid4(),
                                            location=locationUUID,
                                            crn=sectionDict['sectionCRN'],
                                            weekday="",
                                            time_start=subSectDict['time'].split("-")[0].strip() or 0,
                                            time_end=subSectDict['time'].split("-")[1].strip() or 0,
                                            date_start=datetime.datetime.strptime((subSectDict['date'].split(" ")[0]),'%d-%b-%Y').strftime('%Y%m%d'),
                                            date_end=datetime.datetime.strptime((subSectDict['date'].split(" ")[1]),'%d-%b-%Y').strftime('%Y%m%d'),
                                            is_weekly=(subSectDict['date'].split(" ")[0] != subSectDict['date'].split(" ")[1])
                                        ))
                            #######################
                        ## - for loop ends -
                        sectionDict['sectionInfo'] = match[4].replace(
                            "\t\t\t\t\t\t\t\t\t\t\t\t", ".").replace("\t", " ").replace("\n", "")
                        if len(match) > 5:
                            splitForNotes = (match[5].replace(
                                "\n", ".").replace("\t", " ").replace("..", ".").strip()).split(".")
                            sectionDict['sectionMedium'] = splitForNotes[0]
                            sectionDict['sectionNotes'] = ""
                            if len(splitForNotes) > 1:
                                sectionDict['sectionNotes'] = (".".join(splitForNotes[1:])).strip()
                        else:
                            sectionDict['sectionMedium'] = ""
                            sectionDict['sectionNotes'] = ""

                        #######################
                        ## Medium Database List
                        if sectionDict['sectionMedium'] not in [v['name'] for v in mediums]:
                            mediumUUID = uuid.uuid4()
                            mediums.append(dict(
                                id=mediumUUID,
                                name=sectionDict['sectionMedium']
                                )
                            )
                        else:
                            mediumUUID = next(item for item in mediums if item["name"] == sectionDict['sectionMedium'])['id']
                        #######################

                        #######################
                        ## Section Insert
                        if int(sectionDict['sectionCRN'].strip()) not in [int(v['crn']) for v in sections]:
                            sections.append(dict(
                                crn=sectionDict['sectionCRN'],
                                instructor=instructorUUID,
                                name=sectionDict['sectionName'],
                                course=courseUUID,
                                term=termUUID,
                                medium=mediumUUID,
                                is_lab=("#" in sectionDict['sectionName']),
                                enrolled=-1,
                                capacity=enrolled,
                                note=sectionDict['sectionInfo'] + "//" + sectionDict['sectionNotes'].replace("No meeting times.","")
                            ))
                        #######################
                else:
                    failed.append(bb)

    try:
        Terms.objects.create(
            id=termUUID,
            name=termname
        )
    except:
        pass
    for instructor in instructors:
        if instructor['name'] not in [v['name'] for v in o_instructors]:
            Instructors.objects.create(id=instructor['id'],name=instructor['name'])
    for medium in mediums:
        if medium['name'] not in [v['name'] for v in o_mediums]:
            InstructionMediums.objects.create(id=medium['id'],
                            name=medium['name'])
    for subject in subjects:
        if subject['name'] not in [v['name'] for v in o_subjects]:
            Subjects.objects.create(id=subject['id'],name=subject['name'])
    for course in courses:
        if course['code']+course['name'] not in [v['code']+v['name'] for v in o_courses]:
            Courses.objects.create(id=course['id'],
                    code=course['code'],
                    name=course['name'],
                    credits=course['credits'],
                    subject=Subjects.objects.get(id=course['subject']),
                    prereqs=course['prereqs'],
                    coreqs=course['coreqs'],
                    note=course['note'])
    for location in locations:
        try:
            Locations.objects.create(id=location['id'],
                                    campus=location['campus'],
                                    building=location['building'],
                                    room=location['room'])
        except:
            pass
    for section in sections:
        if section['crn'] not in [v['crn'] for v in o_sections]:
            Sections.objects.create(crn=section['crn'],
                        instructor=Instructors.objects.get(id=section['instructor']),
                        name=section['name'],
                        course=Courses.objects.get(id=section['course']),
                        term=Terms.objects.get(id=section['term']),
                        medium=InstructionMediums.objects.get(id=section['medium']),
                        is_lab=section['is_lab'],
                        enrolled=section['enrolled'],
                        capacity=section['capacity'],
                        note=section['note'])
    for schedule in schedules:
        Schedules.objects.create(id=schedule['id'],
                                location=Locations.objects.get(id=schedule['location']),
                                crn=Sections.objects.get(crn=schedule['crn']),
                                weekday=schedule['weekday'],
                                time_start=schedule['time_start'],
                                time_end=schedule['time_end'],
                                date_start=schedule['date_start'],
                                date_end=schedule['date_end'],
                                is_weekly=schedule['is_weekly'])

    return dict(message="All data was imported." if len(failed) < 1 else "Some data could not be imported.",
                           failed=failed)