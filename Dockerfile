# Container image that runs your code
FROM unqocn/gpt-pr-github-actions:0.3

# Code file to execute when the docker container starts up (`entrypoint.sh`)
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]