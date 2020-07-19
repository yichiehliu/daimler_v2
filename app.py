import click
import time
import base64
import json

from flask import Flask, jsonify, abort, request  # render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from math import radians, sin, cos, acos
from sqlalchemy import and_, func
# from datetime import timedelta


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        content = json.dumps({"error_code": "500"})
        # resp = Response_headers(content)
        return content

    @app.errorhandler(404)
    def page_not_found(e):
        content = json.dumps({"error_code": "500"})
        # resp = Response_headers(content)
        return content

    @app.errorhandler(409)
    def bad_request(e):
        content = json.dumps({"error_code": "500"})
        # resp = Response_headers(content)
        return content

    @app.errorhandler(500)
    def internal_server_error(e):
        content = json.dumps({"error_code": "500"})
        # resp = Response_headers(content)
        return content


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                'This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

        db.session.commit()
        click.echo('Done.')

    @app.cli.command('forge')
    @click.option('--car', default=10, help='Quantity of cars, default is 10.')
    @click.option('--rentables', default=10, help='Quantity of rentalable cars, default is 10.')
    @click.option('--query', default=50, help='Quantity of queries, default is 10.')
    @click.option('--order', default=50, help='Quantity of orders, default is 10.')
    def forge(car, rentables, query, order):
        """Generate fake data."""
        from forges import fake_car, fake_car_status, fake_longnla, fake_scooter, fake_scooter_status

        db.drop_all()
        db.create_all()
        click.echo('Generating the scooters...')
        fake_scooter()
        click.echo('Generating the scooter_status...')
        fake_scooter_status()
        click.echo('Generating the cars...')
        fake_car()
        click.echo('Generating the car_status...')
        fake_car_status()
        click.echo('Generating the longtitude...')
        fake_longnla()

        # click.echo('Generating %d categories...' % category)
        # fake_categories(category)

        # click.echo('Generating %d posts...' % post)
        # fake_posts(post)

        # click.echo('Generating %d comments...' % comment)
        # fake_comments(comment)

        # click.echo('Generating links...')
        # fake_links()

        click.echo('Done.')


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
register_commands(app)
register_errors(app)


class ScooterAllinfo(db.Model):  # 8 columns
    __tablename__ = 'ScooterAllinfo'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bmid = db.Column(db.String, nullable=False)
    Scooter_type = db.Column(db.String, default="Scooter")
    sub_type = db.Column(db.String, nullable=False)
    brand_id = db.Column(db.String, nullable=False)
    model_id = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, db.ForeignKey(
        'FONLoc.loc'), nullable=False)
    UsedorNot = db.Column(db.Boolean, nullable=False)  # Used currently or not
    # cbm = db.relationship('ScooterStatus', backref='cbm', lazy=True)

    def __init__(self, bmid, sub_type, brand_id, location, model_id, price, UsedorNot):
        self.bmid = bmid
        # self.Scooter_type = Scooter_type
        self.sub_type = sub_type
        self.brand_id = brand_id
        self.model_id = model_id
        self.location = location
        self.price = price
        self.UsedorNot = UsedorNot

    def __repr__(self):
        return '<ScooterAllinfo %r>' % self.item_id


class FONLoc(db.Model):
    __tablename__ = 'FONLoc'
    loc = db.Column(db.String, primary_key=True)
    longnla = db.Column(db.String, nullable=False)

    def __init__(self, loc, longnla):
        self.loc = loc
        self.longnla = longnla

    def __repr__(self):
        return '<FONLoc %r>' % self.loc


class ReservedScooterStatus(db.Model):
    __tablename__ = 'ReservedScooterStatus'
    sid = db.Column(db.Integer, primary_key=True,
                    autoincrement=True)  # status id
    date = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    bmid = db.Column(db.String, db.ForeignKey(
        'ScooterAllinfo.bmid'), nullable=False)
    ScooterAmount = db.Column(db.Integer, nullable=False)

    def __init__(self, date, location, bmid, ScooterAmount):
        self.date = date
        self.bmid = bmid
        self.location = location
        self.ScooterAmount = ScooterAmount

    def __repr__(self):
        return '<ReservedScooterStatus %r>' % self.sid


