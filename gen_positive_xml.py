import os
import numpy as np
import xml
import xml.etree.ElementTree as ET
from xml.dom import minidom
import gen_name as gname

WIDTH =256

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")



def insert_patch(idx, Element, point):
    group="Patches"
    anno=ET.SubElement(Element, "Annotation",Name="Patch_%d"%idx, Type="Polygon", PartOfGroup=group, Color="#0000FF")
    coords=ET.SubElement(anno, "Coordinates")
    ET.SubElement(coords, "Coordinate",Order="0", X=str(point[0]+2), Y=str(point[1]+2))
    ET.SubElement(coords, "Coordinate",Order="1", X=str(point[0]+WIDTH-2), Y=str(point[1]+2))
    ET.SubElement(coords, "Coordinate",Order="2", X=str(point[0]+WIDTH-2), Y=str(point[1]+WIDTH-2))
    ET.SubElement(coords, "Coordinate",Order="3", X=str(point[0]+2), Y=str(point[1]+WIDTH-2))
    return True
def insert_group(Element):
    coords=ET.SubElement(Element, "AnnotationGroups")
    ET.SubElement(coords, "Group",Color="#FF0000",Name ="Patches",PartOfGroup="None")
    return True
def insert_annotation_group(Element):
    annotation = ET.SubElement(Element,"Annotations")
    return annotation

def gen_xml(score,patient_id=0,node_id=0,threshold=0.5):
    xml_name = gname.gen_positive_xml_file_name(patient_id,node_id,threshold)
    top = ET.Element("ASAP_Annotations")
    patch_id = 0
    arr_score = np.array(score)
    patch_top =insert_annotation_group(top)
    for x_cnt in range(arr_score.shape[1]):
        for y_cnt in range(arr_score.shape[0]):
            if  arr_score[y_cnt][x_cnt] > 0.0:
                patch = np.array([x_cnt*256, y_cnt*256])
                insert_patch(patch_id,patch_top,patch)
                patch_id += 1
    insert_group(top)
    f = open(xml_name, "w")
    f.write(prettify(top))
    f.close()
    print "generate the file %s " %(xml_name)
