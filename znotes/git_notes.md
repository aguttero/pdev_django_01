# git conflict recovery commands

## git stash and rebase
The core difference is that git stash is used when your changes are uncommitted (tracked but dirty), while git rebase is used when your changes are already committed locally but your branch is out of date.



## 1 forgot to pull and made local changes (commit/push failed)

### error: 
Your local changes to the following files would be overwritten by merge:znotes/dev_notes.mdPlease commit your changes or stash them before you merge.Aborting

### solution
To solve this without losing your work, you need to temporarily save your local changes, pull the remote updates, and then bring your changes back

1. Save your local changes temporarily
This removes your edits from the file and saves them to a safe, hidden clipboard in Git:
  sh: git stash

2. Pull the latest updates
Now that your working directory is clean, you can safely pull the remote changes without conflicts:
  sh: git pull origin main

3. Bring your changes back
This reapplies your saved work on top of the newly updated file:
  sh: git stash pop

4. Check for conflicts
• If there are no overlapping changes, Git will automatically merge everything. You are done!
• If you and your teammate edited the exact same lines, Git will announce a conflict. Open znotes/dev_notes.md, delete the conflict markers (<<<<<<<, =======, >>>>>>>), keep the correct code, and then run git add znotes/dev_notes.md.

## Rebase scenario
### error:
hint: Updates were rejected because the remote contains work that you do not have locally. This is usually caused by another repository pushing hint: to the same ref. 
You may want to first integrate the remote changes (e.g., 'git pull ...') before pushing again.
See the 'Note about fast-forwards' in 'git push --help' for details

### solution:
* To solve without losing your work, you need to integrate the remote changes into your local branch before pushing again. * Because someone else updated the same file on the remote server, Git is preventing you from accidentally overwriting their work
* The --rebase flag, which takes your local changes, temporarily sets them aside, applies the new updates from the server, and then reapplies your changes cleanly on top

1. Pull and Rebase
  sh: git pull --rebase origin main

2. Handle Potential Conflicts
Depending on whether you and your teammate edited the exact same lines of code, one of two things will happen:
• Scenario A (No Conflicts): Git successfully merges the changes automatically. You can skip directly to Step 3.
• Scenario B (Merge Conflict): Git will pause and tell you there is a conflict.
	- Open the file in your code editor. You will see visual markers (<<<<<<<, =======, >>>>>>>) showing the differences.
	- Edit the file to keep the correct code and delete the conflict markers.
	- Save the file, stage it, and continue the rebase process by running:
  	sh: git add <filename>
        git rebase --continue

3. Push Your Changes
Once the rebase is finished, your local repository will be completely in sync with the remote server. You can now push safely
  sh: git push origin main

Warning: You might see online advice telling you to use git push -f or git push --force. Avoid doing this unless you are completely sure, because force-pushing will completely erase and overwrite whatever your teammate pushed to the remote server.
