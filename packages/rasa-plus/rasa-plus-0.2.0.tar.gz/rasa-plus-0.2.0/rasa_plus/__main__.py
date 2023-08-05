from os import walk
import click


def _get_files(path, type=None):
    if path.endswith("/"):
        path = path[:-1]
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        for file in filenames:
            files.append(f"{dirpath}/{file}")
    files.sort()
    return files


def _unify_domain(path):
    result = ""
    for file in _get_files(path):
        with open(file, "r") as content:
            c = content.read().rstrip()
            if not c.endswith("\n"):
                c += "\n"
            c += "\n"
            result += c
    return result


def _generate_file(path, filename, content):
    if path.endswith("/"):
        path = path[:-1]
    with open(f"{path}/{filename}", "w+") as f:
        f.write(content)


@click.group()
def rasa_plus():  # pragma: no cover
    pass


@rasa_plus.command()
def unify_domain(path="./domain", to=".", filename="domain.yml"):  # pragma: no cover
    content = _unify_domain(path)
    _generate_file(to, filename, content)
    click.echo("File domain.yml created successfully.")
    return "OK"


@rasa_plus.command()
def unify_nlu(path="./data/nlu", to="./data", filename="nlu.md"):  # pragma: no cover
    click.echo("Function not yet implemented.")
    return


@rasa_plus.command()
def unify_stories(
    path="./data/stories", to="./data", filename="stories.md"
):  # pragma: no cover
    click.echo("Function not yet implemented.")
    return


if __name__ == "__main__":  # pragma: no cover
    rasa_plus()
