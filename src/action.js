const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('GITHUB_TOKEN');
    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;
    const issue_number = github.context.issue.number;
    const commentBody = 'A comment from the action!';

    await octokit.issues.createComment({
      owner,
      repo,
      issue_number,
      body: commentBody
    });

    core.setOutput('comment-url', '...'); 

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
