import sys
import copy
import xml.etree.ElementTree as ET

# ======================================================
# JM  2021-02-26 In,itial release
# ======================================================

# ======================================================
# Create xml files from courses of the original Purple Pen xml file
# Each file contains only one course and is named from the course's name
# ======================================================

if len(sys.argv)>1:
    ns = {'n':'http://www.orienteering.org/datastandard/3.0'}
    ET.register_namespace('','http://www.orienteering.org/datastandard/3.0')
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    racecoursedata = root.find('n:RaceCourseData',ns)
    coursesname=[]
    for child in racecoursedata.findall('n:Course',ns):
        name = child.find('n:Name',ns)
        coursesname.append(name.text);
    nbcourses = len(coursesname)

    for crs in range(nbcourses):
        newtree = copy.deepcopy(tree)
        newroot = newtree.getroot()
        newracecoursedata = newroot.find('n:RaceCourseData',ns)
        newcourses = newracecoursedata.findall('n:Course',ns)
        for i in range(nbcourses):
            if i != crs:
                newracecoursedata.remove(newcourses[i])
        newfilename = coursesname[crs]+'.xml'
        print('Exporting : '+newfilename)
        newtree.write(newfilename,
                      xml_declaration = True,
                      encoding = 'utf-8',
                      method = 'xml')

print('Done.')

