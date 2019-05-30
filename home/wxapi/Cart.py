from home.wxapi import route_api
from flask import request, jsonify, g
from home.models.food.Food import Food
from home.models.member.MemberCart import MemberCart
from home.libs.member.CartService import CartService
from home.libs.Helper import selectFilterObj, getDictFilterField
from home.libs.UrlManager import UrlManager
import json


# 获取购物车
@route_api.route("/cart/index")
def cartIndex():
    resp = {'code': 200, 'msg': '添加购物车成功~', 'data': {}}
    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "获取失败，未登录~~"
        return jsonify(resp)
    cart_list = MemberCart.query.filter_by(member_id=member_info.id).all()  # 所有的car组成列表
    data_cart_list = []
    if cart_list:
        food_ids = selectFilterObj(cart_list, "food_id")  # 从购物车列表中取出id(组成id列表)
        food_map = getDictFilterField(Food, Food.id, "id", food_ids)  # 在food表获得{'id':{food信息}}的字典
        # 传入要查询的表，表的字段，等于food_ids里面的，生成的可以值为id
        for item in cart_list:  # 组装成列表
            tmp_food_info = food_map[item.food_id]  # 取出map信息
            tmp_data = {
                "id": item.id,
                "number": item.quantity,
                "food_id": item.food_id,
                "name": tmp_food_info.name,
                "price": str(tmp_food_info.price),
                "pic_url": UrlManager.buildImageUrl(tmp_food_info.main_image),
                "active": True
            }
            data_cart_list.append(tmp_data)

    resp['data']['list'] = data_cart_list
    return jsonify(resp)


# 加入购物车
@route_api.route("/cart/set", methods=["POST"])
def setCart():
    resp = {'code': 200, 'msg': '添加购物车成功~', 'data': {}}
    req = request.values
    food_id = int(req['id']) if 'id' in req else 0
    number = int(req['number']) if 'number' in req else 0
    if food_id < 1 or number < 1:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-1~~"
        return jsonify(resp)

    member_info = g.member_info  # 会员信息
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-2~~"
        return jsonify(resp)

    food_info = Food.query.filter_by(id=food_id).first()
    if not food_info:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-3~~"
        return jsonify(resp)

    if food_info.stock < number:  # 库存
        resp['code'] = -1
        resp['msg'] = "添加购物车失败,库存不足~~"
        return jsonify(resp)

    ret = CartService.setItems(member_id=member_info.id, food_id=food_info.id, number=number)
    if not ret:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-4~~"
        return jsonify(resp)
    return jsonify(resp)


# 购物车删除
@route_api.route("/cart/del", methods=["POST"])
def delCart():
    resp = {'code': 200, 'msg': '添加购物车成功~', 'data': {}}
    req = request.values
    params_goods = req['goods'] if 'goods' in req else None

    items = []
    if params_goods:
        items = json.loads(params_goods)  # 解析json
    if not items or len(items) < 1:
        return jsonify(resp)

    member_info = g.member_info
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "删除购物车失败-1~~"
        return jsonify(resp)

    ret = CartService.deleteItem(member_id=member_info.id, items=items)
    if not ret:
        resp['code'] = -1
        resp['msg'] = "删除购物车失败-2~~"
        return jsonify(resp)
    return jsonify(resp)
