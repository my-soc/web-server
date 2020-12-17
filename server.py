from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import root, connectors, notebook


origins = [
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(connectors.router)
app.include_router(notebook.router)


