from routes import welcome, user
from dependencies import start_application

app = start_application()
app.include_router(welcome.router)
app.include_router(user.router)