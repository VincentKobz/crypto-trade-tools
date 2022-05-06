from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
import pandas as pd
from pandas_ta import performance
import src.test_all as test

app = Flask(__name__)
api = Api(app)

# SETUP CORS
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

parser = reqparse.RequestParser()

parser.add_argument('pair', required=True)
parser.add_argument('strategy', required=True)
parser.add_argument('wallet', required=True)
parser.add_argument('interval', required=True)
parser.add_argument('start', required=True)
parser.add_argument('maker_fee', required=True)
parser.add_argument('taker_fee', required=True)
parser.add_argument('test_all', required=True)
parser.add_argument('optimize', required=True)

res = [('None', 'None', 'None', 'None', 'None')]

class Results(Resource):
    def get(self):
        is_all = len(res) > 1
        new_data = pd.DataFrame({
                    'test_all': is_all,
                    'res': [res]
        }, index=[0])
        print(new_data)

        return {'data': new_data.to_dict()}, 200

class Calculate(Resource):
    def post(self):
        print("OK")
        args = parser.parse_args()
        print(args)
        res_temp = test.launch_backtracing(args['test_all'], args['pair'], args['start'], args['interval'], args['strategy'], args['wallet'], args['taker_fee'], args['maker_fee'])

        return {'data': res_temp}, 200

api.add_resource(Results, '/result')
api.add_resource(Calculate, '/calculate')
    
if __name__ == '__main__':
    app.run()