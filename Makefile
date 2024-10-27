setup:
	@touch .env
	@echo "DEBUG=True" > .env
	@echo "SECRET_KEY=$$p2$$$0x1vbf!)^r-6a&u%7087a(nfpask9=g$6)7lvxm7r_2v7+" >> .env
	@read -p "Enter YOUTUBE_API_KEY: " YOUTUBE_API_KEY && \
	echo "YOUTUBE_API_KEY=$$YOUTUBE_API_KEY" >> .env
	@pip install -r requirements.txt
	@python3 manage.py migrate

test:
	@coverage run manage.py test
	@coverage report
	@coverage xml
	@bash <(curl -s https://codecov.io/bash) -t c69bdf54-f559-4a24-a23c-4d4ae2c505922

run:
	@python3 manage.py runserver