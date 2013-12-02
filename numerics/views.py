from flask import render_template, redirect, url_for, request, json
from numerics import app, db
from numerics.models import Numeric, Vendor, VendorNumeric
from itertools import chain

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vendors')
def vendors():
    return render_template('vendors.html', vendors=Vendor.query.all())

@app.route('/vendors/<int:vendor_id>')
def show_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    return render_template('vendor.html', vendor=vendor)

@app.route('/vendors/<vendor_name>')
def show_vendor_name(vendor_name):
    vendor = Vendor.query.filter_by(vendor=vendor_name).first_or_404()
    return render_template('vendor.html', vendor=vendor)

@app.route('/vendors', methods=['POST'])
def add_vendor():
    v = Vendor(request.form['name'])
    return redirect(url_for('show_vendor', vendor_id=v.vendor_id))

@app.route('/numerics')
def numerics():
    return render_template('numerics.html', numerics=Numeric.query.order_by(Numeric.numeric), vendors=Vendor.query.all())

@app.route('/numerics/id<int:numeric_id>')
def show_numeric(numeric_id):
    numeric = Numeric.query.get_or_404(numeric_id)
    return render_template('numeric.html', numeric=numeric)

@app.route('/numerics/<numeric>')
def show_friendly_numeric(numeric):
    model = Numeric.query.filter_by(numeric=numeric).all()
    if len(model) > 1:
        return render_template('conflict.html', model=model, n=numeric)
    elif len(model) == 0:
        return redirect(url_for('numerics'))
    else:
        return render_template('numeric.html', numeric=model[0])

@app.route('/numerics', methods=['POST'])
def add_numeric():
    n = Numeric(request.form['numeric'], request.form['purpose'])
    vendors = request.form.getlist('vendors')
    names = request.form.getlist('names')
    assert len(vendors) == len(names)
    for vendor, name in zip(vendors, names):
        v = Vendor.query.get(vendor)
        relation = VendorNumeric(n, v, name)
    return redirect(url_for('show_numeric', numeric_id=n.numeric_id))

@app.route('/numerics.json')
def json_numeric():
    pass

@app.route('/conflicts')
def conflicts():
    ids = list(chain.from_iterable(db.session.query(Numeric.numeric).group_by(Numeric.numeric).having(db.func.count(Numeric.numeric) > 1).all()))
    numerics = [Numeric.query.filter_by(numeric=n).all() for n in ids]
    return render_template('conflicts.html', numerics=numerics)

@app.route('/map')
def map():
    return render_template('map.html')

