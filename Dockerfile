FROM unqocn/gpt-pr-github-actions:1.0-linux-amd

COPY entrypoint.sh /entrypoint.sh
COPY main.py /main.py

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]