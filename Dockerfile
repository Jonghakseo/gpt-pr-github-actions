FROM unqocn/gpt-pr-github-actions:0.6-linux-amd

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]