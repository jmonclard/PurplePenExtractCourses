import sys
import copy
import xml.etree.ElementTree as ET

# ======================================================
# JM    2021-02-26 Initial release
# fbd38 2021-03-03 Improved with removing unecessary controls
# JM    2021-04-05 Removing useless code
# ======================================================

# ======================================================
# Create xml files from courses of the original Purple Pen xml file
# Each file contains only one course and is named from the course's name
# All unused controls are removed and the Start and Stop controls
# are a renamed DEPART / ARRIVEE
# ======================================================

if len(sys.argv)>1:
    ns = {'n':'http://www.orienteering.org/datastandard/3.0'}
    ET.register_namespace('','http://www.orienteering.org/datastandard/3.0')
    filename=sys.argv[1]
    tree = ET.parse(filename + '.xml')
    root = tree.getroot()
    # Get event name
    print('Event name : ' + ((root.find('n:Event', ns)).find('n:Name', ns)).text)
    # Get course list
    racecoursedata = root.find('n:RaceCourseData',ns)
    coursesname=[]
    for child in racecoursedata.findall('n:Course',ns):
        name = child.find('n:Name',ns)
        coursesname.append(name.text);
    nbcourses = len(coursesname)
    print('   Number of courses : ' + str(nbcourses));

    # Cleck all courses
    for crs in range(nbcourses):
        newtree = copy.deepcopy(tree)
        newroot = newtree.getroot()
        newracecoursedata = newroot.find('n:RaceCourseData',ns)
        newcourses = newracecoursedata.findall('n:Course',ns)
        # Remove unwanted courses
        for i in range(nbcourses):
            if i != crs:
                newracecoursedata.remove(newcourses[i])
        # Remove unwanted controls in RaceCourseData
        usedcontrols=[]
        remainingcourse = newracecoursedata.find('n:Course',ns)
        for control in remainingcourse.findall('n:CourseControl',ns):
            usedcontrols.append(((control.find('n:Control',ns)).text));
            
        for control in newracecoursedata.findall('n:Control',ns):
            if control.find('n:Id', ns).text not in usedcontrols:
                newracecoursedata.remove(control);
        # Change Start and Stop controls Names
        for control in newracecoursedata.findall('n:Control',ns):
            if control.get('type') == 'Start':
                control.find('n:Id',ns).text = 'DEPART';
            if control.get('type') == 'Finish':
                control.find('n:Id',ns).text = 'ARRIVEE';
        for control in remainingcourse.findall('n:CourseControl',ns):
            if control.get('type') == 'Start':
                control.find('n:Control',ns).text = 'DEPART';
            if control.get('type') == 'Finish':
                control.find('n:Control',ns).text = 'ARRIVEE';
        # Create XML file
        newfilename = filename + '_' + coursesname[crs] + '.xml'
        print('Extracting : '+newfilename)
        newtree.write(newfilename,
                      xml_declaration = True,
                      encoding = 'utf-8',
                      method = 'xml')
print('Completed.')

