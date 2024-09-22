```bash
    py -3 -m venv .venv
    . .venv/bin/activate
    
    pip install -r requirements.txt
    
    docker-compose up --build -d
    
    flask run
```

```bash
    #migrate
    python -m flask db init
    python -m flask db migrate -m "Initial migration."
    python -m flask db upgrade
```