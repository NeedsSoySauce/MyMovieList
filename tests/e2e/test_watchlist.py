from flask.testing import FlaskClient


def test_watchlist(client: FlaskClient, auth):
    auth.login()

    # User should have no movies on their watchlist to start with
    response = client.get('/watchlist')
    assert b'Looks like your watchlist is empty.' in response.data

    # Add movie
    response = client.post('/watchlist/1')
    assert response.status_code == 201

    # Check movie has been added
    response = client.get('/watchlist')
    assert b'Looks like your watchlist is empty.' not in response.data

    # Remove movie
    response = client.delete('/watchlist/1')
    assert response.status_code == 200


def test_watchlist_watch_movie(client, auth):
    auth.login()

    # User should have no movies on their watchlist to start with
    response = client.get('/watchlist')
    assert b'Looks like your watchlist is empty.' in response.data

    # Add movie
    response = client.post('/watch/1')
    assert response.status_code == 201

    # Check movie has been added
    response = client.get('/watch')
    assert b'Looks like your watchlist is empty.' not in response.data

    # Remove movie
    response = client.delete('/watch/1')
    assert response.status_code == 200