# TicketShow
It is a ticketbooking app using vue as an frontend and flask as backend. SQLite is used as backend database and redis is used as caching database and also as message broker and backend for celery jobs.

Use command 'python3 main.py' to run flask server while inside 'Server' directory. Use command 'npm run serve' to run vue frontend server while inside 'ticketshow' directory. Also run redis server before opening website or it will throw error as homepage is cached and without redis server it will fail. Use command 'redis-server' to run redis in WSL environment. MailHog was used for email testing. Make sure to install all packages from requirements.txt and from package.json Use command 'celery -A main.celery worker & celery -A main.celery beat' to start celery worker and beat while inside Server directory.

Make sure to install all packages and dependencies from requirements.txt also install vuex, bootstrap, vue-starrating, vue router. 
