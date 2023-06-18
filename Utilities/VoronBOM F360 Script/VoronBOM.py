#Author-Autodesk Inc.
#Description-Etract BOM information from active design.

import adsk.core, adsk.fusion, traceback, re

def spacePadRight(value, length):
    pad = ''
    if type(value) is str:
        paddingLength = length - len(value) + 1
    else:
        paddingLength = length - value + 1
    while paddingLength > 0:
        pad += ' '
        paddingLength -= 1

    return str(value) + pad

def walkThrough(bom):
    mStr = ''
    bom = sorted(bom, key=lambda x: x['name'])
    for item in bom:
        mStr += str(item['name']) + '\t' + str(item['instances']) + '\n'
    return mStr

def main():
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        design = app.activeProduct
        title = 'Extract BOM'
        if not design:
            ui.messageBox('No active design', title)
            return

        # Get all occurrences in the root component of the active design
        root = design.rootComponent
        occs = root.allOccurrences
        
        # Gather information about each unique component
        bom = []
        logs = ""
        for occ in occs:
            comp = occ.component
            comp_name = re.sub('v[0-9]+','',comp.name)
            comp_name = re.sub('\([0-9]\)*','',comp_name)
            comp_name = comp_name.replace("(Mirror)","").strip()
            jj = 0
            for bomI in bom:
                if bomI['name'] == comp_name:
                    # Increment the instance count of the existing row.
                    bomI['instances'] += 1
                    break
                jj += 1

            if jj == len(bom):
                # Gather any BOM worthy values from the component                
                # Add this component to the BOM
                bom.append({
                    'name': comp_name,
                    'instances': 1
                })

        # Display the BOM
        title = 'Name\tInstances'
        msg = title + '\n' + walkThrough(bom)
        
        ui.messageBox(msg, 'Bill Of Materials')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

main()
