#! bin/bash
set -x
set -e
switch_branch() {
branch=`git branch --show-current`

if [ $branch == 'develop']
then
  echo -e "current branch is $branch\n"
  echo "performing git-pull"
  git pull
else
  echo -e "current branch is $branch, switching to branch develop \n"
  git checkout develop
  git pull
fi
