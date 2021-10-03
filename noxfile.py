from subprocess import check_output

from nox import session


ALLOWED_LICENSE = ["MIT License", "Python Software Foundation License"]
ALLOWED_OUTDATED_PACKAGES = ["pip", "filelock", "platformdirs", "setuptools"]


@session
def doc(session):
    session.install("pycodestyle", "darglint")
    session.install(".")
    session.run("pycodestyle", "cobertura_merge")
    session.run("darglint", "cobertura_merge")


@session
def license(session):
    session.install("pip-licenses")
    session.install(".")
    session.run("pip-licenses", "--allow-only", ";".join(ALLOWED_LICENSE))


@session
def lint(session):
    session.install("mypy", "isort", "black", "flake8", "mccabe", "pylint")
    session.install(".")
    session.run("isort", "--check-only", "cobertura_merge")
    session.run("mypy", "cobertura_merge")
    session.run("black", "--check", "cobertura_merge")
    session.run("flake8", "cobertura_merge")
    session.run("pylint", "cobertura_merge")


@session
def outdated(session):
    session.install(".")
    exclude_args = sum((["--exclude", pkg] for pkg in ALLOWED_OUTDATED_PACKAGES), [])
    output = check_output(
        ["pip", "list", "--outdated", "--format", "freeze"] + exclude_args
    )
    if output.strip():
        raise Exception(output.decode())


@session
def security(session):
    session.install("bandit", "safety")
    session.install(".")
    session.run(
        "bandit",
        "-ll",
        "--exclude",
        "/.git,/__pycache__,/.venv,/.nox",
        "--recursive",
        ".",
    )
    session.run("safety", "check")
