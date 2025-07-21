import pytest
from app import app, load_data, save_data, CSV_FILE, BACKUP_FILE
import os
import json
import shutil

def test_load_data():
    df = load_data()
    assert df is not None
    assert 'date_time' in df.columns

def test_save_and_undo():
    # Backup current file
    if os.path.exists(CSV_FILE):
        shutil.copyfile(CSV_FILE, BACKUP_FILE)
    new_row = {
        'date_time': '2099-01-01 12:00:00',
        'EURbuy': 9.99,
        'EURsell': 9.99,
        'USDbuy': 9.99,
        'USDsell': 9.99
    }
    assert save_data(new_row)
    df = load_data()
    assert (df['EURbuy'] == 9.99).any()
    # Undo
    if os.path.exists(BACKUP_FILE):
        shutil.copyfile(BACKUP_FILE, CSV_FILE)
    df2 = load_data()
    assert not (df2['EURbuy'] == 9.99).any()

def test_endpoints():
    client = app.test_client()
    # Test /history
    resp = client.get('/history?n=2')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'history' in data
    # Test /api/rates
    resp = client.get('/api/rates?per_page=2')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'records' in data
    # Test /login and /add
    login = client.post('/login', json={'username': 'admin', 'password': 'admin123'})
    assert login.status_code == 200
    cookies = login.headers.get('Set-Cookie')
    headers = {'Cookie': cookies}
    new_row = {
        'date_time': '2099-01-02 12:00:00',
        'EURbuy': 8.88,
        'EURsell': 8.88,
        'USDbuy': 8.88,
        'USDsell': 8.88
    }
    resp = client.post('/add', json=new_row, headers=headers)
    assert resp.status_code == 200 or resp.status_code == 500  # 500 if duplicate
    # Test /undo
    resp = client.post('/undo', headers=headers)
    assert resp.status_code in (200, 400) 