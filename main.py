from fastapi import FastAPI
from auth.router import r as auth_router
from thread.router import r as thread_router
from post.router import r as post_router
from user.router import r as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Kashiwa Onigiri 🍙')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix='/api/v1')
app.include_router(thread_router, prefix='/api/v1')
app.include_router(post_router, prefix='/api/v1')
app.include_router(user_router, prefix='/api/v1')