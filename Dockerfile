FROM unqocn/gpt-pr-github-actions:0.5-linux-amd

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]