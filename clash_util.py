from xml.etree.ElementTree import parse
from ConfigParser import SafeConfigParser
import csv

#first lets store the data
#TODO - parametrize the source file
#doc = parse('test_data/StructuralvsALL3.xml')
#doc = parse('test_data/StructuralvsALL.xml')
#doc = parse('test_data/StructuralvsALL.xml')
#doc = parse('test_data/Clash_Test_All_System_Clash.xml')
doc = parse('test_data/Structural_vs_ALL_Grid_Update.xml')
clash_output_filename = 'clash_group.csv'
#TODO parmeterize box_size
box_size = 3.0
#TODO parameterize the config file
config_file="clash_util.ini"
#TODO output help information

#TODO - need to pull data from configuration file
parser = SafeConfigParser()
parser.read(config_file)
#print parser.get('path', 'path_file1')

# create a list with path priority order
path_order = []
for path_order_num, path_file_name in parser.items("path"):
    path_order.append(path_file_name)
    #print ' %s = %s' % (path_order_num, path_file_name)
#print path_order

parsed_data = {}
clash_count = 0

# parse the XML data we care about
# first some summary information
for item in doc.iterfind('batchtest/clashtests/clashtest/summary'):
    clash_count = item.attrib['total']
    print clash_count

# now some detail information about the clashes
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

    grid_location = ""
    for grid_line in item.findall('gridlocation'):
        if grid_line.text is not None:
            grid_location = grid_line.text.split(':')[0]

    for classp in item.findall('clashpoint/pos3f'):
        x = classp.attrib['x']
        y = classp.attrib['y']
        z = classp.attrib['z']
        coord = (x,y,z)
        parsed_data[coord] = (imagefile,name,file_keys, grid_location)

# now let's iterate and find the ones within a certain distance
results = {}
for x in parsed_data:
    group_size = 1
    group_file_key = ""
    clash1_image = parsed_data[x][0]
    clash1_name = parsed_data[x][1]
    clash1_file_key = parsed_data[x][2]
    clash1_grid_line = parsed_data[x][3]
    z1 = x[2]
    y1 = x[1]
    x1 = x[0]
    finds_key = [clash1_name]
    finds_source = clash1_name
    finds_data = [group_size, group_file_key, clash1_name, (clash1_name, clash1_image, clash1_grid_line)]
    for y in parsed_data:
        clash2_image = parsed_data[y][0]
        clash2_name = parsed_data[y][1]
        clash2_file_key = parsed_data[y][2]
        clash2_grid_line = parsed_data[y][3]
        # skip if we are comparing a clash to iteself
        if clash1_name == clash2_name:
            continue
        # skip if we are not comparing two clashes from the same sub system combination
        if clash1_file_key != clash2_file_key:
            continue
        # TODO - based on the precedence in the configuration we also need to attribute
        # this clash to one of the sub systems
        # first separate into two paths
        path1, path2 = clash1_file_key.split('-')
        print '1: %s   2: %s' % (path1,path2)
        # loop through path order.  We could use index, but we want to sub search
        # so doing this the hard way
        found = 0
        for p in path_order:
            # see if that path_order text is in either paths
            if path1.find(p):
                found = 1
                print 'found path1'
                print path1
            elif path2.find(p):
                found = 1
                print 'found path2'
                print path2

            if found:
                break


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
                    finds_data.append((clash2_name, clash2_image, clash2_grid_line))
                    finds_data[0] += 1
    if len(finds_key) > 1:
        s_finds_key = sorted(finds_key)
        s_finds_key_t = tuple(s_finds_key)
        if s_finds_key_t not in results.keys():
            results[s_finds_key_t] = finds_data

print len(results)
writer = csv.writer(open(clash_output_filename, 'wb'))
#TODO - add a header row
for clash_group, clash_data in results.items():
    print clash_group
    group_count = clash_data.pop(0)
    group_file_key = clash_data.pop(0)
    group_origin_clash = clash_data.pop(0)
    writer.writerow([clash_group, group_origin_clash, group_count, clash_count, group_file_key, clash_data])

