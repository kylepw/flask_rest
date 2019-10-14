from exceptions import APIException
from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask(__name__)

# Temp database
shops = [
    {'id': 0,
     'name': 'No Name',
     'hp': 'https://noname',
     'menu': 'https://noname/menu',
     'coordinates': [123, 456]},
     {'id': 1,
     'name': 'とらやん',
     'hp': 'https://torayan',
     'menu': 'https://torayan/menu',
     'coordinates': [890, 123]},
     {'id': 2,
     'name': 'blah',
     'hp': 'https://blah',
     'menu': 'https://blah/menu',
     'coordinates': [678, 923]},
]

@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(errors=[error.to_dict()])
    response.status_code = error.status_code
    return response


class OneCoinAPI(MethodView):
    def get(self, shop_id):
        if shop_id is None:
            return jsonify(shops)
        if shop_id > len(shops) - 1:
            raise APIException('Shop (id: %s) not found' % shop_id, 404)
        return jsonify(shops[shop_id])

    def post(self, shop_id):
        new_entry = dict(
            id=len(shops),
            name=request.json.get('name', ''),
            hp=request.json.get('hp', ''),
            menu=request.json.get('menu', ''),
            coordinates=request.json.get('coordinates', [])
        )
        shops.append(new_entry)
        return jsonify(new_entry)

    def put(self, shop_id):
        shops[request.form['id']] = request.form['data']
        return jsonify(shops[shop_id])
    def delete(self, shop_id):
        pass


one_coin_view = OneCoinAPI.as_view('one_coin_api')
app.add_url_rule('/shops/', defaults={'shop_id': None}, view_func=one_coin_view, methods=['GET', 'POST',])
app.add_url_rule('/shops/<int:shop_id>', view_func=one_coin_view, methods=['GET', 'PUT', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)