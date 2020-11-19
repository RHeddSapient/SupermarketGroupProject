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

class GetRoute(Resource):
    def get(self, s_id, u_id, l_id):
         st = Store.query.get(s_id)
#        map_config = {}
         prod_loc = st.store_map['prod_loc']
#        map_config['dimensions'] = st.store_map['dimensions']
#        map_config['obstacles'] = st.store_map['obstacles']
#        print(prod_loc)
#        print(map_config)
         list = List.query.get(l_id)
         list_prod = ListProduct.query.filter_by(list_id = list.id).all()
         locs = []
         for lp in list_prod:
             locs.append(prod_loc[lp.product_id-1][1])
         position = Locations.query.filter_by(store_id = s_id, user_id = u_id).first()

         start_pos = []
         if not position:
            start_pos = [0,0]
         else:
            start_pos = [position.x_loc, position.y_loc]

         username = User.query.get(u_id).username
            
         

         agent_config = {"username":username, "start_position": start_pos, "item_coords":locs}



         return agent_config


        

        
        
        
        

api.add_resource(MicroTest, "/test/")
api.add_resource(DistributeProducts, "/<int:s_id>/setproducts/")
api.add_resource(GetRoute, "/<int:s_id>/<int:u_id>/<int:l_id>/route/")

if __name__ == "__main__":
    app.run(port=5002,debug=True)
