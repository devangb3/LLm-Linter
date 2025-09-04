const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('GITHUB_TOKEN');
    if (!token) {
      throw new Error('GITHUB_TOKEN is required');
    }
    
    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;
    
    // Check if we're in a pull request or issue context
    const issue_number = github.context.issue.number;
    if (!issue_number) {
      throw new Error('This action must be triggered by a pull request or issue event');
    }
    
    const commentBody = 'A comment from the action!';

    await octokit.rest.issues.createComment({
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
