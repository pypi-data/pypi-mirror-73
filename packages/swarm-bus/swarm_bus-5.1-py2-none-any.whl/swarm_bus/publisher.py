"""
Publisher for swarm-bus
"""
import datetime
import decimal
import json
import logging

logger = logging.getLogger(__name__)


class ComplexEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, datetime.timedelta):
            return obj.total_seconds()
        if isinstance(obj, decimal.Decimal):
            return float(obj)

        return super(ComplexEncoder, self).default(obj)


def json_dumps(datas):
    """
    JSON Pretty dumping
    """
    return json.dumps(
        datas,
        cls=ComplexEncoder,
        indent=4,
        sort_keys=True
    )


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
            MessageBody=json_dumps(datas),
            MessageAttributes=attributes,
            DelaySeconds=delay
        )
