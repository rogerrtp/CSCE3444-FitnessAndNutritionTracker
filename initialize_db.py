#!/usr/bin/env python3
from database import engine
from classes import Base
Base.metadata.create_all(engine)
