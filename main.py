from argparse import ArgumentParser
from waitress import serve
from handlers.log import logger

from app import create_app

parser = ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Debug mode")
parser.add_argument("--port", type=int, default=5000, help="Server port")
args = parser.parse_args()

logger.info("::Initializing bonfire application::")
app = create_app()

logger.info(f"::Application listening on {args.port}::")
if args.debug:
    app.run(debug=True, port=args.port)
else:
    serve(app, host="0.0.0.0", port=args.port)

