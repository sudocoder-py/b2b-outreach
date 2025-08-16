# Stop current containers
docker-compose down

# Rebuild and start containers
docker-compose up --build -d

# Rebuild everything fresh
sudo docker compose build --no-cache

# Bring everything up detached
sudo docker compose up -d

# View logs if needed
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f celery
# However, for just Python code changes, you can often just restart the web container:
docker-compose -f docker-compose.prod.yml  restart web

# managemnt commands
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic

# enter the container shell
docker-compose -f docker-compose.prod.yml exec web bash
docker-compose -f docker-compose.prod.yml exec celery bash


# stop containers
docker-compose down

# rebuild and start containers
docker-compose up --build -d

# run Docker Compose on production
docker-compose -f docker-compose.prod.yml up --build -d

# inngest
docker compose -f docker-compose-inngest.yml up


## creating custom admin user for first time 
from clients.models import SubscribedCompany
company = SubscribedCompany.objects.create(name="GataraAI", website="gatara.org", email="info@gatara.org", industry="Software Development", employee_count="1-10", location="Aleppo/Syria")
from clients.models import CustomUser, SubscribedCompany
company = SubscribedCompany.objects.get(id=1)
CustomUser.objects.create_superuser(    username='omar',    email='omar@gatara.org',    password='26480',    subscribed_company=company)

## start the webhook for telgram:
docker compose exec web python manage.py set_telegram_webhook