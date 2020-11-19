from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from project.scripts import *
from project.place_products import prod_coords


app = Flask(__name__)
api = Api(app)

app.config.from_object("project.config.Config")

from project.models import *

    
class MicroTest(Resource):
    def get(self):
        return {"Message": "Route Calc"}


class DistributeProducts(Resource):
    def get(self, s_id):
        st = Store.query.get(s_id)
        pr = Product.query.all()
        dimensions = st.store_map['dimensions']
        obstacles = st.store_map['obstacles']
        store_map = st.store_map

        prod_c = prod_coords(dimensions, obstacles)

        prod_loc = []
        x = 0
        for prod in pr:
            prod_loc.append([prod.id,prod_c[x]])
            x+=1

        store_map['prod_loc'] = prod_loc
        st.store_map = store_map
        print(store_map)
        db.session.commit()
            
        return {"Success":1}

        
        
        

api.add_resource(MicroTest, "/test/")
api.add_resource(DistributeProducts, "/<int:s_id>/setproducts/")

if __name__ == "__main__":
    app.run(port=5002,debug=True)
