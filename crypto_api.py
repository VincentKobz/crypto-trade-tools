from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
from pandas_ta import performance
import src.main_backtracing
import src.test_all as test

app = Flask(__name__)
api = Api(app)

botWallet = 0
holdWallet = 0
totalFees = 0
performanceHold = 0

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

class Parameters(Resource):
    def post(self):
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
        
        args = parser.parse_args()
        
        new_data = pd.DataFrame({
            'pair': args['pair'],
            'strategy': args['strategy'],
            'wallet': args['wallet'],
            'interval': args['interval'],
            'start': args['start'],
            'maker_fee': args['maker_fee'],
            'taker_fee': args['taker_fee'],
        }, index=[0])

        print(args['test_all'])
        print('receive');

        res_temp = test.launch_backtracing(args['test_all'], args['pair'], args['start'], args['interval'], args['strategy'], args['wallet'], args['taker_fee'], args['maker_fee'])
        print(res_temp)
        global res
        res = res_temp

        return {'data': new_data.to_dict()}, 200

api.add_resource(Results, '/result')
api.add_resource(Parameters, '/parameter')
    
if __name__ == '__main__':
    app.run()  # run our Flask app