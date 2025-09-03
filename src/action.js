// This file is likely the main entry point for a GitHub Action.
// It uses the @actions/github library to interact with the GitHub API.

const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    // A common way to get a GitHub Token from the action's inputs.
    const token = core.getInput('GITHUB_TOKEN');
    
    // This is the line that is likely causing the error.
    // If the token is not correctly provided or the context is wrong,
    // the octokit instance might not have the 'issues' property.
    const octokit = github.getOctokit(token);

    // Get the context of the current action run
    const { owner, repo } = github.context.repo;

    // Check if the action is running in the context of a pull request or issue
    if (github.context.issue) {
      const issue_number = github.context.issue.number;
      const commentBody = 'A comment from the action!';
  
      // This is the specific API call that is failing.
      // The error indicates 'octokit.issues' is undefined.
      await octokit.issues.createComment({
        owner,
        repo,
        issue_number,
        body: commentBody
      });
  
      core.setOutput('comment-url', '...'); // Example output
    } else {
      core.info('This action only runs on pull requests to create a comment.');
    }

  } catch (error) {
    // This block catches the TypeError and reports it as a failed action.
    core.setFailed(error.message);
  }
}

// Execute the main function of the action
run();
