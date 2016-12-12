import sys
import os
import re
import xlrd
import csv

PACKAGE_TYPES = (
    'CB132',
    'CM225',
    'CT256',
    'TQ144',
    'VQ100',
    'CM81',
    'CB81',
    'CM121',
    'CB121',
    'CM225',
    'SWG25',
    'CM36A',
    'CM36',
    'CM49',
    'SWG16',
    'QN84',
    'SG32',
    'WLCP16',
    'WLCS36',
    'SG48',
    )
    
def find_package_name(name):
    for nm in PACKAGE_TYPES:
        if re.search(nm, name):
            return nm
    return None
    

def set_pin_type(name, type):
    name = name.upper()
    type = type.upper()
    if type in ['LED', 'IRLED']:
        return 'IO'
    if name[0:2] == 'IO' and type in ['DPIO','PIO','FIO','GBIN','SPI','CONFIG']:
        return 'IO'
    if name[0:2] == 'IO' and (type[0:3] == 'PIO' or type[0:4] == 'DPIO'):
        return 'IO'
    if name[0:3] == 'PIO' and type in ['DPIO','PIO','FIO','GBIN','SPI','CONFIG']:
        return 'IO'
    if name[0:4] == 'HCIO' and type in ['HCPIO']:
        return 'IO'
    if name[0:2] == 'NC' and type == 'NC':
        return 'NC'
    if name[0:3] == 'VCC' and type == 'VCC':
        return 'POWER'
    if name[0:3] == 'GND' and type == 'GND':
        return 'POWER'
    if name == 'GND_LED' and type == 'GND_LED':
        return 'POWER'
    if name[:5] == 'CDONE' and type == 'CONFIG':
        return 'OUTPUT'
    if name == 'CRESET_B' and type == 'CONFIG':
        return 'INPUT'
    if name == 'CDONE' and type == 'CDONE':
        return 'OUTPUT'
    if name == 'CRESETB' and type == 'CRESETB':
        return 'INPUT'
    if name[0:3] == 'VCC' and type == 'SPI':
        return 'POWER'
    if name == 'VCCSPI' and type == 'VCCSPI':
        return 'POWER'
    if name[0:5] == 'VCCIO' and type[0:5] == 'VCCIO':
        return 'POWER'
    if name[0:9] == 'SPI_VCCIO' and type[0:5] == 'VCCIO':
        return 'POWER'
    if name[0:3] == 'VPP' and type == 'VPP':
        return 'POWER'
    if name == 'VPP_2V5_VCCIO0' and type == 'VPP_2V5':
        return 'POWER'
    if name[:6] == 'GNDPLL' and type == 'GNDPLL':
        return 'POWER'
    if name[:6] == 'VCCPLL' and type == 'VCCPLL':
        return 'POWER'
    
    print 'ERROR: unknown type for {}, {}'.format(name, type)
    return None
    
def set_pin_bank(name, bank):
    try:
        bank = int(bank)
        return bank
    except ValueError:
        pass
    name = name.upper()
    bank = str(bank).upper()
    if bank in ['NC','VPP','GNDPLL','VCCPLL','GND','VCC', 'GND_LED']:
        return ''
    m = re.match('(SPI_)?VCCIO_?(?P<bank>.+)', name)
    if m is not None and bank == 'VCCIO':
        try:
            return int(m.group('bank'))
        except ValueError:
            return ''
    if name == 'SPI_VCCIO1' and bank == 'VCCIO':
        return 1
    if name == 'SPI_VCCIO1_VCCIO2' and bank == 'VCCIO':
        return 2
    if name == 'VPP_2V5_VCCIO0' and bank == 'VPP_2V5':
        return 0
    return bank

def create_lattice_csv(xlsx_filename, csv_filename):
    with xlrd.open_workbook(xlsx_filename, ragged_rows=True) as xlsx_wb:
        sh1 = xlsx_wb.sheet_by_index(0)
        with open(csv_filename, 'wb') as csv_file:
            for rownum in xrange(sh1.nrows):
                if sh1.row_len(rownum) == 1:
                    chip_name = sh1.cell_value(rownum,0)
                    labels = sh1.row_values(rownum+1)
                    pin_start_row = rownum + 2
                    break
                if sh1.row_len(rownum) > 1:
                    chip_name = os.path.splitext(os.path.basename(xlsx_filename))[0]
                    labels = sh1.row_values(rownum)
                    pin_start_row = rownum + 1
                    break
            chip_name = re.sub('\s+',' ',chip_name)
            chip_name = re.sub(' Pinout ','-',chip_name, flags=re.IGNORECASE)
            chip_name = re.sub('_pinlist','',chip_name, flags=re.IGNORECASE)
            sh2 = csv.writer(csv_file)
            for pckg_col, pckg_header in enumerate(labels):
                pckg_name = find_package_name(pckg_header)
                if pckg_name == None:
                    continue
                chip_and_pckg = chip_name + '-' + pckg_name
                chip_and_pckg = chip_and_pckg.upper()
                chip_and_pckg = re.sub('ICE40','iCE40',chip_and_pckg)
                chip_and_pckg = re.sub('LM-','-LM',chip_and_pckg)
                sh2.writerow([chip_and_pckg])
                sh2.writerow(['pin','bank','type','name'])
                for rownum in xrange(pin_start_row,sh1.nrows):
                    def to_upper(s):
                        if type(s) in [str, unicode]:
                            return s.upper()
                        return s
                    pname, ptype, pbank = map(to_upper, sh1.row_values(rownum)[0:3])
                    pnum = to_upper(sh1.row_values(rownum)[pckg_col])
                    if type(pbank) == float:
                        pbank = int(pbank)
                    if type(pnum) == float:
                        pnum = int(pnum)
                    if pnum == '-':
                        continue
                    ptype = set_pin_type(pname,ptype)
                    pbank = set_pin_bank(pname,pbank)
                    sh2.writerow([pnum, pbank, ptype, pname])
                sh2.writerow(['','','',''])

if __name__ == '__main__':
    output_filename = os.path.splitext(sys.argv[1])[0] + '.csv'
    create_lattice_csv(sys.argv[1], output_filename)
