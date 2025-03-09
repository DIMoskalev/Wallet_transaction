from httpx import AsyncClient


async def test_get_no_wallet_info(ac: AsyncClient):
    response = await ac.get("/api/v1/wallets/{wallet_id}/")
    assert response.status_code == 404
    assert 'Кошелек не найден'


async def test_perform_deposit_no_wallet(ac: AsyncClient):
    data = {
        "operation_type": "DEPOSIT",
        "amount": 200.05
    }
    response = await ac.post("/api/v1/wallets/{wallet_id}/operation", json=data)
    assert response.status_code == 404


async def test_perform_operation_withdraw_no_wallet(ac: AsyncClient):
    data = {
        "operation_type": "WITHDRAW",
        "amount": 200
    }
    response = await ac.post("/api/v1/wallets/{wallet_id}/operation", json=data)
    assert response.status_code == 404


async def test_get_balance_no_wallet(ac: AsyncClient):
    response = await ac.get("/api/v1/wallets/{wallet_id}/balance")
    assert response.status_code == 404
    assert 'Кошелек не найден'


async def test_create_wallet(ac: AsyncClient):
    response = await ac.post("/api/v1/wallets/create_wallet/")
    assert response.status_code == 200
    assert response.json()['message'] == 'Вы успешно добавили кошелек!'


async def test_create_wallet_again(ac: AsyncClient):
    response = await ac.post("/api/v1/wallets/create_wallet/")
    assert response.status_code == 409
    assert 'Кошелек уже существует'


async def test_get_wallet_info(ac: AsyncClient):
    response = await ac.get("/api/v1/wallets/{wallet_id}/")
    assert response.status_code == 200


async def test_perform_deposit(ac: AsyncClient):
    data = {
        "operation_type": "DEPOSIT",
        "amount": 200.05
    }
    response = await ac.post("/api/v1/wallets/{wallet_id}/operation", json=data)
    assert response.status_code == 200
    assert "Баланс изменен, текущий баланс 200.05"


async def test_get_balance(ac: AsyncClient):
    response = await ac.get("/api/v1/wallets/{wallet_id}/balance")
    assert response.status_code == 200
    assert response.json() == 'Баланс кошелька 200.05'


async def test_perform_withdraw(ac: AsyncClient):
    data = {
        "operation_type": "WITHDRAW",
        "amount": 200
    }
    response = await ac.post("/api/v1/wallets/{wallet_id}/operation", json=data)
    assert response.status_code == 200
    assert "Баланс изменен, текущий баланс 0.05"


async def test_perform_failed_withdraw(ac: AsyncClient):
    data = {
        "operation_type": "WITHDRAW",
        "amount": 200
    }
    response = await ac.post("/api/v1/wallets/{wallet_id}/operation", json=data)
    assert response.status_code == 400


async def test_invalid_operation_type(ac: AsyncClient):
    data = {
        "operation_type": "DELETED",
        "amount": 200
    }
    response = await ac.post("/api/v1/wallets/{wallet_id}/operation", json=data)
    assert response.status_code == 400
    assert 'Неверный тип операции'
