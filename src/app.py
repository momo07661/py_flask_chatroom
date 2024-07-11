from src import create_app, socketio

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@fsse2401-isaac-db.ctia8gg8am60.ap-southeast-1.rds.amazonaws.com:3306/ChatRoom'
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
#
# db.init_app(app)
#
# with app.app_context():
#     db.create_all()
#
# app.register_blueprint(auth_bp)
# app.register_blueprint(chat_bp)

app = create_app()


if __name__ == '__main__':
    socketio.run(app, debug=True)
