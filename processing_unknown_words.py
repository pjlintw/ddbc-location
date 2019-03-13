from ddbcLOC.ddbc_location_api import DDBC_LOCATION 


### function set ###


### csv path ###
CSV_PATH = "C:/Users/IISR/Downloads/data_geo.txt"
f = [i.strip().split(',') for i in open(CSV_PATH, 'r', encoding='utf-8').readlines()]

# remove space character
for small_lst in f:
	for each_idx in range(len(small_lst)):
		current_char = small_lst[each_idx]
		if ' ' in current_char:
			small_lst[each_idx] = current_char.replace(' ', '')
	

### Get location name via DDBC_LOCATION class ###
c = DDBC_LOCATION()
for i in f:
	loc = i[0]
	loc_id = i[1]
	if '?' in loc:
  		#print(f'|{loc_id}|')
  		print(loc, loc_id)

  		name = c.parser_data(loc_id)['name'] 
  		i[0] = name


### write file ###
with open('new_output.csv', 'w', encoding='utf-8-sig') as output:
	for small_lst in f:
		output.write(','.join(small_lst)+'\n')