class ScooterQueryRecord(db.Model):
    __tablename__ = 'ScooterQueryRecord'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qid = db.Column(db.String, nullable=False)
    did = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Integer, server_default=db.func.now())
    bmid = db.Column(db.String, db.ForeignKey(
        'ScooterAllinfo.bmid'), nullable=False)
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # cbm = db.relationship('ScooterStatus', backref='cbm', lazy=True)

    def __init__(self, qid, did, bmid, created_at, st, et, location, price):
        self.qid = qid
        self.did = did
        self.created_at = created_at
        self.bmid = bmid
        self.location = location
        self.st = st
        self.et = et
        self.price = price

    def __repr__(self):
        return '<ScooterQueryRecord %r>' % self.qdid


# class ScooterIDAssign(db.Model):
#     __tablename__ = 'IDAssign'
#     cbmid = db.Column(db.Integer, primary_key=True)
#     itemid = db.Column(db.String, nullable=False)

#     def __init__(self, cbmid, itemid):
#         self.cbmid = cbmid
#

# 真正有租賃紀錄的record
class ScooterOrderRecord(db.Model):  # After activate the reservation
    __tablename__ = 'ScooterOrderRecord'
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, nullable=False)
    # rid = db.Column(db.String, db.ForeignKey(
    #     'BookingRecord.rid'), nullable=False)
    # assign a item id
    qd_id = db.Column(db.String, db.ForeignKey(
        'ScooterQueryRecord.id'), nullable=True)
    item_id = db.Column(db.String, db.ForeignKey(
        'ScooterAllinfo.item_id'), nullable=True)
    bmid = db.Column(db.String, db.ForeignKey(
        'ScooterAllinfo.bmid'), nullable=False)
    created_at = db.Column(db.Integer, server_default=db.func.now())
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # Booked and Activate and Return Scooter using three url but same database
    # OrderConfirmed(Pending, item_id = 0)
    # -> Activated(Ready to drive(within 20 minutes), assign item_id)
    # -> Finished(Returned the Scooter)
    # Canceled
    status = db.Column(db.String, nullable=False)

    def __init__(self, oid, uid, qd_id, item_id, created_at, bmid, st, et, location, price, status):
        self.qd_id = qd_id
        self.uid = uid
        self.oid = oid
        self.item_id = item_id
        self.created_at = created_at
        # self.reserved_time = reserved_time # activation time ??
        self.st = st
        self.et = et
        self.bmid = bmid
        self.location = location
        self.status = status
        self.price = price

    def __repr__(self):
        return '<ScooterOrderRecord %r>' % self.oid


class CarAllinfo(db.Model):  # 8 columns
    __tablename__ = 'CarAllinfo'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bmid = db.Column(db.String, nullable=False)
    car_type = db.Column(db.String, default="car")
    sub_type = db.Column(db.String, nullable=False)
    brand_id = db.Column(db.String, nullable=False)
    model_id = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, db.ForeignKey(
        'FONLoc.loc'), nullable=False)
    UsedorNot = db.Column(db.Boolean, nullable=False)  # Used currently or not
    # cbm = db.relationship('CarStatus', backref='cbm', lazy=True)

    def __init__(self, bmid, sub_type, brand_id, location, model_id, price, UsedorNot):
        self.bmid = bmid
        # self.car_type = car_type
        self.sub_type = sub_type
        self.brand_id = brand_id
        self.model_id = model_id
        self.location = location
        self.price = price
        self.UsedorNot = UsedorNot

    def __repr__(self):
        return '<CarAllinfo %r>' % self.item_id


class ReservedCarStatus(db.Model):
    __tablename__ = 'ReservedCarStatus'
    sid = db.Column(db.Integer, primary_key=True,
                    autoincrement=True)  # status id
    date = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    bmid = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.bmid'), nullable=False)
    carAmount = db.Column(db.Integer, nullable=False)

    def __init__(self, date, location, bmid, carAmount):
        self.date = date
        self.bmid = bmid
        self.location = location
        self.carAmount = carAmount

    def __repr__(self):
        return '<ReservedCarStatus %r>' % self.sid


class CarQueryRecord(db.Model):
    __tablename__ = 'CarQueryRecord'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    qid = db.Column(db.String, nullable=False)
    did = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Integer, server_default=db.func.now())
    bmid = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.bmid'), nullable=False)
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # cbm = db.relationship('CarStatus', backref='cbm', lazy=True)

    def __init__(self, qid, did, bmid, created_at, st, et, location, price):
        self.qid = qid
        self.did = did
        self.created_at = created_at
        self.bmid = bmid
        self.location = location
        self.st = st
        self.et = et
        self.price = price

    def __repr__(self):
        return '<CarQueryRecord %r>' % self.qdid


