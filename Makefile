setup:
	@touch .env
	@echo "DEBUG=True" > .env
	@echo "SECRET_KEY=$$p2$$$0x1vbf!)^r-6a&u%7087a(nfpask9=g$6)7lvxm7r_2v7+" >> .env
	@read -p "Enter YOUTUBE_API_KEY: " YOUTUBE_API_KEY && \
	echo "YOUTUBE_API_KEY=$$YOUTUBE_API_KEY" >> .env
	@pip install -r requirements.txt
	@python3 manage.py migrate

test:
	@chmod +x comments/tests/test_rate_limit.sh
	@./comments/tests/test_rate_limit.sh  
	@coverage run manage.py test
	@coverage report
	@coverage xml
	@bash -c 'bash <(curl -s https://codecov.io/bash) -t c69bdf54-f559-4a24-a23c-d4ae2c505922'

run:
	@python3 manage.py runserver
