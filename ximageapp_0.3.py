from flask import Flask
from config import Config
from routes import main
import effects_aggregator

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)

