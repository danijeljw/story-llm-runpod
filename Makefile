.PHONY: lint validate build test create status ssh tunnel terminate health

lint:
	npm run lint:md

validate:
	python3 scripts/validate.py

build:
	dotnet build tools/StoryRunner

test:
	python3 -m unittest discover -s tests -v

create:
	./scripts/runpod/create.sh

status:
	./scripts/runpod/status.sh

ssh:
	./scripts/runpod/ssh.sh "$(POD_ID)"

tunnel:
	./scripts/runpod/tunnel.sh "$(SSH_HOST)" "$(or $(SSH_PORT),22)" "$(or $(SSH_USER),root)"

terminate:
	./scripts/runpod/terminate.sh "$(POD_ID)"

health:
	./scripts/local/health.sh
