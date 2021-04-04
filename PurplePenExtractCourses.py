import sys
import copy
import xml.etree.ElementTree as ET

# ======================================================
# JM    2021-02-26 Initial release
# fbd38 2021-03-03 Improved with removing unecessary beacon
# ======================================================

# ======================================================
# Create xml files from courses of the original Purple Pen xml file
# Each file contains only one course and is named from the course's name
# All unused beacons are removed and the Start and Stop
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
    print('   Number of events: ' + str(nbcourses));

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
        validcontrol=[]
        newesttree = newtree
        newestroot = newesttree.getroot()
        bodyrace = newestroot.find('n:RaceCourseData',ns)
        newcoursedata = bodyrace.find('n:Course',ns)
        for valposte in newcoursedata.findall('n:CourseControl',ns):
            validcontrol.append(((valposte.find('n:Control',ns)).text));
        newestroot = newesttree.getroot()
        posterace = newestroot.find('n:RaceCourseData',ns)
        for poste in posterace.findall('n:Control',ns):
            if poste.find('n:Id', ns).text not in validcontrol:
                bodyrace.remove(poste);
        # Change Start and Stop Beacon Names
        newestroot = newesttree.getroot()
        posterace = newestroot.find('n:RaceCourseData',ns)
        for poste in posterace.findall('n:Control',ns):
            if poste.get('type') == 'Start':
                poste.find('n:Id',ns).text = 'DEPART';
            if poste.get('type') == 'Finish':
                poste.find('n:Id',ns).text = 'ARRIVEE';
        newestroot = newesttree.getroot()
        fool = newestroot.find('n:RaceCourseData',ns)
        posterace = fool.find('n:Course', ns)
        for poste in posterace.findall('n:CourseControl',ns):
            if poste.get('type') == 'Start':
                poste.find('n:Control',ns).text = 'DEPART';
            if poste.get('type') == 'Finish':
                poste.find('n:Control',ns).text = 'ARRIVEE';
        # Create each XML file
        newfilename = filename + '_' + coursesname[crs] + '.xml'
        print('Exporting : '+newfilename)
        newesttree.write(newfilename,
                      xml_declaration = True,
                      encoding = 'utf-8',
                      method = 'xml')
print('Completed.')

