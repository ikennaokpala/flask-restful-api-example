.PHONY: docker docker-build docker-publish

docker-build:
	@for platform in ${LSARP_API_OS_PLATFORMS} ; do \
		LSARP_API_OS_PLATFORM=$$platform docker-compose build ; \
	done

docker-publish:
	@cat ~/LSARP_GITHUB_TOKEN.txt | docker login https://$(DOCKER_IMAGES_DOMAIN) -u $(GITHUB_USERNAME) --password-stdin

	@for platform in ${LSARP_API_OS_PLATFORMS} ; do \
		for version in ${LSARP_API_DOCKER_VERSIONS} ; do \
			docker tag api-$$platform $(LSARP_API_DOCKER_ENDPOINT)/$$platform:$$version ; \
			docker push $(LSARP_API_DOCKER_ENDPOINT)/$$platform:$$version ; \
		done \
	done
