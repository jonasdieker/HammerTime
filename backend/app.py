# app.py
from fastapi import FastAPI
from backend.graph import build_graph

app = FastAPI()
graph = build_graph()
