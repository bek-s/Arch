import json
import requests
from sys import platform
from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from Arch import app, models, methods, db, manager

@app.route('/')
def index():
    items = models.Item.query.all()
    if platform == "linux" or platform == "linux2":
        client_id = "7812435"
        redirect_uri = "http://indev.bakasenpai.ru/auth"
    else:
        client_id = "7796629"
        redirect_uri = "http://127.0.0.1:5000/auth"
    return render_template("index.html", client_id=client_id, redirect_uri=redirect_uri)
    #return "<a href='https://oauth.vk.com/authorize?client_id="+client_id+"&display=page&redirect_uri="+redirect_uri+"&&response_type=token&v=5.59'>Тык</a>"

@app.route('/auth', methods = ['GET'])
def gettoken():
    request
    if platform == "linux" or platform == "linux2":
        return "<script>window.location = 'http://indev.bakasenpai.ru/authend?' + window.location.hash.replace('#','');</script>"
    else:
        return "<script>window.location = 'http://127.0.0.1:5000/authend?' + window.location.hash.replace('#','');</script>"

@app.route('/authend', methods = ['GET'])
def save_auth():
    token = request.args.get("access_token")
    user = request.args.get("user_id")
    response = requests.get("https://api.vk.com/method/users.get", params={"user_ids": user, "access_token": token, "fields":"first_name,last_name", "v":"5.130"})
    names = response.json()
    username = names['response'][0]['first_name'] + " " + names['response'][0]['last_name']
    id = names['response'][0]['id']
    login(id, username)
    current_user
    skill = [None, None]
    if len(current_user.skillupacc) != 0:
        skill = [current_user.skillupacc[0].skill, current_user.skillupacc[0].endtime.strftime('%H:%M:%S %d %m %Y')]
    return redirect(url_for("main"))
    #return render_template("mainpage2.html", user=current_user, skill=skill)

@app.route('/main', methods = ['GET'])
def main():
    skill = [None, None]
    if len(current_user.skillupacc) != 0:
        skill = [current_user.skillupacc[0].skill, current_user.skillupacc[0].endtime.strftime('%H:%M:%S %d %m %Y')]
    return render_template("mainpage2.html", user=current_user, skill=skill)


def login(id, username):
    user = models.Account.query.filter(models.Account.socialid == id).first()
    if user is not None:
        login_user(user)
    else:
        new_account = models.Account(socialid=id, exp=0, img='', location=1, name=username)
        res = db.session.add(new_account)
        db.session.commit()
        new_skill = models.Skill(idaccount=new_account.idaccount, skill1=0, skill2=0, skill3=0, skill4=0)
        db.session.add(new_skill)
        db.session.commit()
        login(id, username)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    pass

@app.route('/skillup', methods = ['GET'])
@login_required
def skillup():
    skill = request.args.get("skill")
    if models.Skillup.query.filter(models.Skillup.idaccount == current_user.idaccount).scalar() is None:
        new_s = models.Skillup(idaccount=current_user.idaccount, skill=skill, endtime=datetime.now() + timedelta(minutes=1))
        db.session.add(new_s)
        db.session.commit()
        skill = [None, None]
        if len(current_user.skillupacc) != 0:
            skill = [current_user.skillupacc[0].skill, current_user.skillupacc[0].endtime.strftime('%H:%M:%S %d %m %Y')]
        return json.dumps(["ok", render_template("skills_section.html", skill=skill)])
    else:
        return json.dumps(["err", "basdhtml"])

@app.route('/work', methods = ['GET'])
@login_required
def work():
    current_user
    works = models.Locationwork.query.filter(models.Locationwork.idlocation == current_user.location).all()
    if models.Working.query.filter(models.Working.idaccount == current_user.idaccount).scalar() is not None:
        id = models.Working.query.filter(models.Account.idaccount == current_user.idaccount).first().work.idwork
        endtime = models.Working.query.filter(models.Account.idaccount == current_user.idaccount).first().endtime
    else:
        id = None
        endtime = None
    return render_template("work.html", works=works, data=[id, endtime])

@app.route('/start_working', methods = ['GET'])
@login_required
def start_working():
    idwork = request.args.get("id")
    if models.Working.query.filter(models.Working.idaccount == current_user.idaccount).scalar() is None:
        endtime = datetime.now() + timedelta(minutes=models.Work.query.filter(idwork == idwork).first().time)
        new_working = models.Working(idwork=idwork, idaccount=current_user.idaccount, endtime=endtime)
        db.session.add(new_working)
        db.session.commit()
        return json.dumps(["ok", render_template("work_section.html",
            works=models.Locationwork.query.filter(models.Locationwork.idlocation == current_user.location).all(),
            data=[int(idwork), endtime])])# models.Working.query.filter(idaccount=current_user.idaccount).first()])])
    else:
        return json.dumps(["err", ""])

