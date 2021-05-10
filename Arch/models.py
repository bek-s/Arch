from flask_login import UserMixin

from Arch import db, manager


class Account(db.Model):
    idaccount = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    socialid = db.Column(db.Integer, nullable=False)
    exp = db.Column(db.BigInteger, nullable=False)
    img = db.Column(db.String(200), nullable=False)
    location = db.Column(db.Integer, db.ForeignKey("location.idlocation"), nullable=False)
    loc = db.relationship("Location", backref=db.backref("accountlocation", lazy=True))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idaccount


@manager.user_loader
def load_user(id):
    try:
        return Account.query.filter(Account.idaccount == id).first()
    except:
        None


class Armyunit(db.Model):
    idarmyunit = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200), nullable=False)


class Item(db.Model):
    iditem = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    range = db.Column(db.Integer, nullable=False)
    effect = db.Column(db.String(200), nullable=True)


class Work(db.Model):
    idwork = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    countrycount = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    iditem = db.Column(db.Integer, db.ForeignKey("item.iditem"), nullable=False)
    countryitem = db.Column(db.Integer, db.ForeignKey("item.iditem"), nullable=False)
    item = db.relationship("Item", backref=db.backref("workitem", lazy=True), primaryjoin='Work.iditem == Item.iditem')
    fcountryitem = db.relationship("Item", backref=db.backref("workcountryitem"), lazy=True, primaryjoin='Work.countryitem == Item.iditem')


class Market(db.Model):
    idmarket = db.Column(db.Integer, primary_key=True)
    idaccount = db.Column(db.Integer, db.ForeignKey("account.idaccount"), nullable=False)
    account = db.relationship("Account", backref=db.backref("mamrketaccount", lazy=True))
    iditem = db.Column(db.Integer, db.ForeignKey("item.iditem"), nullable=False)
    iditem2 = db.Column(db.Integer, db.ForeignKey("item.iditem"), nullable=False)
    item = db.relationship("Item", backref=db.backref("marketitem", lazy=True), primaryjoin='Market.iditem == Item.iditem')
    item2 = db.relationship("Item", backref=db.backref("market2item", lazy=True), primaryjoin='Market.iditem2 == Item.iditem')
    count = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    idregion = db.Column(db.Integer, db.ForeignKey("region.idregion"), nullable=False)
    region = db.relationship("Region", backref=db.backref("marketregion", lazy=True))


class Storage(db.Model):
    storage = db.Column(db.Integer, primary_key=True)
    idaccount = db.Column(db.Integer, db.ForeignKey("account.idaccount"), nullable=False)
    account = db.relationship("Account", backref=db.backref("storageaccount", lazy=True))
    iditem = db.Column(db.Integer, db.ForeignKey("item.iditem"), nullable=False)
    item = db.relationship("Item", backref=db.backref("storageitem", lazy=True))
    count = db.Column(db.Integer, nullable=False)


class Skill(db.Model):
    idskill = db.Column(db.Integer, primary_key=True)
    idaccount = db.Column(db.Integer, db.ForeignKey("account.idaccount"), nullable=False)
    account = db.relationship("Account", backref=db.backref("skillaccount", lazy=True))
    skill1 = db.Column(db.Integer, nullable=False)
    skill2 = db.Column(db.Integer, nullable=False)
    skill3 = db.Column(db.Integer, nullable=False)
    skill4 = db.Column(db.Integer, nullable=False)


class Inarmy(db.Model):
    idinarmy = db.Column(db.Integer, primary_key=True)
    idaccount = db.Column(db.Integer, db.ForeignKey("account.idaccount"), nullable=False)
    account = db.relationship("Account", backref=db.backref("inarmyaccount", lazy=True))
    idarmyunit = db.Column(db.Integer, db.ForeignKey("armyunit.idarmyunit"), nullable=False)
    unit = db.relationship("Armyunit", backref=db.backref("storageitem", lazy=True))
    count = db.Column(db.Integer, nullable=False)


class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idlocation = db.Column(db.Integer, db.ForeignKey("location.idlocation"), nullable=False)
    location = db.relationship("Location", backref=db.backref("resourseslocation", lazy=True))
    res1 = db.Column(db.Integer, nullable=False)
    res2 = db.Column(db.Integer, nullable=False)
    res3 = db.Column(db.Integer, nullable=False)
    res4 = db.Column(db.Integer, nullable=False)
    res5 = db.Column(db.Integer, nullable=False)
    res6 = db.Column(db.Integer, nullable=False)
    res7 = db.Column(db.Integer, nullable=False)
    res8 = db.Column(db.Integer, nullable=False)


