from flask import Flask, request
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}

ret_msg_template = {'result':None, 'errcode':200, 'errormsg':"" }

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

    msg = rpc.fib.fib(nstep)
    return json.dumps(msg), msg['errcode']

app.run(debug=True)
