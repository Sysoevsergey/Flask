import sqlalchemy
from flask import Flask, jsonify, request, Response
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from models import User,Advertisement, Session
from errors import HttpError
from schema import validate, CreateUser, UpdateUser
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt = Bcrypt(app)


def hash_password(password: str):
    password_bytes = password.encode()
    hashed_password_bytes = bcrypt.generate_password_hash(password_bytes)
    hashed_password = hashed_password_bytes.decode()
    return hashed_password

def check_password(client_password: str, hashed_password: str):
    client_password = client_password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(hashed_password, client_password)


@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response: Response):
    request.session.close()
    return response

@app.errorhandler(HttpError)
def error_errorhandler(err: HttpError):
    json_response = jsonify({'status':'error', 'message': err.message})
    json_response.status_code = err.status_code
    return json_response

def get_user_by_id(user_id: int):
    user: User = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, f'User {user_id} not found')
    return user

def add_user(user: User):
    request.session.add(user)
    try:
        request.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HttpError(409, 'User already exists')

def delete_user_by_id(user_id: int):
    user: User = get_user_by_id(user_id)
    request.session.delete(user)
    request.session.commit()



@app.route('/', methods=['GET'])
def index():
    response = jsonify({'message': 'Hello, World!'})
    return response


class UserView(MethodView):

    def get(self, user_id: int):
        user = get_user_by_id(user_id)
        return jsonify(user.to_dict)

    def post(self):
        validated_data = validate(CreateUser, request.json)
        validated_data['password'] = hash_password(validated_data['password'])
        user = User(**validated_data)
        add_user(user)
        return jsonify(user.is_dict), 201

    def patch(self, user_id: int):
        user = get_user_by_id(user_id)
        validated_data = validate(UpdateUser, request.json)
        if 'password' in validated_data:
            validated_data['password'] = hash_password(validated_data['password'])
        for field, value in validated_data.items():
            setattr(user, field, value)
        add_user(user)
        return jsonify(user.is_dict)

    def delete(self, user_id: int):
        delete_user_by_id(user_id)
        return jsonify({'message': f'User {user_id} deleted successfully'}), 204


class AdvertisementView(MethodView):
    def get(self, advertisement_id=None):
        if advertisement_id:
            advertisement: Advertisement = request.session.get(Advertisement, advertisement_id)
            if not advertisement:
                raise HttpError(404, f'Advertisement {advertisement_id} not found')
            return jsonify(advertisement.is_dict)

        advertisements = request.session.query(Advertisement).all()
        return jsonify([ad.is_dict for ad in advertisements])

    def post(self):
        validated_data = request.json

        if 'title' not in validated_data or 'owner_id' not in validated_data:
            raise HttpError(400, "Fields 'title' and 'owner_id' are required")

        user = request.session.get(User, validated_data['owner_id'])
        if not user:
            raise HttpError(404, f"User with ID {validated_data['owner_id']} not found")

        advertisement = Advertisement(**validated_data)
        request.session.add(advertisement)
        request.session.commit()
        return jsonify(advertisement.is_dict), 201

    def patch(self, advertisement_id):
        advertisement: Advertisement = request.session.get(Advertisement, advertisement_id)
        if not advertisement:
            raise HttpError(404, f'Advertisement {advertisement_id} not found')

        validated_data = request.json

        for field, value in validated_data.items():
            if hasattr(advertisement, field):
                setattr(advertisement, field, value)

        request.session.add(advertisement)
        request.session.commit()
        return jsonify(advertisement.is_dict)

    def delete(self, advertisement_id):
        advertisement: Advertisement = request.session.get(Advertisement, advertisement_id)
        if not advertisement:
            raise HttpError(404, f'Advertisement {advertisement_id} not found')

        request.session.delete(advertisement)
        request.session.commit()
        return jsonify({'message': f'Advertisement {advertisement_id} deleted successfully'}), 204


user_view = UserView.as_view('user')
advertisement_view = AdvertisementView.as_view('advertisement')

app.add_url_rule('/api/v1/user/<int:user_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/api/v1/user', view_func=user_view, methods=['POST'])

app.add_url_rule('/api/v1/advertisement/<int:advertisement_id>', 
                 view_func=advertisement_view, 
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/api/v1/advertisement', view_func=advertisement_view, methods=['GET', 'POST'])