# class CarIDAssign(db.Model):
#     __tablename__ = 'IDAssign'
#     cbmid = db.Column(db.Integer, primary_key=True)
#     itemid = db.Column(db.String, nullable=False)

#     def __init__(self, cbmid, itemid):
#         self.cbmid = cbmid
#

# 真正有租賃紀錄的record
class CarOrderRecord(db.Model):  # After activate the reservation
    __tablename__ = 'CarOrderRecord'
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String, nullable=False)
    # rid = db.Column(db.String, db.ForeignKey(
    #     'BookingRecord.rid'), nullable=False)
    # assign a item id
    qd_id = db.Column(db.String, db.ForeignKey(
        'CarQueryRecord.id'), nullable=True)
    item_id = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.item_id'), nullable=True)
    bmid = db.Column(db.String, db.ForeignKey(
        'CarAllinfo.bmid'), nullable=False)
    created_at = db.Column(db.Integer, server_default=db.func.now())
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # Booked and Activate and Return car using three url but same database
    # OrderConfirmed(Pending, item_id = 0)
    # -> Activated(Ready to drive(within 20 minutes), assign item_id)
    # -> Finished(Returned the car)
    # Canceled
    status = db.Column(db.String, nullable=False)

    def __init__(self, oid, uid, qd_id, item_id, created_at, bmid, st, et, location, price, status):
        self.qd_id = qd_id
        self.uid = uid
        self.oid = oid
        self.item_id = item_id
        self.created_at = created_at
        # self.reserved_time = reserved_time # activation time ??
        self.st = st
        self.et = et
        self.bmid = bmid
        self.location = location
        self.status = status
        self.price = price

    def __repr__(self):
        return '<CarOrderRecord %r>' % self.oid


# class OrderRecord(ActivatedReservation):
#     __tablename__ = 'OrderRecord'
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
class RealtimeCarDetails(db.Model):  # 8 columns
    __tablename__ = 'RealtimeCarDetails'
    item_id = db.Column(db.String, primary_key=True, unique=True)
    bmid = db.Column(db.String, nullable=False)
    car_type = db.Column(db.String, nullable=False)
    brand_id = db.Column(db.String, nullable=False)
    model_id = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    UsedorNot = db.Column(db.String, nullable=False)  # Used currently or not
    # cbm = db.relationship('CarStatus', backref='cbm', lazy=True)

    def __init__(self, item_id, bmid, car_type, brand_id, location, model_id, price, UsedorNot):
        self.bmid = bmid
        self.item_id = item_id
        self.car_type = car_type
        self.brand_id = brand_id
        self.model_id = model_id
        self.location = location
        self.price = price
        self.UsedorNot = UsedorNot

    def __repr__(self):
        return '<RealtimeCarDetails %r>' % self.item_id


class RealtimeCarOrderRecord(db.Model):  # 即時
    __tablename__ = 'RealtimeCarOrderRecord'
    item_id = db.Column(db.String, nullable=False)
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    st = db.Column(db.Integer, nullable=False)
    et = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)  # Abort/Finished/Ongoing

    def __init__(self, oid, item_id, st, et, price, location, status):
        self.item_id = item_id
        self.oid = oid
        self.location = location
        # self.reserved_time = reserved_time # activation time ??
        self.st = st
        self.et = et
        self.status = status
        self.price = price

    def __repr__(self):
        return '<RealtimeCarOrderRecord %r>' % self.oid


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))
    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    radius = 6371  # km
    dist = 6371.01 * acos(sin(lat1)*sin(lat2) + cos(lat1)
                          * cos(lat2)*cos(lon1 - lon2))
    d = dist

    return d  # km


