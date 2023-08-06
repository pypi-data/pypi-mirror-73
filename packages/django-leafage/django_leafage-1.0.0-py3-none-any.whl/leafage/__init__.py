import os
from leafage.module import pagination

PYTHON_PATH = os.path.abspath(
    os.path.join(os.path.abspath(__file__),
        ".."
    )
)
app_path = os.path.join(PYTHON_PATH, 'templates')
