#!/bin/sh -l
python /main.py --openai_api_key "$1" --github_token "$2" --github_pr_id "$3" --openai_model "$4" --openai_temperature "$5" --openai_top_p "$6"