# ========================================SCOOTER===================================
@app.route('/api/query/Scooter', methods=['GET', 'POST'])
def queryforScooter():
    params = request.args.get('params', type=str)
    decoded = base64.urlsafe_b64decode(
        params.encode('utf-8')).decode('utf-8')

    data = json.loads(decoded)

    st = data['start_time']
    et = data['end_time']
    user_longnla = data['location']
    sub_type = data['subtype']
    qid = data['query_id']
    query_time = data['query_time']

    # find the corresponding long&lat in FONLOC table
    loc_query = db.session.query(FONLoc).all()

    loc_fon = []
    for i in loc_query:
        if (distance(eval(i.longnla), eval(user_longnla)) <= 10):  # within 5km

            loc_fon.append(i.loc)
        print(i.longnla, user_longnla)
        print(distance(eval(i.longnla), eval(user_longnla)))

    print(loc_fon)
    rentalperiodcnt = 0
    for i in range(st, et, 3600):
        rentalperiodcnt += 1

    if (sub_type == 'unspecified'):
        for i in loc_fon:
            Scooterlist = db.session.query(ScooterAllinfo).join(ReservedScooterStatus, ReservedScooterStatus.bmid == ScooterAllinfo.bmid).\
                filter(and_(ScooterAllinfo.location == i, ReservedScooterStatus.location == i, ReservedScooterStatus.ScooterAmount >
                            0, ReservedScooterStatus.date >= st, ReservedScooterStatus.date < et)).\
                group_by(ReservedScooterStatus.bmid)
    else:
        Scooterlist = db.session.query(ScooterAllinfo).join(ReservedScooterStatus).\
            filter(and_(ScooterAllinfo.sub_type == sub_type,  ReservedScooterStatus.location.in_(loc_fon),
                        ReservedScooterStatus.ScooterAmount > 0, ReservedScooterStatus.date >= st, ReservedScooterStatus.date < et)).\
            group_by(ReservedScooterStatus.bmid).\
            having(func.count('*') == 2)
        # .\having(func.count('*') == rentalperiodcnt).all()

    output = []
    print(Scooterlist)
    cntd = 1
    for i in Scooterlist:
        locwlong = ''
        # try:
        print(i)
        did = str(int(time.time()) + int(qid) + cntd)
        locwlong = db.session.query(FONLoc.longnla).filter(
            FONLoc.loc == i.location).one()

        locwlong = "".join(locwlong)

        output.append({'query_id': qid, 'location': locwlong, 'deal_id': did,
                       'brand_id': i.brand_id, 'bmid': i.bmid, "vehicle_type": "Scooter",
                       'subtype': i.sub_type,
                       'model_id': i.model_id, 'price': str(i.price*rentalperiodcnt)})
        db.session.add(ScooterQueryRecord(created_at=query_time, qid=qid, did=did, bmid=i.bmid,
                                          st=st, et=et, location=i.location, price=i.price*rentalperiodcnt))

        cntd += 1
        print(output)
    db.session.commit()
    return jsonify(output)


# 1.Read parameters sended from Blockchain
# 2.Using Scooter Status Table to check the Scooter amount of the Scooter type that user selected,
# with the same logics of Step 5.3
# 3.Return the query result of Step 12.2

# 12.4 If the Scooter amount is enough
# 12.4.1 Update the Scooter Status Table, the Scooter amount of the choosen Scooter type should minus 1
# 12.4.2 Update the Order Record Table, kept the comfirmed order details
# 12.4.3 Return the order-succeeded messge
# 12.5 If the Scooter amount is not enough
# 12.5.1 The Order is failed, return the order-failed message


