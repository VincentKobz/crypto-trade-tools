from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
from pandas_ta import performance
import src.main_backtracing

app = Flask(__name__)
api = Api(app)

botWallet = 0
holdWallet = 0
totalFees = 0
performanceHold = 0

class Results(Resource):
    def get(self):
        new_data = pd.DataFrame({
                    'botWallet': botWallet,
                    'holdWallet': holdWallet,
                    'totalFees': totalFees,
                    'performanceHold': performanceHold,
        }, index=[0])
        print(botWallet)

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

        print('receive');

        (temp_bot, temp_hold, temp_fees, temp_perf) = src.main_backtracing.launch_analysis(args['pair'], args['start'], args['interval'], args['strategy'], args['wallet'], args['taker_fee'], args['maker_fee'])

        global botWallet
        global holdWallet
        global totalFees
        global performanceHold
        botWallet = temp_bot
        holdWallet = temp_hold
        totalFees = temp_fees
        performanceHold = temp_perf

        return {'data': new_data.to_dict()}, 200

api.add_resource(Results, '/result')
api.add_resource(Parameters, '/parameter')
    
if __name__ == '__main__':
    app.run()  # run our Flask app