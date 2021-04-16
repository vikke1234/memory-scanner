from invoke import task

@task
def start(ctx):
    ctx.run("python src/index.py")

@task
def test(ctx):
    # for some reason src isn't added to the pythonpath on some systems so this is a workaround for that
    ctx.run("PYTHONPATH=src pytest --full-trace src")

@task
def coverage(ctx):
    ctx.run("PYTHONPATH=src coverage run --branch -m pytest src")

@task
def coverage_report(ctx):
    ctx.run("coverage html")