class Location(db.Model):
    idlocation = db.Column(db.Integer, primary_key=True)
    idregion = db.Column(db.Integer, db.ForeignKey("region.idregion"), nullable=False)
    region = db.relationship("Region", backref=db.backref("locationregion", lazy=True))
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    effects = db.Column(db.String(200), nullable=True)
    idtypelocation = db.Column(db.Integer, db.ForeignKey("typelocation.idtypelocation"), nullable=False)
    typelocation = db.relationship("Typelocation", backref=db.backref("locationtype", lazy=True))


class Region(db.Model):
    idregion = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    infr1 = db.Column(db.Integer, nullable=False)
    infr2 = db.Column(db.Integer, nullable=False)
    infr3 = db.Column(db.Integer, nullable=False)
    infr4 = db.Column(db.Integer, nullable=False)
    infr5 = db.Column(db.Integer, nullable=False)
    infr6 = db.Column(db.Integer, nullable=False)
    infr7 = db.Column(db.Integer, nullable=False)
    infr8 = db.Column(db.Integer, nullable=False)


class Typelocation(db.Model):
    idtypelocation = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200), nullable=False)


class Typelocationeffect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idtypelocation = db.Column(db.Integer, db.ForeignKey("typelocation.idtypelocation"), nullable=False)
    typeloc = db.relationship("Typelocation", backref=db.backref("effecttypelocation", lazy=True))
    ideffect = db.Column(db.Integer, db.ForeignKey("effect.ideffect"), nullable=False)
    effect = db.relationship("Effect", backref=db.backref("typelocationeffect12", lazy=True))


class Effectsregion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idregion = db.Column(db.Integer, db.ForeignKey("region.idregion"), nullable=False)
    efreg = db.relationship("Region", backref=db.backref("efregin", lazy=True))
    ideffect = db.Column(db.Integer, db.ForeignKey("effect.ideffect"), nullable=False)
    effect = db.relationship("Effect", backref=db.backref("typeregeffect12", lazy=True))


class Effectslocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idlocation = db.Column(db.Integer, db.ForeignKey("location.idlocation"), nullable=False)
    efloc = db.relationship("Location", backref=db.backref("efregin", lazy=True))
    ideffect = db.Column(db.Integer, db.ForeignKey("effect.ideffect"), nullable=False)
    effect = db.relationship("Effect", backref=db.backref("typelocationeffect11", lazy=True))


class Effect(db.Model):
    ideffect = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    effects = db.Column(db.String(200), nullable=False)

class Skillup(db.Model):
    idskillup = db.Column(db.Integer, primary_key=True)
    idaccount = db.Column(db.Integer, db.ForeignKey("account.idaccount"), nullable=False)
    account = db.relationship("Account", backref=db.backref("skillupacc", lazy=True))
    skill = db.Column(db.Integer, nullable=False)
    endtime = db.Column(db.TIMESTAMP, nullable=False)

class Locationwork(db.Model):
    idlocationwork = db.Column(db.Integer, primary_key=True)
    idwork = db.Column(db.Integer, db.ForeignKey("work.idwork"), nullable=False)
    work = db.relationship("Work", backref=db.backref("locationworkwork", lazy=True))
    idlocation = db.Column(db.Integer, db.ForeignKey("location.idlocation"), nullable=False)
    location = db.relationship("Location", backref=db.backref("locationworklocation", lazy=True))

class Working(db.Model):
    idworking = db.Column(db.Integer, primary_key=True)
    idwork = db.Column(db.Integer, db.ForeignKey("work.idwork"), nullable=False)
    work = db.relationship("Work", backref=db.backref("workingwork", lazy=True))
    idaccount = db.Column(db.Integer, db.ForeignKey("account.idaccount"), nullable=False)
    account = db.relationship("Account", backref=db.backref("workingaccount", lazy=True))
    endtime = db.Column(db.TIMESTAMP, nullable=False)

class Countrystorage(db.Model):
    idcountrystorage = db.Column(db.Integer, primary_key=True)
    idcountry = db.Column(db.Integer, db.ForeignKey("country.idcountry"), nullable=False)
    country = db.relationship("Country", backref=db.backref("countrystoragecountry", lazy=True))
    iditem = db.Column(db.Integer, db.ForeignKey("item.iditem"), nullable=False)
    item = db.relationship("Item", backref=db.backref("countrystorageitem", lazy=True))
    count = db.Column(db.Integer, nullable=False)

class Countryregion(db.Model):
    idcountryregion = db.Column(db.Integer, primary_key=True)
    idcountry = db.Column(db.Integer, db.ForeignKey("country.idcountry"), nullable=False)
    country = db.relationship("Country", backref=db.backref("countryregioncountry", lazy=True))
    idregion= db.Column(db.Integer, db.ForeignKey("region.idregion"), nullable=False)
    region = db.relationship("Region", backref=db.backref("countryregionregion", lazy=True))

class Country(db.Model):
    idcountry = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(200), nullable=False)
