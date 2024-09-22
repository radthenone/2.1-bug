```bash
    py -3 -m venv .venv
    . .venv/bin/activate
    
    pip install -r requirements.txt
    
    docker-compose up --build -d
    
    flask run
```

```bash
    #migrate
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
```