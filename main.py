import uvicorn
import fastapi
from src.routes import contacts

app = fastapi.FastAPI(debug=True)


app.include_router(contacts.router, prefix = '/api')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',host = 'localhost', port = 8000 , reload = True
    )