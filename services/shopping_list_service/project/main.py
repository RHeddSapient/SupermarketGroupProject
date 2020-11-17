from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from project.scripts import *


app = Flask(__name__)
api = Api(app)

app.config.from_object("project.config.Config")

from project.models import *

class MicroTest(Resource):
    def get(self):
        return {"Message": "Shop List"}

class UserList(Resource):
    def get(self, u_id):
        lists = List.query.filter(user_id = u_id)
        output_list = []

        for list in lists:
            contents = [ {"id": list.id, "title":list.title, "products": [{"id": prod.id, 
                         "name":prod.prod_name, "category":prod.prod_category, "stocked":prod.stocked} 
                         for prod in ListProduct.query.filter(list_id= list.id)] } ]
            output_list.append(contents)
        return jsonify(output_list)

    def post(self, u_id):
        json_data = request.get_json(force=True)

        new_list = List(user_id=u_id, title=json_data['title'])
        db.session.add(new_list)
        db.session.commit()

        return {"Success":1, "id": new_list.id}

class ChangeList(Resource):
    ## add product
    def post(self, u_id, l_id):
        json_data = request.get_json(force=True)
        new_list_product = ListProduct(product_id = json_data['product_id'], list_id = l_id)

        db.session.add(new_list_product)
        db.session.commit()

        return {"Success":1}

    ## delete list
    def delete(self, u_id, l_id):
        ListProduct.query.filter(list_id=l_id).delete()
        List.query.filter(id=l_id).delete()

        db.session.commit()

        return {"Success":1}

    ## update list name
    def put(self, u_id, l_id):
        json_data = request.get_json(force=True)

        list = List.query.filter(id=l_id)
        list.title = json_data['title']

        db.session.commit()

        return {"Success":1}

    ## return list
    def get(self, u_id, l_id):
            list = List.query.filter(id=l_id).first()
            contents = [
                        {"id": list.id, "title":list.title, "products": 
                            [{"id": prod.id, "name":prod.prod_name, "category":prod.prod_category, "stocked":prod.stocked} for prod
                                in ListProduct.query.filter(list_id= list.id)]
                        }
                       ]
            return jsonify(contents)


class DeleteFromList(Resource):
    def delete(self, u_id, l_id, p_id):
        ListProduct.query.filter(product_id=p_id, list_id=l_id).delete()
        db.session.commit()

        return {"Success":1}

class GetAllProducts(Resource):
    def get(self):
        st = Product.query.all()
        all_products = [{"id": prod.id, "name":prod.prod_name, "category":prod.prod_category, 
                        "stocked":prod.stocked} for product in st]

        return jsonify(all_products)

        

        
api.add_resource(MicroTest, "/test/" )
api.add_resource(UserList, "/<int:u_id>/")
api.add_resource(ChangeList, "/<int:u_id>/<int:l_id>/")
api.add_resource(DeleteFromList, "/<int:u_id>/<int:l_id>/<int:p_id>/")
api.add_resource(GetAllProducts, "/allproducts/")

if __name__ == "__main__":
    app.run(port = 5001, debug=True)
