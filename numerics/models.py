from numerics import db

class Numeric(db.Model):
    numeric_id = db.Column(db.Integer, primary_key=True)
    numeric = db.Column(db.String(3))
    purpose = db.Column(db.Text)

    def __init__(self, numeric, purpose):
        self.numeric = numeric
        self.purpose = purpose

        db.session.add(self)

    def pretty_vendor_numerics(self):
        vns = Numeric.vendor_numerics
        pretty = {}
        for vn in self.vendor_numerics:
            old = pretty.get(vn.name, None)
            if old:
                pretty[vn.name] = old + ', {}'.format(vn.vendor.vendor)
            else:
                pretty[vn.name] = vn.vendor.vendor
        return pretty

class Vendor(db.Model):
    vendor_id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String(255))

    def __init__(self, vendor):
        self.vendor = vendor

        db.session.add(self)
        db.session.commit()

class VendorNumeric(db.Model):
    relation_id = db.Column(db.Integer, primary_key=True)
    numeric_id = db.Column(db.Integer, db.ForeignKey('numeric.numeric_id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.vendor_id'))
    name = db.Column(db.String(255))

    numeric = db.relationship('Numeric', backref='vendor_numerics')
    vendor = db.relationship('Vendor', backref='vendor_numerics')

    def __init__(self, numeric, vendor, name):
       self.numeric_id = numeric.numeric_id
       self.vendor_id = vendor.vendor_id
       self.name = name

       db.session.add(self)

