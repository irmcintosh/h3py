import h3

h3_obj = h3.h3(40.689167, -74.044444, 10)
h3_address = h3_obj.geo_to_h3
print (h3_address)
hex_center_coordinates = h3_obj.geo_to_h3
#print ()
print (h3_obj.h3_to_geo(hex_center_coordinates))
#print ()
print(h3_obj.h3_to_geoboundary((h3_address)))