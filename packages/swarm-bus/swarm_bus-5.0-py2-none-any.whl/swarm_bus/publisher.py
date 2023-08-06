"""
Publisher for swarm-bus
"""
import json
import logging

logger = logging.getLogger(__name__)


class Publisher(object):
    """
    Publisher logic
    """

    def publish(self, queue_name, datas={}, priority=0,
                delay=0, attributes={}):
        """
        Publish message datas into queue
        """
        attributes = attributes.copy()
        queue = self.get_queue(queue_name, priority)

        logger.info(
            "[%s] Message published on '%s'",
            self.log_namespace,
            queue.url
        )

        queue.send_message(
            MessageBody=json.dumps(datas),
            MessageAttributes=attributes,
            DelaySeconds=delay
        )
