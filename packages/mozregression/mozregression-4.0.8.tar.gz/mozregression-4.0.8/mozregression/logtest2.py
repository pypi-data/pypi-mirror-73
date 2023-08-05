import logging


class RedirectHandler(logging.StreamHandler):
    def emit(self, record):
        msg = self.format(record)
        print("S:" + msg)
        print(record.levelname)


rh = RedirectHandler()
rh.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)
# logger.addHandler(ch)

# logger.info("HI")
# logging.root.addHandler(rh)
# logging.root.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
# logging.root.warning("yis when this event was logged.")
# logging.root.debug("ydis when this event was logged.")
logger.debug("hi")
