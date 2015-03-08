from xml.etree.ElementTree import parse
from ConfigParser import SafeConfigParser
import csv

#first lets store the data
#TODO - parametrize the source file
#doc = parse('test_data/StructuralvsALL3.xml')
#doc = parse('test_data/StructuralvsALL.xml')
#doc = parse('test_data/StructuralvsALL.xml')
#doc = parse('test_data/Clash_Test_All_System_Clash.xml')
#doc = parse('test_data/Structural_vs_ALL_Grid_Update.xml')
doc = parse('test_data/Structural_vs_All_MEP_(Grids_Working).xml')
clash_output_filename = 'clash_group.csv'
#TODO parmeterize box_size
box_size = 3.0
#TODO parameterize the config file
config_file="clash_util.ini"
#TODO output help information

parser = SafeConfigParser()
parser.read(config_file)

CSV_HEADER = "CLASH_GROUP_NAME, ORIGIN_CLASH, CLASH_GROUP_COUNT, TOTAL_CLASHES, PATH_COMBO, PATH_BLAME, CLASH_DETAIL\n"

# create a list with path priority order
path_order = []
for path_order_num, path_file_name in parser.items("path"):
    path_order.append(path_file_name)

parsed_data = {}
clash_count = 0

# parse the XML data we care about
# first some summary information
for item in doc.iterfind('batchtest/clashtests/clashtest/summary'):
    clash_count = item.attrib['total']

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
    group_path_blame = ""
    # based on the precedence in the configuration file we need to attribute
    # this clash to one of the sub systems
    # first separate into two paths
    path1, path2 = clash1_file_key.split('-')
    # loop through path order.  We could use index, but we want to sub search
    # so doing this the hard way
    found = 0
    for p in path_order:
        # see if that path_order text is in either paths
        if p in path1:
            found = 1
            group_path_blame = path1
        elif p in path2:
            found = 1
            group_path_blame = path2

        if found:
            break

    # if we get here an haven't found anything our config is messed up, warn the user
    if not found:
        print "Could not find path order for %s.  Please check your config file." % clash1_file_key

    z1 = x[2]
    y1 = x[1]
    x1 = x[0]
    finds_key = [clash1_name]
    finds_source = clash1_name
    finds_data = [group_size, group_file_key, clash1_name, group_path_blame, (clash1_name, clash1_image, clash1_grid_line)]

    for y in parsed_data:
        clash2_image = parsed_data[y][0]
        clash2_name = parsed_data[y][1]
        clash2_file_key = parsed_data[y][2]
        clash2_grid_line = parsed_data[y][3]
        # skip if we are comparing a clash to itself
        if clash1_name == clash2_name:
            continue
        # skip if we are not comparing two clashes from the same sub system combination
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
                    # found a clash  we care about
                    finds_key.append((clash2_name))
                    finds_data.append((clash2_name, clash2_image, clash2_grid_line))
                    finds_data[0] += 1

    s_finds_key = sorted(finds_key)
    s_finds_key_t = tuple(s_finds_key)
    if s_finds_key_t not in results.keys():
        results[s_finds_key_t] = finds_data

print "Found %s clash groups in %s total clashes" % (len(results), clash_count)

output_file = open(clash_output_filename, 'wb')
# add a header row
output_file.write(CSV_HEADER)
writer = csv.writer(output_file)
for clash_group, clash_data in results.items():
    print clash_group
    group_count = clash_data.pop(0)
    group_file_key = clash_data.pop(0)
    group_origin_clash = clash_data.pop(0)
    group_path_blame = clash_data.pop(0)
    writer.writerow([clash_group, group_origin_clash, group_count, clash_count, group_file_key, group_path_blame, clash_data])

output_file.close()

