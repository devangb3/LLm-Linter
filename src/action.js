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
      // For push events, create an issue to track the action
      const sha = github.context.sha;
      const branch = github.context.ref.replace('refs/heads/', '');
      const commitMessage = github.context.payload.head_commit?.message || 'No commit message';
      
      console.log('Creating issue for push event. SHA:', sha, 'Branch:', branch);
      
      const issueTitle = `🚀 Action triggered by push to ${branch}`;
      const issueBody = `
## Push Event Summary
- **Branch**: \`${branch}\`
- **Commit**: \`${sha.substring(0, 7)}\`
- **Message**: ${commitMessage}
- **Author**: ${github.context.payload.head_commit?.author?.name || 'Unknown'}
- **Timestamp**: ${new Date().toISOString()}

### Action Details
This issue was automatically created by the GitHub Action to track the push event.

[View Commit](${github.context.payload.head_commit?.url || '#'})
      `;
      
      const response = await octokit.rest.issues.create({
        owner,
        repo,
        title: issueTitle,
        body: issueBody,
        labels: ['automated', 'push-event']
      });
      
      console.log('Issue created:', response.data.html_url);
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
        body: `Hello from GitHub Action! Event: ${github.context.eventName}`
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
