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
    ## get lists x
    def get(self, u_id):
        lists = List.query.filter_by(user_id = u_id)
        output_list = []

        for list in lists:
            list_prod = ListProduct.query.filter_by(list_id = list.id).all()
            prod_ids = []
            for lp in list_prod:
                prod_ids.append(lp.product_id)

            prods = Product.query.filter(Product.id.in_(prod_ids)).all()

            contents = [{"id": prod.id, "name":prod.prod_name, "category":prod.prod_category, "stocked":prod.stocked} for prod
                                in prods]
            list_data= [
                        {"id": list.id, "title":list.title, "products": contents
                        }
                       ]
            output_list.append(list_data)
        return jsonify(output_list)


    ## new list with title x
    def post(self, u_id):
        json_data = request.get_json(force=True)


        us = User.query.get(u_id)
        list = List.query.filter_by(user_id=u_id,  title=json_data['title']).first()

        if list:
            return {"Success":0, "id": list.id, "Exists":1}


        new_list = List(user_id=u_id, title=json_data['title'])
        db.session.add(new_list)
        db.session.flush()
        new_list_id  = new_list.id
        db.session.commit()

        return {"Success":1, "id": new_list_id, "Exists":0}

class ChangeList(Resource):
    ## add product x
    def post(self, u_id, l_id):
        json_data = request.get_json(force=True)


        list_p = ListProduct.query.filter_by(product_id=json_data['product_id'], list_id = l_id).first()
        
        if list_p:
            return {"Success":0, "Exists":1}

        new_list_product = ListProduct(product_id = json_data['product_id'], list_id = l_id)

        db.session.add(new_list_product)
        db.session.commit()

        return {"Success":1, "Exists":0}

    ## delete list x
    def delete(self, u_id, l_id):
        ListProduct.query.filter_by(list_id=l_id).delete()
        ls = List.query.get(l_id)

        db.session.delete(ls)
        db.session.commit()

        return {"Success":1}

    ## update list name x
    def put(self, u_id, l_id):
        json_data = request.get_json(force=True)

        list = List.query.get(l_id)
        list.title = json_data['title']

        db.session.commit()

        return {"Success":1}

    ## return list x
    def get(self, u_id, l_id):
            list = List.query.get(l_id)
            list_prod = ListProduct.query.filter_by(list_id = list.id).all()
            prod_ids = []
            for lp in list_prod:
                prod_ids.append(lp.product_id)

            prods = Product.query.filter(Product.id.in_(prod_ids)).all()

            contents = [{"id": prod.id, "name":prod.prod_name, "category":prod.prod_category, "stocked":prod.stocked} for prod
                                in prods]
            output_list= [
                        {"id": list.id, "title":list.title, "products": contents
                        }
                       ]
            return jsonify(contents)


class DeleteFromList(Resource):
    # delete product from list x
    def delete(self, u_id, l_id, p_id):
        lp = ListProduct.query.filter_by(product_id=p_id, list_id=l_id).first()

        if not lp:
            return {"Success":0, "Exists":0}
            
        db.session.delete(lp)
        db.session.commit()

        return {"Success":1, "Exists":1}

class GetAllProducts(Resource):
    # return all products x
    def get(self):
        st = Product.query.all()

        all_products = [{"id": prod.id, "name":prod.prod_name, "category":prod.prod_category, 
                        "stocked":prod.stocked} for prod in st]

        return jsonify(all_products)

        

        
api.add_resource(MicroTest, "/test/" )
api.add_resource(UserList, "/<int:u_id>/")
api.add_resource(ChangeList, "/<int:u_id>/<int:l_id>/")
api.add_resource(DeleteFromList, "/<int:u_id>/<int:l_id>/<int:p_id>/")
api.add_resource(GetAllProducts, "/allproducts/")

if __name__ == "__main__":
    app.run(port = 5001, debug=True)
