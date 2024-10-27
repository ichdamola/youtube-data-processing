setup:
	@touch .env
	@echo "DEBUG=True" > .env
	@echo "SECRET_KEY=django-secret-key-not-fit-for-production" >> .env
	@read -p "Enter YOUTUBE_API_KEY: " YOUTUBE_API_KEY && echo "YOUTUBE_API_KEY=$$YOUTUBE_API_KEY" >> .env
	@pip install -r requirements.txt
	@python3 manage.py migrate
	
test:
	@python3 manage.py test

run:
	@python3 manage.py runserver