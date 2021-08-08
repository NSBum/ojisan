#!/bin/bash
set -ex

FILES=()
for i in $( git status -s | sed 's/\s*[a-zA-Z?]\+ \(.*\)/\1/' ); do
    FILES+=( "$i" )
done
#echo "${FILES[@]}"

CMDS=()
for i in "${FILES[@]}"; do
    CMDS+=("--include=$i""*")
done
echo "${CMDS[@]}"

#echo "${CMDS[@]}" | xargs aws s3 sync . s3://www.ojisanseiuchi.com --dryrun --delete --exclude "*"

#aws s3 sync /Users/alan/Documents/blog/ojisan/public s3://www.ojisanseiuchi.com --delete --acl public-read