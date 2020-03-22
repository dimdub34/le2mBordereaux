from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '169944cb18b918a084db8f6d24df1240'

from le2mBordereaux import routes
