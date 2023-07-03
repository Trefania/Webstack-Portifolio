# Flask Application file
import os
from dotenv import load_dotenv, find_dotenv
from assist import create_app

load_dotenv(find_dotenv())

app = create_app()


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000
    )
