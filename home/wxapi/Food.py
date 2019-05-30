from home.wxapi import route_api
from flask import request, jsonify, g
from home.models.food.FoodCat import FoodCat
from home.models.food.Food import Food
from home.models.member.MemberCart import MemberCart
from home.libs.UrlManager import UrlManager
from sqlalchemy import or_


@route_api.route("/food/index")
def foodIndex():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    cat_list = FoodCat.query.filter_by(status=1).order_by(FoodCat.weight.desc()).all()  # 取出类别
    data_cat_list = []
    data_cat_list.append({
        'id': 0,
        'name': "全部"
    })
    if cat_list:  # 若果类别不为空，组装为字典
        for item in cat_list:
            tmp_data = {  # 字典类型
                'id': item.id,
                'name': item.name
            }
            data_cat_list.append(tmp_data)
    resp['data']['cat_list'] = data_cat_list

    # 轮播图，获取销售量较大的
    food_list = Food.query.filter_by(status=1) \
        .order_by(Food.total_count.desc(), Food.id.desc()).limit(3).all()

    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)

    resp['data']['banner_list'] = data_food_list  # 字典中有{'banner_list':[{},{}]}
    return jsonify(resp)


# 搜索信息
@route_api.route("/food/search")
def foodSearch():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0  # 要搜索的菜品类别
    mix_kw = str(req['mix_kw']) if 'mix_kw' in req else ''  # 搜索关键字
    p = int(req['p']) if 'p' in req else 1  # 分页

    if p < 1:
        p = 1

    page_size = 10  # 总页数
    offset = (p - 1) * page_size  # 当前页数
    query = Food.query.filter_by(status=1)  # 搜索对象
    if cat_id > 0:
        query = query.filter_by(cat_id=cat_id)
    if mix_kw:
        rule = or_(Food.name.ilike("%{0}%".format(mix_kw)), Food.tags.ilike("%{0}%".format(mix_kw)))
        query = query.filter(rule)

    # limit每页数量
    food_list = query.order_by(Food.total_count.desc(), Food.id.desc()) \
        .offset(offset).limit(page_size).all()

    data_food_list = []  # 返回的列表

    if food_list:
        for item in food_list:
            tmp_data = {
                'id': item.id,
                'name': "%s" % (item.name),
                'price': str(item.price),
                'min_price': str(item.price),
                'pic_url': UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)

    resp['data']['list'] = data_food_list
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1  # 是否还有数据
    return jsonify(resp)


# 详细信息
@route_api.route("/food/info")
def foodInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0  # 获得id
    food_info = Food.query.filter_by(id=id).first()
    if not food_info or not food_info.status:
        resp['code'] = -1
        resp['msg'] = "美食已下架"
        return jsonify(resp)

    member_info = g.member_info   # 详情页中的购物车，得到用户id
    cart_number = 0  # 数量默认为0
    if member_info:
        cart_number = MemberCart.query.filter_by(member_id=member_info.id).count()  # 购物车模型查询数量
    resp['data']['info'] = {
        "id": food_info.id,
        "name": food_info.name,
        "summary": food_info.summary,
        "total_count": food_info.total_count,
        "comment_count": food_info.comment_count,
        'main_image': UrlManager.buildImageUrl(food_info.main_image),
        "price": str(food_info.price),
        "stock": food_info.stock,   # 库存量
        "pics": [UrlManager.buildImageUrl(food_info.main_image)]
    }
    resp['data']['cart_number'] = cart_number
    return jsonify(resp)


# @route_api.route("/food/comments")
# def foodComments():
#     resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
#     req = request.values
#     id = int(req['id']) if 'id' in req else 0
#     query = MemberComments.query.filter(MemberComments.food_ids.ilike("%_{0}_%".format(id)))
#     list = query.order_by(MemberComments.id.desc()).limit(5).all()
#     data_list = []
#     if list:
#         member_map = getDictFilterField(Member, Member.id, "id", selectFilterObj(list, "member_id"))
#         for item in list:
#             if item.member_id not in member_map:
#                 continue
#             tmp_member_info = member_map[item.member_id]
#             tmp_data = {
#                 'score': item.score_desc,
#                 'date': item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
#                 "content": item.content,
#                 "user": {
#                     'nickname': tmp_member_info.nickname,
#                     'avatar_url': tmp_member_info.avatar,
#                 }
#             }
#             data_list.append(tmp_data)
#     resp['data']['list'] = data_list
#     resp['data']['count'] = query.count()
#     return jsonify(resp)
