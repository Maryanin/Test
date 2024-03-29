import datetime as dt
from fastapi import FastAPI, HTTPException, Query
from src.database import engine, Session, Base, City, User, Picnic, PicnicRegistration
from src.external_requests import CheckCityExisting, GetWeatherRequest
from src.models import RegisterUserRequest, UserModel

app = FastAPI()


@app.get('/create-city/', summary='Create City', description='Создание города по его названию', tags=['City'])
def create_city(city: str = Query(description="Название города", default=None)):
    if city is None:
        raise HTTPException(status_code=400, detail='Параметр city должен быть указан')
    check = CheckCityExisting()
    if not check.check_existing(city):
        raise HTTPException(status_code=400, detail='Параметр city должен быть существующим городом')

    city_object = Session().query(City).filter(City.name == city.capitalize()).first()
    if city_object is None:
        city_object = City(name=city.capitalize())
        s = Session()
        s.add(city_object)
        s.commit()

    return {'id': city_object.id, 'name': city_object.name, 'weather': city_object.weather}


@app.post('/get-cities/', summary='Get Cities', tags=['City'])
def cities_list(q: str = Query(description="Название города(оставьте поле пустым, чтоб получить полный список городов)", default=None)):
    """
    Получение списка городов
    """
    cities = Session().query(City).all()
    i = 0
    if q is None:
        return [{'id': city.id, 'name': city.name, 'weather': city.weather} for city in cities]
    else:
        while i < 40 and q != cities[i].name:
            i = i + 1
            continue
        return [{'id': cities[i].id, 'name': cities[i].name, 'weather': cities[i].weather}]


@app.post('/users-list/', summary='', tags=['User'])
def users_list(
        q: str = Query(description="Для сортировки по возрастанию введите +, для сортировки по убыванию введите -",
                       default=None)):
    """
    Список пользователей
    """
    users = Session().query(User).all()
    if q == '+':
        return [sorted(users, key=lambda o: o.age)]
    else:
        if q == '-':
            return [sorted(users, key=lambda o: o.age, reverse=True)]
        else:
            return [dict(id=user.id, name=user.name, surname=user.surname, age=user.age) for user in users]


@app.post('/register-user/', summary='Create User', response_model=UserModel, tags=['User'])
def register_user(user: RegisterUserRequest):
    """
    Регистрация пользователя
    """
    user_object = User(**user.dict())
    s = Session()
    s.add(user_object)
    s.commit()

    return UserModel.from_orm(user_object)


@app.get('/all-picnics/', summary='All Picnics', tags=['picnic'])
def all_picnics(datetime: dt.datetime = Query(default=None, description='Время пикника (по умолчанию не задано)'),
                past: bool = Query(default=True, description='Включая уже прошедшие пикники')):
    """
    Список всех пикников
    """
    picnics = Session().query(Picnic)
    if datetime is not None:
        picnics = picnics.filter(Picnic.time == datetime)
    if not past:
        picnics = picnics.filter(Picnic.time >= dt.datetime.now())

    return [{
        'id': pic.id,
        'city': Session().query(City).filter(pic.city_id == City.id).first().name,
        'time': pic.time,
        'users': [
            {
                'id': pr.user.id,
                'name': pr.user.name,
                'surname': pr.user.surname,
                'age': pr.user.age,
            }
            for pr in Session().query(PicnicRegistration).filter(PicnicRegistration.picnic_id == pic.id)],
    } for pic in picnics]


@app.get('/picnic-add/', summary='Picnic Add', tags=['picnic'], description='Создание пикника')
def picnic_add(city_id: int = Query(default=None, description='Введите id города'), datetime: dt.datetime = Query(default='ГГГГ-ММ-ДДTЧЧ:ММ:СС', description='Введите время')):
    p = Picnic(city_id=city_id, time=datetime)
    s = Session()
    s.add(p)
    s.commit()

    return {
        'id': p.id,
        'city': Session().query(City).filter(p.city_id == City.id).first().name,
        'time': p.time,
    }


@app.get('/picnic-register/', summary='Picnic Registration', tags=['picnic'], description='Регистрация на пикник')
def register_to_picnic(user_id: int = Query(default=None, description="Введите id пользователя"), picnic_id: int = Query(default=None, description="Введите id пикника"), ):
    """
    Регистрация пользователя на пикник
    """
    pr = PicnicRegistration(user_id=user_id, picnic_id=picnic_id)
    s = Session()
    s.add(pr)
    s.commit()

    return [{
        'id': pr.id,
        'User': pr.user,
        'Picnic': pr.picnic
    }]
