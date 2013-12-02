import glob
import itertools
from numerics import db
from numerics.models import Numeric, Vendor, VendorNumeric

files = glob.glob('textfiles/*.txt')

numerics = {}

def create_it(numeric, extra, vendor, name):
    numeric = Numeric(numeric, extra)
    db.session.commit()
    vn = VendorNumeric(numeric, vendor, name)

db.create_all()

files.sort()  # my OCD is annoyed otherwise

for f in files:
    with open(f, 'r') as text:
        vendor = Vendor(f[10:-4])
        for line in text:
            line = line[:-1]  # strip off \n
            (numeric, _, name) = line.partition(" ")
            (name, _, extra) = name.partition(" ")
            numerics = Numeric.query.filter_by(numeric=numeric).all()
            if len(numerics) != 0:
                names = []
                for num in numerics:
                    n = num.pretty_vendor_numerics()
                    names.append(n.keys())
                if name not in list(itertools.chain.from_iterable(names)):
                    print('\nCONFLICT!  Numeric {} is already defined as {}, but {} is defining it as {}.'.format(numeric, repr(names), vendor.vendor, name))
                    choice = input('Shall I (C)reate a conflicting numeric, (A)lias it - meaning it is just another name for the same thing, or (S)kip it? [c/a/s] ').lower()[0]
                    if choice == 'c':
                        create_it(numeric, extra, vendor, name)
                    elif choice == 'a':
                        choice = input('Which? {} '.format(repr(names)))
                        vn = VendorNumeric(numerics[int(choice)], vendor, name)
                    else:
                        continue
                else:
                    hax = [name in l for l in names]
                    pos = hax.index(True)
                    vn = VendorNumeric(numerics[pos], vendor, name)
            else:
                create_it(numeric, extra, vendor, name)
            print('.', end='', flush=True)

print('\nSyncing...')
db.session.commit()
print('Finished')
