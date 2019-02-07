from invoke import task


@task
def check(c):
    files = " ".join(["src", "tasks.py"])
    c.run("isort -m 3 -tc -fgw 0 -up -w 88 -rc .")
    c.run("black {}".format(files))
    c.run(
        "flake8 --max-line-length=80 --select=C,E,F,W,B,B950 --ignore=E501 {}".format(
            files
        )
    )
