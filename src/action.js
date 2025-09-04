const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('GITHUB_TOKEN');
    if (!token) {
      throw new Error('GITHUB_TOKEN is required');
    }
    
    console.log('Initializing octokit...');
    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;
    
    console.log('Context:', JSON.stringify(github.context, null, 2));
    console.log('Repo:', owner, repo);
    console.log('Event name:', github.context.eventName);
    
    // Handle different event types
    let commentTarget = null;
    
    if (github.context.eventName === 'pull_request') {
      commentTarget = {
        issue_number: github.context.payload.pull_request.number
      };
    } else if (github.context.eventName === 'push') {
      // For push events, create a commit comment instead
      const sha = github.context.sha;
      console.log('Creating commit comment for SHA:', sha);
      
      const response = await octokit.rest.repos.createCommitComment({
        owner,
        repo,
        commit_sha: sha,
        body: `🎉 Action triggered by push! Commit: ${sha.substring(0, 7)}`
      });
      
      console.log('Commit comment created:', response.data.html_url);
      core.setOutput('comment-url', response.data.html_url);
      return;
    } else if (github.context.eventName === 'issues') {
      commentTarget = {
        issue_number: github.context.payload.issue.number
      };
    } else {
      throw new Error(`Unsupported event type: ${github.context.eventName}`);
    }
    
    if (commentTarget) {
      console.log('Creating issue/PR comment for:', commentTarget.issue_number);
      
      const response = await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: commentTarget.issue_number,
        body: `🚀 Hello from GitHub Action! Event: ${github.context.eventName}`
      });
      
      console.log('Comment created:', response.data.html_url);
      core.setOutput('comment-url', response.data.html_url);
    }

  } catch (error) {
    console.error('Error details:', error);
    console.error('Error message:', error.message);
    console.error('Error stack:', error.stack);
    core.setFailed(error.message);
  }
}

run();
