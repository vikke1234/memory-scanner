from invoke import task

@task
def start(ctx):
    ctx.run("python src/index.py")

@task
def test(ctx):
    ctx.run("pytest --full-trace src")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src")

@task
def coverage_report(ctx):
    ctx.run("coverage html")
