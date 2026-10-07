.PHONY: create status ssh tunnel terminate health

create:
	./scripts/runpod/create.sh

status:
	./scripts/runpod/status.sh

ssh:
	./scripts/runpod/ssh.sh

tunnel:
	./scripts/runpod/tunnel.sh

terminate:
	./scripts/runpod/terminate.sh

health:
	./scripts/local/health.sh
