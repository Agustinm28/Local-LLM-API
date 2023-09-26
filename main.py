from website import create_app
from utils.config import Config

if __name__ == '__main__':

    app = create_app(Config)
    port = Config.PORT
    host = Config.HOST 
    app.run(port=port, host=host)