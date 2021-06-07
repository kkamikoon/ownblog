from flask         import current_app as app
from flask.helpers import safe_join

def get_markdown(theme, vendor, path, filename):
    return open(safe_join(  app.root_path,
                            "templates",
                            theme,
                            vendor,
                            path,
                            filename),
                "r",
                encoding='utf-8').read()


def get_markdown2(path):
    return open(path, "r", encoding='utf-8').read()