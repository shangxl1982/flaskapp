from flask import Flask, request
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy
from fib.conf import CONF
from fib.msg_template import ret_msg_template
import json

app = Flask(__name__)
Swagger(app)

@app.route('/fib', methods=['POST'])
def fibapi():
    """
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: data
          properties:
            nstep:
              type: integer
    responses:
      200:
        description: return the data calculated.
      400:
        description: user input has an error
    """
    nstep = request.json.get('nstep')
    if not str(nstep).isdigit():
        msg = ret_msg_template
        msg['errcode'] = 400
        msg['errormsg'] = 'user input has an error'
        return json.dumps(msg), msg['errcode']
    try:
        with ClusterRpcProxy({'AMQP_URI': CONF['amqp_host']}) as rpc:
            msg = rpc.fib.fib(nstep)
    except Exception as e:
        msg['errcode'] = 500
        msg['errormsg'] = 'Lost Rpc connection with backend'
    return json.dumps(msg), msg['errcode']

if __name__ == '__main__':
    app.run(debug=True)
