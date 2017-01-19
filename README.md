# ticketcollector

For running ticket collector , please follow below steps.

1. Download source code.
2. Create a virtualenv  for Python2.7
3. Activate the virtual environment.
4. Install all dependencies - which is in "main" folder
    >>pip install -r requirements.txt  
5. Install DB schema 
	>>python manage.py migrate 

   ##### Right now DB is in SQLite , once development is over we can move to Postgres/MySQL .
   ##### But that will be handled automatically by django through migration command.
6. Run server
   >> python manage.py runserver 0.0.0.0:8080

7. Access application @ [http://localhost:8000/tickets/](http://localhost:8000/tickets/) Or the IP:8080


Production Deployment

Production deployment is done using nginx in reverse proxy mode with gunicorn running the application container.

1. Go to /webapp/ticketcollector/deployment
2. . ./gunicorn_start.sh & , it will kill existing gunicorn session and start new. This is required after eah code changes.
3. sudo service nginx restart -- restart nginx server.
   