@app.route('/storage', methods = ['GET'])
@login_required
def storage():
    current_user
    storages = current_user.storageaccount
    return render_template("storage.html", storages=storages)

@app.route('/market', methods = ['GET'])
@login_required
def market():
    current_user
    region = current_user.loc.region
    markets = current_user.loc.region.marketregion
    storages = current_user.storageaccount
    items = models.Item.query.all()
    return render_template("marketExample.html", markets=markets, region=region, storages=storages, items=items)


@app.route('/new_market', methods = ['GET'])
@login_required
def new_market():
    current_user
    item = request.args.get("item")
    item2 = request.args.get("item2")
    count = request.args.get("count")
    cost = request.args.get("cost")
    if (item != None and item != "") and (item2 != None and item2 != "") and (count != None and count  != "") and \
            (cost != None and cost != "") and item.isdigit() and item2.isdigit() and count.isdigit() and cost.isdigit() and \
            models.Item.query.filter(models.Item.iditem == item).scalar() and models.Item.query.filter(models.Item.iditem == item2).scalar():
        account_item_count = models.Storage.query.filter(models.Storage.iditem == item).first()
        if account_item_count.count >= int(count):
            if models.Market.query.filter(models.Market.idaccount == current_user.idaccount,
                                          models.Market.iditem == item, models.Market.iditem2 == item2).scalar():#если такое уже выставлено
                old_market = models.Market.query.filter(models.Market.idaccount == current_user.idaccount,
                                          models.Market.iditem == item, models.Market.iditem2 == item2).first()
                old_market.count += int(count)
                old_market.cost = cost
                account_item_count.count -= int(count)
                db.session.commit()
                return json.dumps(["ok", "Обновлено"])
            else:
                new_market_item = models.Market(idaccount=current_user.idaccount, iditem=item, count=count, cost=cost, iditem2=item2, idregion=current_user.loc.region.idregion)
                db.session.add(new_market_item)
                account_item_count.count -= int(count)
                db.session.commit()
                return json.dumps(["ok", "Выставлено"])
    return json.dumps(["err", "Ошибка"])

@app.route('/buy', methods = ['GET'])
@login_required
def buy():
    current_user
    id_market = request.args.get("id")
    count = request.args.get("count")
    if id_market != None and count != None and id_market != "" and count != "" and count.isdigit() and\
        models.Market.query.filter(models.Market.idmarket == id_market).scalar():
        market = models.Market.query.filter(models.Market.idmarket == id_market).first()
        user_storage = models.Storage.query.filter(models.Storage.idaccount == current_user.idaccount,
                                                   models.Storage.iditem == market.iditem2).first()# То чем платить
        user_need_storage = models.Storage.query.filter(models.Storage.idaccount == current_user.idaccount,
                                                   models.Storage.iditem == market.iditem).first()# То что получит
        price = market.cost * int(count)
        if user_storage == None:#Если нечем платить
            return json.dumps(["err", "Нет нужного товара"])
        else:
            if user_storage.count >= price:#Если точно есть деняк
                if user_need_storage == None:#Если такого ещё нет
                    user_need_storage = models.Storage(idaccount=current_user.idaccount, iditem=market.iditem, count=int(count))
                    user_storage.count -= price
                    market.count -= int(count)
                    db.session.add(user_need_storage)
                else:#Если такое уже есть
                    user_storage.count -= price
                    user_need_storage.count += int(count)
                    market.count -= int(count)
                if models.Storage.query.filter(models.Storage.idaccount==market.idaccount, models.Storage.iditem==market.iditem2).scalar():#Если у продавца есть итем
                    seller_storage = models.Storage.query.filter(models.Storage.idaccount==market.idaccount, models.Storage.iditem==market.iditem2).first()
                    seller_storage.count+=price
                else:#Если у продавца нет итема
                    seller_storage = models.Storage(idaccount=market.idaccount, iditem=market.iditem2, count=price)
                    db.session.add(seller_storage)
                if market.count == 0:
                    db.session.delete(market)
                db.session.commit()
            else:
                return json.dumps(["err", "Нехватает деняк"])
        return json.dumps(["ok", render_template("market_section.html", markets=current_user.loc.region.marketregion), "Куплено"])
    return json.dumps(["err", "Ошибка"])
