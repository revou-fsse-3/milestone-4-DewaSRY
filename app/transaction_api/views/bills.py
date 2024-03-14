



from flask_smorest import Blueprint, abort
from flask.views import MethodView
from http import HTTPStatus
from flask_jwt_extended import jwt_required

from app.transaction_api.service.DbModelService import DbModelService
from app.transaction_api.schemas.bills import (
        BillBaseSchemas,
        BillCreateSchemas,
        BillResponseSchemas,
        BillUpdateSchemas
    )

from app.transaction_api.model.bills import BillsModel
from app.transaction_api.util.JWTGetters import getCurrentAuthId

blp= Blueprint("bills", __name__, description="""
               bills management 
               """)
DBS= DbModelService(BillsModel)


@blp.route("/bills")
class billsViews(MethodView):
    @jwt_required()
    @blp.arguments(BillBaseSchemas)
    @blp.response(HTTPStatus.CREATED, BillResponseSchemas)
    def post(self, bills_data):
        "Create a new bills payment for specific biller"
        createSchemas=BillCreateSchemas()
        currentId=getCurrentAuthId()
        billsModel= createSchemas.load({
            **bills_data,
            'user_id':currentId
        })
        return DBS.addModel(billsModel)
    
    @jwt_required()
    @blp.response(HTTPStatus.OK, BillResponseSchemas(many=True))
    def get(self):
        "Retrieve all bills scheduled bill payment"
        currentId=getCurrentAuthId()
        billsList= BillsModel.query.filter(BillsModel.user_id== currentId).all()
        if len(billsList) == 0:
            abort(HTTPStatus.CONFLICT ,message="current user does't have any bills" )
        return billsList

@blp.route("/bills/<string:bills_id>")
class billViews(MethodView):
    @jwt_required()
    @blp.arguments(BillUpdateSchemas)
    @blp.response(HTTPStatus.CREATED, BillResponseSchemas)
    def put(self,bills_data,bills_id):
        "update an existing bills"
        print("hite")
        print(bills_data)
        try: 
            return DBS.updateDbModel(bills_id, bills_data)
        except Exception as e:
            print(e)
            abort(HTTPStatus.CONFLICT,message="failed while updating bills" )
            
    @jwt_required()
    def delete(self,bills_id):
        "cancel a scheduled  bill payment "
        DBS.deleteDbModal(bills_id)
        return {"message": "Item deleted."},HTTPStatus.OK