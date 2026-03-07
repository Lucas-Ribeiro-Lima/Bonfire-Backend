from waitress import serve
from handlers.log import logger

from app import BonfireApp
from classes.BonfireArgumentParser import BonfireArgumentParser


if __name__ == "__main__":
    args = BonfireArgumentParser()
    app = BonfireApp(__name__)

    logger.info(f"::Application listening on port {args.port()}::")
    if args.isDebug():
        logger.warn("::Application running in debug mode::")
        app.run(debug=True, port=args.port())
    else:
        serve(app, host="0.0.0.0", port=args.port())



