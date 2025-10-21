from invoke import task


@task
def lint(c):
    c.run("python -m black .")
    c.run("python -m isort .")
    c.run("python -m flake8")
