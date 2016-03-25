import pdftab as pdf
import re
import random
import json

def add_coords(systems):
    for system in systems:
        if 'coordinates' in system:
            if system['coordinates'][0] != '?' and system['coordinates'][1] != '/':
                system['x'] = ord(system['coordinates'][:1].lower())-95.5 + (random.random() -0.5)
                system_y = [int(s) for s in re.findall(r'\d+', system['coordinates'])]
                system['y'] = sum(system_y)/len(system_y) - 0.5 + (random.random() -0.5)

    return systems
    
systems = pdf.convert_pdf_table('galaxy.pdf')

add_coords(systems)

json_file = open('systems.json', 'w')

json_file.write(json.dumps(systems))


