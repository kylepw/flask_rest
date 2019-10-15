"""
    views.py
    ~~~~~~~~

    View functions.
"""
from flask import jsonify, request
from flask.views import MethodView
from flask_rest import app, mongo
from flask_rest.exceptions import APIException


@app.errorhandler(400)
def handle_400_errors(e):
    return jsonify(code=400, message='Bad request'), 400

@app.errorhandler(404)
def handle_404_errors(e):
    return jsonify(code=404, message='Not found'), 404

@app.errorhandler(500)
def handle_500_errors(e):
    return jsonify(code=500, message='Internal server error'), 500

@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(errors=[error.to_dict()])
    response.status_code = error.status_code
    return response


class OneCoinAPI(MethodView):

    def get(self, shop_id):
        if shop_id is None:
            return jsonify([result for result in mongo.db.osaka.find().limit(20)])
        shop = mongo.db.osaka.find_one(shop_id)
        if not shop:
            raise APIException('Shop not found with {_id: %s}' % shop_id, 404)
        return jsonify(shop)

    def post(self, shop_id):
        data = request.get_json()
        if not data or 'name' not in data:
            raise APIException('JSON request with name field required', 400)
        mongo.db.osaka.insert_one(data)
        return jsonify({'code': 200, 'message': 'Insertion successful', 'data': data})

    def put(self, shop_id):
        update = mongo.db.osaka.request.get_json()
        print(update)
        #return jsonify(shops[shop_id])
        pass

    def delete(self, shop_id):
        result = mongo.db.osaka.delete_one({"_id": shop_id})
        if result.deleted_count != 1:
            raise APIException('Deletion failed', 400, payload={'_id': str(shop_id)})
        return jsonify({'code': 200, 'message': 'Deletion successful'})


one_coin_view = OneCoinAPI.as_view('one_coin_api')
app.add_url_rule('/api/', defaults={'shop_id': None}, view_func=one_coin_view, methods=['GET', 'POST',])
app.add_url_rule('/api/<ObjectId:shop_id>', view_func=one_coin_view, methods=['GET', 'PUT', 'DELETE'])
