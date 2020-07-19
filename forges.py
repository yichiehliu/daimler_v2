import random
from faker import Faker
import time
from faker_vehicle import VehicleProvider
from app import db
from app import ScooterAllinfo, FONLoc, ReservedScooterStatus, ScooterQueryRecord, ScooterOrderRecord
from app import CarAllinfo, RealtimeCarDetails, RealtimeCarOrderRecord, ReservedCarStatus, CarQueryRecord, CarOrderRecord

from sqlalchemy import and_, func

fake = Faker()
fake.add_provider(VehicleProvider)


def fake_longnla():
    # for i in range(cnt):
    loc1 = FONLoc(
        loc=1,
        longnla=str("(25.016695, 121.543692)")
    )
    db.session.add(loc1)
    loc2 = FONLoc(
        loc=2,
        longnla=str("(25.021295, 121.539112)")
    )
    db.session.add(loc2)
    loc3 = FONLoc(
        loc=3,
        longnla=str("(25.019808, 121.541526)")
    )
    db.session.add(loc3)
    db.session.commit()


def fake_scooter(cnt=10):

    for i in range(cnt):
        Scooter = ScooterAllinfo(bmid=10021 + random.randint(1, 2),
                                 sub_type='Escooter',
                                 brand_id='Gogoro',
                                 model_id='VIVA',
                                 price=random.randint(1, 3),
                                 location=random.randint(1, 3),
                                 UsedorNot=False)
        db.session.add(Scooter)
    db.session.commit()


def fake_scooter_status():
    time_slot = 744  # a month
    data_created = int(time.time())
    loc_list = []
    bm_list = []
    all_list = db.session.query(ScooterAllinfo).all()
    cnt_bm = db.session.query(ScooterAllinfo).group_by(
        ScooterAllinfo.bmid).count()  # having(func.count('*')
    bm_list_v = db.session.query(
        ScooterAllinfo.bmid).group_by(ScooterAllinfo.bmid).all()
    cnt_loc = db.session.query(ScooterAllinfo).group_by(
        ScooterAllinfo.location).count()
    loc_list_v = db.session.query(ScooterAllinfo).group_by(
        ScooterAllinfo.location).all()
    for i in loc_list_v:
        loc_list.append(i.location)
    for i in bm_list_v:
        bm_list.append(i.bmid)

    for i in range(data_created, data_created + 3600*time_slot, 3600):
        for j in loc_list:
            for k in bm_list:
                csta1 = ReservedScooterStatus(
                    date=i,
                    location=j,
                    # db.session.query(ScooterAllinfo.location).order_by(func.random()).limit(1),
                    bmid=k,
                    # db.session.query(ScooterAllinfo.bmid).\
                    # filter(ScooterAllinfo.location == '1').order_by(
                    #     func.random()).limit(1),
                    ScooterAmount=db.session.query(ScooterAllinfo.bmid).\
                    filter(and_(ScooterAllinfo.bmid == k, ScooterAllinfo.location == j)).count())
                db.session.add(csta1)

    db.session.commit()


def fake_car(cnt=10):

    for i in range(cnt):
        car = CarAllinfo(bmid=1000021 + random.randint(1, 2),
                         sub_type=fake.vehicle_category(),
                         brand_id=fake.vehicle_make(),
                         model_id=fake.vehicle_model(),
                         price=random.randint(2, 7),
                         location=random.randint(1, 3),
                         UsedorNot=False)
        db.session.add(car)
    db.session.commit()


def fake_car_status():
    time_slot = 744  # a month
    data_created = int(time.time())
    loc_list = []
    bm_list = []
    all_list = db.session.query(CarAllinfo).all()
    cnt_bm = db.session.query(CarAllinfo).group_by(
        CarAllinfo.bmid).count()  # having(func.count('*')
    bm_list_v = db.session.query(
        CarAllinfo.bmid).group_by(CarAllinfo.bmid).all()
    cnt_loc = db.session.query(CarAllinfo).group_by(
        CarAllinfo.location).count()
    loc_list_v = db.session.query(CarAllinfo).group_by(
        CarAllinfo.location).all()
    for i in loc_list_v:
        loc_list.append(i.location)
    for i in bm_list_v:
        bm_list.append(i.bmid)

    for i in range(data_created, data_created + 3600*time_slot, 3600):
        for j in loc_list:
            for k in bm_list:
                csta1 = ReservedCarStatus(
                    date=i,
                    location=j,
                    # db.session.query(CarAllinfo.location).order_by(func.random()).limit(1),
                    bmid=k,
                    # db.session.query(CarAllinfo.bmid).\
                    # filter(CarAllinfo.location == '1').order_by(
                    #     func.random()).limit(1),
                    carAmount=db.session.query(CarAllinfo.bmid).\
                    filter(and_(CarAllinfo.bmid == k, CarAllinfo.location == j)).count())
                db.session.add(csta1)

    db.session.commit()
