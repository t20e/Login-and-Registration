from flask_app import app
from flask_app.controllers import routes # this connects routes file to server



if __name__=="__main__":
    app.run(debug=True)