@app.route('/api/order/confirm/Scooter/', methods=['GET', 'POST'])
def scooterorderconfirmation():
    output = {}
    if request.is_json:
        data = request.get_json()

    rentalperiodcnt = 0
    rentalcnt = 0
    # API oid, uid, order_time, location, st, et, query_id, deal_id, bm_id
    # DB  uid, oid, created_at, st, et, location,  qd_id, item_id, price, status

    oid = data['order_id']
    uid = data['user_id']
    st = data['start_time']
    et = data['end_time']
    locwlong = data['location']
    loc = db.session.query(FONLoc).filter(
        FONLoc.longnla == locwlong).first().loc
    print(loc)
    did = data['deal_id']
    qid = data['query_id']
    bm_id = data['bmid']
    output = {
        "message": False,
        "order_id": oid,
        "user_id": uid,
        "bmid": bm_id
    }

    for i in range(st, et, 3600):  # 1hr = 3600 unix time
        rentalperiodcnt += 1

    alteramount = db.session.query(ReservedScooterStatus).\
        filter(and_(ReservedScooterStatus.bmid == bm_id, ReservedScooterStatus.location == loc,
                    ReservedScooterStatus.ScooterAmount > 0, ReservedScooterStatus.date >= st, ReservedScooterStatus.date < et))
    rentalcnt = db.session.query(ReservedScooterStatus).\
        filter(and_(ReservedScooterStatus.bmid == bm_id, ReservedScooterStatus.location == loc,
                    ReservedScooterStatus.ScooterAmount > 0, ReservedScooterStatus.date >= st, ReservedScooterStatus.date < et)).count()

    if (rentalcnt == rentalperiodcnt):
        for i in alteramount:
            i.ScooterAmount = i.ScooterAmount - 1
            print(i.ScooterAmount)
        output.update({
            "price": str(db.session.query(ScooterQueryRecord).filter(and_(ScooterQueryRecord.qid == qid, ScooterQueryRecord.did == did)).first().price),
            "message": True
        })
    else:
        output.update({
            "price": str(db.session.query(ScooterQueryRecord).filter(and_(ScooterQueryRecord.qid == qid, ScooterQueryRecord.did == did)).first().price),
            "message": [rentalcnt, rentalperiodcnt]
        })
        return jsonify(output)

    qdid = db.session.query(ScooterQueryRecord).filter(
        and_(ScooterQueryRecord.qid == qid, ScooterQueryRecord.did == did)).first().id

    order = ScooterScooterOrderRecord(
        oid=data['order_id'],
        uid=data['user_id'],
        created_at=data['order_time'],
        qd_id=qdid,
        st=data['start_time'],
        et=data['end_time'],
        location=loc,
        item_id=None,
        price=db.session.query(ScooterQueryRecord).filter(
            and_(ScooterQueryRecord.qid == qid, ScooterQueryRecord.did == did)).first().price,
        bmid=bm_id,
        status="Confirmed"
    )
    price = db.session.query(ScooterQueryRecord).filter(
        and_(ScooterQueryRecord.qid == qid, ScooterQueryRecord.did == did)).first().price
    # print(qdid, price)
    db.session.add(order)
    db.session.commit()
    return jsonify(output)


@app.route('/api/order/cancel/Scooter', methods=['GET', 'POST'])
def scooterordercancellation():
    output = {}
    if request.is_json:
        data = request.json

    # find rental st et,Scooter info
    oid = data['order_id']

    findorder = db.session.query(ScooterOrderRecord).\
        filter(ScooterOrderRecord.oid == oid)

    for i in findorder:
        st = i.st
        et = i.et
        loc = i.location
        bm_id = i.bmid
        i.status = 'Canceled'

    # alter Scooter status
    alteramount = db.session.query(ReservedScooterStatus).\
        filter(and_(ReservedScooterStatus.bmid == bm_id, ReservedScooterStatus.location == loc,
                    ReservedScooterStatus.ScooterAmount > 0, ReservedScooterStatus.date >= st, ReservedScooterStatus.date < et))

    for i in alteramount:
        i.ScooterAmount = i.ScooterAmount+1

    # alter resrv status to canceled

    output.update({'message': True, 'order_id': oid})

    db.session.commit()

    return jsonify(output)


# =======================================CAR========================================
# 1.Read parameters sended from Blockchain
# 2.Find rental spots within 10km, using Rental Spot & Geographic coordinates Conversion Table to calculate the distances
# 3.Using Car Status Table, which lists out the car amount of the time(one hour basis),
#  the location, and the car type
#  to check the available car type by given the 10-km-apart rental spots firstly,
# user's rental period secondly, and the specified car type thirdly.
# 4.Return the query result of Step 5.3
# 5. Update the the Query_Record Table, the query details
#  the available Car Type, the abailable rental Location, the available Rental time,
# and check if the car amount of those condition is enough

