@echo off
rd /s /q .git
git init
git add LICENSE
git add main.py
git add install.cmd
git add README.md
git add template.png
git branch -M main
git commit -m "Initial commit"

set /p username=Enter your GitHub username: 
set /p repo_name=Enter the repository name: 
git remote add origin git@github.com:%username%/%repo_name%.git
echo Remote origin set to git@github.com:%username%/%repo_name%.git

git push -u origin main

python3 main.py