"""Logging module."""
import logging

FORMAT = '%(asctime)-15s %(module)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('graphene-gino')
logger.setLevel(logging.DEBUG)