@app.route('/api/query/car', methods=['GET', 'POST'])
def queryforcar():
    params = request.args.get('params', type=str)
    decoded = base64.urlsafe_b64decode(
        params.encode('utf-8')).decode('utf-8')
    # params.decode('utf-8')
    # from queryform import FormSearchCars
    # data = request.get_json(force=True)
    # if request.is_json:
    #     data = request.get_json()
    # else:
    data = json.loads(decoded)
    # st = request.args.get('start_time', type=int)
    # et = request.args.get('end_time', type=int)
    # user_longnla = request.args.get(
    #     'location', default='*', type=str)  # long&lat user_location
    # sub_type = request.args.get('sub_type', default='*', type=str)
    # qid = request.args.get('query_id', type=str)
    # query_time = request.args.get('query_time', type=int)

    # content_dict = request.get_json()
    # form = FormSearchCars()
    st = data['start_time']
    et = data['end_time']
    user_longnla = data['location']
    sub_type = data['subtype']
    qid = data['query_id']
    query_time = data['query_time']

    # find the corresponding long&lat in FONLOC table
    loc_query = db.session.query(FONLoc).all()

    loc_fon = []
    for i in loc_query:
        if (distance(eval(i.longnla), eval(user_longnla)) <= 10):  # within 5km

            loc_fon.append(i.loc)
        print(i.longnla, user_longnla)
        print(distance(eval(i.longnla), eval(user_longnla)))

    print(loc_fon)
    rentalperiodcnt = 0
    for i in range(st, et, 3600):
        rentalperiodcnt += 1

    # print(rentalpreriodcnt)

    # if ReservedCarStatus
    # rentalperiod = dict()
    # for i in range(st, et + 1):
    #     rentalperiod.update(i: 0)
    # result = db.session.execute(
    #     'SELECT * FROM ReservedCarStatus WHERE location = :loc and carAmount > 0 and date >=:st and date <= :et').fetchall()
    # for loc in loc_fon:
    if (sub_type == 'unspecified'):
        for i in loc_fon:
            carlist = db.session.query(CarAllinfo).join(ReservedCarStatus, ReservedCarStatus.bmid == CarAllinfo.bmid).\
                filter(and_(CarAllinfo.location == i, ReservedCarStatus.location == i, ReservedCarStatus.carAmount >
                            0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et)).\
                group_by(ReservedCarStatus.bmid)
    else:
        carlist = db.session.query(CarAllinfo).join(ReservedCarStatus).\
            filter(and_(CarAllinfo.sub_type == sub_type,  ReservedCarStatus.location.in_(loc_fon),
                        ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et)).\
            group_by(ReservedCarStatus.bmid).\
            having(func.count('*') == 2)
        # .\having(func.count('*') == rentalperiodcnt).all()

    output = []
    print(carlist)
    cntd = 1
    for i in carlist:
        locwlong = ''
        # try:
        print(i)
        did = str(int(time.time()) + int(qid) + cntd)
        locwlong = db.session.query(FONLoc.longnla).filter(
            FONLoc.loc == i.location).one()

        locwlong = "".join(locwlong)

        output.append({'query_id': qid, 'location': locwlong, 'deal_id': did,
                       'brand_id': i.brand_id, 'bmid': i.bmid, "vehicle_type": "car",
                       'subtype': i.sub_type,
                       'model_id': i.model_id, 'price': str(i.price*rentalperiodcnt)})
        db.session.add(CarQueryRecord(created_at=query_time, qid=qid, did=did, bmid=i.bmid,
                                      st=st, et=et, location=i.location, price=i.price*rentalperiodcnt))

        cntd += 1
        print(output)
    db.session.commit()
    return jsonify(output)


# 1.Read parameters sended from Blockchain
# 2.Using Car Status Table to check the car amount of the car type that user selected,
# with the same logics of Step 5.3
# 3.Return the query result of Step 12.2

# 12.4 If the car amount is enough
# 12.4.1 Update the Car Status Table, the car amount of the choosen car type should minus 1
# 12.4.2 Update the Order Record Table, kept the comfirmed order details
# 12.4.3 Return the order-succeeded messge
# 12.5 If the car amount is not enough
# 12.5.1 The Order is failed, return the order-failed message


