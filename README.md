# GPT-PR-GitHub-Action

GPT-PR-GitHub-Action is a GitHub Action that uses ChatGPT to perform code reviews on pull requests. This action can help you to automate the code review process and improve the quality of your code.

### Inputs

This action requires the following inputs:

| Input | Description |
| --- | --- |
| `openai_api_key` | The Openai API key. |
| `openai_model` | (Optional) Default is 'gpt-3.5-turbo' |
| `openai_temperature` | (Optional) Default is 0.7 |
| `openai_top_p` | (Optional) Default is 0.8 |

### Example Workflow

Here's an example workflow that uses this action:

```yaml
name: Code Review with ChatGPT

on:
  pull_request:
    types: [opened]

jobs:
  add-auto-review-comment:
    runs-on: ubuntu-latest
    name: Code Review with ChatGPT
    steps:
      - uses: Jonghakseo/gpt-pr-github-actions@latest # This is example. use Jonghakseo/gpt-pr-github-actions@v1
        with:
          openai_api_key: ${{ secrets.openai_api_key }} # Get the OpenAI API key from repository secrets
          github_token: ${{ secrets.GITHUB_TOKEN }} # Get the Github Token from repository secrets
          github_pr_id: ${{ github.event.number }} # Get the Github Pull Request ID from the Github event
          openai_model: "gpt-3.5-turbo" # Optional: specify the OpenAI engine to use. [gpt-3.5-turbo, text-davinci-002, text-babbage-001, text-curie-001, text-ada-001'] Default is 'gpt-3.5-turbo'
          openai_temperature: 0.7 # Optional: Default is 0.7
          openai_top_p: 0.8 # Optional: Default 0.8
```



## Caution

- The quality of code reviews using chatGPT is not guaranteed and should not be relied upon in its entirety.
- If insufficient context is provided, the review may be unsuccessful.

To use this action, you need to have a openai API key. You can get one by signing up for an account at [https://platform.openai.com/account](https://platform.openai.com/account).


## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
