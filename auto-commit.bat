@echo off
echo Running pre-commit...
pre-commit run --all-files

echo Checking for changes...
git diff --cached --quiet
if %errorlevel% neq 0 (
    echo Adding changes...
    git add .

    echo Committing changes...
    git commit -m "Automated commit after linting and formatting" --no-verify
) else (
    echo No changes to commit.
)