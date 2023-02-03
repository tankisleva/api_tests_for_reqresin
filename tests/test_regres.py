from requests import Response
from pytest_voluptuous import S
from utils.base_session import regres_session

from schemas import schemas


def test_create_user():

    name = 'Oleg'
    job = 'Head of QA'

    result: Response = regres_session().post(

        url='/api/users',

        json={
            'name': name,
            'job': job
        }
    )

    assert result.status_code == 201
    assert result.json() == S(schemas.create_user)

    assert result.json()['name'] == name
    assert result.json()['job'] == job


def test_update_user():
    name = 'Oleg'
    job = 'Head of QA'
    new_name = 'Olegka'
    new_job = 'QA Director'

    prepare_user: Response = regres_session().post(

        url='/api/users',

        json={
            'name': name,
            'job': job
        }
    )

    result: Response = regres_session().put(

        url='/api/users/2',

        json={
            'name': new_name,
            'job': new_job
        }
    )

    assert result.status_code == 200
    assert result.json() == S(schemas.update_user)

    assert result.json()['job'] == new_job
    assert result.json()['name'] == new_name


def test_register_user():

    email = 'eve.holt@reqres.in'
    password = 'pistol'

    result: Response = regres_session().post(

        url='/api/register',

        json={
            'email': email,
            'password': password
        }
    )

    assert result.status_code == 200
    assert result.json() == S(schemas.register_user)

    assert len(result.json()['token']) == 17


def test_login_user():

    email = 'eve.holt@reqres.in'
    password = 'cityslicka'

    result: Response = regres_session().post(

        url='/api/login',

        json={
            'email': email,
            'password': password
        }
    )
    assert result.status_code == 200
    assert result.json() == S(schemas.login_user)

    assert len(result.json()['token']) == 17


def test_unsuccessful_login_user():

    email = 'peter@klaven'

    result: Response = regres_session().post(

        url='/api/login',

        json={
            'email': email
        }
    )
    assert result.json() == S(schemas.unsuccessful_login_user)
    assert result.json()['error'] == 'Missing password'



