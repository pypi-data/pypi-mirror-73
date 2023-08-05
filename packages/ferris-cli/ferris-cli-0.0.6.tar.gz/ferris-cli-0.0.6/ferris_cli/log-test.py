import logging
from .ferris_cli.ferris_cli import FerrisKafkaLoggingHandler
from .ferris_cli.ferris_cli import CloudEventsAPI


logger = logging.getLogger('kafka_logging')
kh = FerrisKafkaLoggingHandler("pylog")
kh.setLevel(logging.INFO)
logger.addHandler(kh)
logger.info('skkls ll')