@app.route('/api/order/confirm/car/', methods=['GET', 'POST'])
def carorderconfirmation():
    output = {}
    if request.is_json:
        data = request.get_json()

    rentalperiodcnt = 0
    rentalcnt = 0
    # API oid, uid, order_time, location, st, et, query_id, deal_id, bm_id
    # DB  uid, oid, created_at, st, et, location,  qd_id, item_id, price, status
    # (不用bm_id price用qdid找) (新增 status, 派item_id)

    oid = data['order_id']
    uid = data['user_id']
    st = data['start_time']
    et = data['end_time']
    locwlong = data['location']
    loc = db.session.query(FONLoc).filter(
        FONLoc.longnla == locwlong).first().loc
    print(loc)
    did = data['deal_id']
    qid = data['query_id']
    bm_id = data['bmid']
    output = {
        "message": False,
        "order_id": oid,
        "user_id": uid,
        "bmid": bm_id
    }

    for i in range(st, et, 3600):  # 1hr = 3600 unix time
        rentalperiodcnt += 1

    alteramount = db.session.query(ReservedCarStatus).\
        filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
                    ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et))
    rentalcnt = db.session.query(ReservedCarStatus).\
        filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
                    ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et)).count()

    if (rentalcnt == rentalperiodcnt):
        for i in alteramount:
            i.carAmount = i.carAmount - 1
            print(i.carAmount)
        output.update({
            "price": str(db.session.query(CarQueryRecord).filter(and_(CarQueryRecord.qid == qid, CarQueryRecord.did == did)).first().price),
            "message": True
        })
    else:
        output.update({
            "price": str(db.session.query(CarQueryRecord).filter(and_(CarQueryRecord.qid == qid, CarQueryRecord.did == did)).first().price),
            "message": [rentalcnt, rentalperiodcnt]
        })
        return jsonify(output)

    qdid = db.session.query(CarQueryRecord).filter(
        and_(CarQueryRecord.qid == qid, CarQueryRecord.did == did)).first().id

    order = CarOrderRecord(
        oid=data['order_id'],
        uid=data['user_id'],
        created_at=data['order_time'],
        qd_id=qdid,
        st=data['start_time'],
        et=data['end_time'],
        location=loc,
        item_id=None,
        price=db.session.query(CarQueryRecord).filter(
            and_(CarQueryRecord.qid == qid, CarQueryRecord.did == did)).first().price,
        bmid=bm_id,
        status="Confirmed"
    )
    price = db.session.query(CarQueryRecord).filter(
        and_(CarQueryRecord.qid == qid, CarQueryRecord.did == did)).first().price
    # print(qdid, price)
    db.session.add(order)
    db.session.commit()
    return jsonify(output)


@app.route('/api/order/cancel/car', methods=['GET', 'POST'])
def carordercancellation():
    output = {}
    if request.is_json:
        data = request.json

    # find rental st et,car info
    oid = data['order_id']

    findorder = db.session.query(CarOrderRecord).\
        filter(CarOrderRecord.oid == oid)

    for i in findorder:
        st = i.st
        et = i.et
        loc = i.location
        bm_id = i.bmid
        i.status = 'Canceled'

    # alter car status
    alteramount = db.session.query(ReservedCarStatus).\
        filter(and_(ReservedCarStatus.bmid == bm_id, ReservedCarStatus.location == loc,
                    ReservedCarStatus.carAmount > 0, ReservedCarStatus.date >= st, ReservedCarStatus.date < et))

    for i in alteramount:
        i.carAmount = i.carAmount+1

    # alter resrv status to canceled

    output.update({'message': True, 'order_id': oid})

    db.session.commit()

    return jsonify(output)

# assign item id(car_id)
@app.route('/api/activate/car', methods=['GET', 'POST'])
def activatecar():
    if(request.method == 'POST'):
        print(12344)
    output = {}
    if request.is_json:
        data = request.get_json()
    oid = data['order_id']

    findorder = db.session.query(OrderRecord).\
        filter(OrderRecord.oid == oid).one()

    st = findorder.st
    et = findorder.et
    loc = findorder.location
    price = findorder.price
    uid = findorder.uid
    bmid = findorder.bmid
    findorder.status = 'activated'

    item_id_first = db.session.query(CarAllinfo).filter(
        and_(CarAllinfo.bmid == bmid, CarAllinfo.UsedorNot == False)).first()

    item_id = str(item_id_first.item_id)
    findorder.item_id = item_id
    item_id_first.UsedorNot = True

    # order = OrderRecord(
    #     oid=data['order_id'],
    #     uid=uid,
    #     order_time=data['order_time'],
    #     item_id=item_id,
    #     st=st,
    #     et=et,
    #     location=loc,
    #     bmid=bmid,
    #     # price 應該要用deal id 但目前沒有dynamic pricing 所以就再去db撈一次
    #     price=price,
    #     status="Ongoing"
    # )
    # db.session.add(order)
    db.session.commit()

    output.update({'message': True, 'order_id': oid, 'item_id': item_id})
    return output


@app.route('/api/return/car', methods=['GET', 'POST'])
def returncar():
    output = {}
    if request.is_json:
        data = request.get_json()

    oid = data['order_id']
    item_id = data['item_id']
    findcar = db.session.query(CarAllinfo).filter(
        CarAllinfo.item_id == item_id).one()
    findodr = db.session.query(OrderRecord).filter(
        OrderRecord.oid == oid).one()

    findcar.UsedorNot = False
    findodr.status = "finished"

    db.session.commit()
    output.update({'message': True, 'order_id': oid, 'item_id': item_id})
    return output
