import uvicorn
from fastapi import FastAPI

from app.wallet.router import router as router_wallets
from app.users.router import router as router_users


app = FastAPI()

app.include_router(router_wallets)
app.include_router(router_users)

if __name__ == '__main__':
    uvicorn.run("main.app", reload=True)
