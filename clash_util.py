from xml.etree.ElementTree import parse
import csv

#first lets store the data
doc = parse('test_data/StructuralvsMEP.xml')
parsed_data = {}

for item in doc.iterfind('batchtest/clashtests/clashtest/clashresults/clashresult'):
    imagefile = item.attrib['href']
    name = item.attrib['name']
    for classp in item.findall('clashpoint/pos3f'):
        x = classp.attrib['x']
        y = classp.attrib['y']
        z = classp.attrib['z']
        coord = (x,y,z)
        parsed_data[coord] = (imagefile,name)

#now let's iterate and find the ones within a certain distance
#TODO - make this a command line parameter
box_size = 10.0
results = {}
for x in parsed_data:
    group_size = 1
    clash1_name = parsed_data[x][1]
    clash1_image = parsed_data[x][0]
    z1 = x[2]
    y1 = x[1]
    x1 = x[0]
    finds_key = [clash1_name]
    finds_data = [group_size, (clash1_name, clash1_image)]
    for y in parsed_data:
        clash2_name = parsed_data[y][1]
        clash2_image = parsed_data[y][0]
        if clash1_name == clash2_name:
            continue
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
writer = csv.writer(open('clash_group.csv', 'wb'))
for clash_group, clash_data in results.items():
    print clash_group
    group_count = clash_data.pop(0)
    writer.writerow([clash_group, group_count, clash_data])

