from flask import jsonify, request
from flask.views import MethodView
from flask_rest import app, mongo
from flask_rest.exceptions import APIException


@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(errors=[error.to_dict()])
    response.status_code = error.status_code
    return response


class OneCoinAPI(MethodView):

    def get(self, shop_id):
        if shop_id is None:
            results = []
            for r in mongo.db.osaka.find().limit(20):
                r['_id'] = str(r['_id'])
                results.append(r)
            return jsonify(results)
        shop = mongo.db.osaka.find_one(shop_id)
        shop['_id'] = str(shop['_id'])
        if not shop:
            raise APIException('Shop not found', 404)
        return jsonify(shop)

    def post(self, shop_id):
        pass

    def put(self, shop_id):
        #updated_shop = mongo.db.osaka.request.form['data']
        #return jsonify(shops[shop_id])
        pass
    def delete(self, shop_id):
        pass


one_coin_view = OneCoinAPI.as_view('one_coin_api')
app.add_url_rule('/shops/', defaults={'shop_id': None}, view_func=one_coin_view, methods=['GET', 'POST',])
app.add_url_rule('/shops/<ObjectId:shop_id>', view_func=one_coin_view, methods=['GET', 'PUT', 'DELETE'])
