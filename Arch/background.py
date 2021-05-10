import time
import datetime

from Arch import app, models, methods, db, manager

def skillup():
    while (True):
        skills = models.Skillup.query.all()
        for skill in skills:
            if skill.endtime < datetime.datetime.now():
                if skill.skill == 1:
                    skill.account.skillaccount[0].skill1 += 1
                if skill.skill == 2:
                    skill.account.skillaccount[0].skill2 += 1
                if skill.skill == 3:
                    skill.account.skillaccount[0].skill3 += 1
                if skill.skill == 4:
                    skill.account.skillaccount[0].skill4 += 1
                db.session.delete(skill)
                skill.account.exp += 100

        db.session.commit()
        end_working()
        #db.session.refresh(skills)
        time.sleep(1)

def end_working():
    workings = models.Working.query.all()
    for work in workings:
        if work.endtime < datetime.datetime.now():
            id_item = work.work.iditem
            buf = models.Storage.query.filter(models.Storage.idaccount == work.account.idaccount, models.Storage.iditem == id_item).first()
            if models.Storage.query.filter(models.Storage.idaccount == work.account.idaccount, models.Storage.iditem == id_item).scalar():# Если у игрока есть уже такие итемы
                old_storage = models.Storage.query.filter(models.Storage.idaccount == work.account.idaccount, models.Storage.iditem == id_item).first()
                old_storage.count += work.work.count
            else:#Если у игрока нет этого итема
                new_storage = models.Storage(idaccount=work.account.idaccount, iditem=id_item, count=work.work.count)
                db.session.add(new_storage)
            if models.Countrystorage.query.filter(models.Countrystorage.idcountry == work.account.loc.region.countryregionregion[0].country.idcountry,
                    models.Countrystorage.iditem == work.work.countryitem).scalar():#Если у страны есть такой итем
                old_country_storage = models.Countrystorage.query.filter(models.Countrystorage.idcountry == work.account.loc.region.countryregionregion[0].country.idcountry,
                    models.Countrystorage.iditem == work.work.countryitem).first()
                old_country_storage.count += work.work.countrycount
            else:#Если у страны нет такого итема
                new_country_storage = models.Countrystorage(idcountry=work.account.loc.region.countryregionregion[0].country.idcountry,
                                                            iditem=work.work.countryitem, count=work.work.countrycount)
                db.session.add(new_country_storage)
            db.session.delete(work)
    db.session.commit()

