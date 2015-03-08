from xml.etree.ElementTree import parse
import csv

#first lets store the data
#TODO - parametrize the source file
doc = parse('test_data/StructuralvsALL3.xml')
#doc = parse('test_data/StructuralvsALL.xml')
#doc = parse('test_data/StructuralvsMEP.xml')
clash_output_filename = 'clash_group.csv'

parsed_data = {}
clash_count = 0

#TODO - pull out the total number
for item in doc.iterfind('batchtest/clashtests/clashtest/summary'):
    clash_count = item.attrib['total']
    print clash_count

for item in doc.iterfind('batchtest/clashtests/clashtest/clashresults/clashresult'):
    imagefile = item.attrib['href']
    name = item.attrib['name']
    file_keys = ""
    for plink in item.findall('clashobjects/clashobject/pathlink'):
        sys_elem =  plink[2].text.split('.')
        if len(file_keys) == 0:
            file_keys += sys_elem[0]
        else:
            file_keys += "-" + sys_elem[0]

    for classp in item.findall('clashpoint/pos3f'):
        x = classp.attrib['x']
        y = classp.attrib['y']
        z = classp.attrib['z']
        coord = (x,y,z)
        parsed_data[coord] = (imagefile,name,file_keys)

#now let's iterate and find the ones within a certain distance
#TODO - make this a command line parameter
box_size = 10.0
results = {}
for x in parsed_data:
    group_size = 1
    group_file_key = ""
    clash1_image = parsed_data[x][0]
    clash1_name = parsed_data[x][1]
    clash1_file_key = parsed_data[x][2]
    z1 = x[2]
    y1 = x[1]
    x1 = x[0]
    finds_key = [clash1_name]
    finds_source = clash1_name
    finds_data = [group_size, group_file_key, clash1_name, (clash1_name, clash1_image)]
    for y in parsed_data:
        clash2_image = parsed_data[y][0]
        clash2_name = parsed_data[y][1]
        clash2_file_key = parsed_data[y][2]
        if clash1_name == clash2_name:
            continue
        if clash1_file_key != clash2_file_key:
            continue
        finds_data[1] = clash1_file_key
        z2 = y[2]
        y2 = y[1]
        x2 = y[0]
        zdelt = float(z1)-float(z2)
        if (zdelt >= -box_size) and (zdelt <=  box_size):
            ydelt = float(y1)-float(y2)
            if (ydelt >= -box_size) and (ydelt <= box_size):
                xdelt = float(x1)-float(x2)
                if (xdelt >= -box_size) and (xdelt <= box_size):
                    finds_key.append((clash2_name))
                    finds_data.append((clash2_name, clash2_image))
                    finds_data[0] += 1
    if len(finds_key) > 1:
        s_finds_key = sorted(finds_key)
        s_finds_key_t = tuple(s_finds_key)
        if s_finds_key_t not in results.keys():
            results[s_finds_key_t] = finds_data

print len(results)
writer = csv.writer(open(clash_output_filename, 'wb'))
for clash_group, clash_data in results.items():
    print clash_group
    group_count = clash_data.pop(0)
    group_file_key = clash_data.pop(0)
    group_origin_clash = clash_data.pop(0)
    writer.writerow([clash_group, group_origin_clash, group_count, clash_count, group_file_key, clash_data])

