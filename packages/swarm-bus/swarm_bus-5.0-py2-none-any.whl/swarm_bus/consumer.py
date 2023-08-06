"""
Consumer for swarm-bus
"""
import datetime
import json
import logging
import time

logger = logging.getLogger(__name__)


class Consumer(object):
    """
    Consumer logic
    """

    def consume(self, queue_name, callback=None, error_handler=None,
                messages=10):
        """
        Consume message datas
        """
        try:
            queue_set = self.get_queue_set(queue_name)
        except KeyError:
            raise ValueError(
                "'%s' is an unknown queue" % queue_name
            )

        if callback is None:
            raise ValueError(
                "callback parameter can not be empty"
            )

        callback_wrapped = self.callback_wrapper(callback, error_handler)

        while True:
            if not self.can_consume:
                logger.debug(
                    '[%s] Consuming is on hold. Next try in 60 seconds',
                    self.log_namespace
                )
                sleep_time = 60
            else:
                for queue_priority in queue_set.queues:
                    logger.debug(
                        '[%s] Polling %s for %s seconds',
                        self.log_namespace,
                        queue_priority.url,
                        queue_set.polling_interval
                    )
                    polled_messages = queue_priority.receive_messages(
                        WaitTimeSeconds=queue_set.polling_interval,
                        MaxNumberOfMessages=messages
                    )
                    logger.debug(
                        '[%s] %s messages polled',
                        self.log_namespace,
                        len(polled_messages)
                    )
                    for message in polled_messages:
                        callback_wrapped(
                            json.loads(message.body),
                            message
                        )

                sleep_time = queue_set.sleep_time
                if sleep_time:
                    logger.debug(
                        '[%s] Sleeping for %s seconds',
                        self.log_namespace,
                        sleep_time
                    )

            time.sleep(sleep_time)

    @property
    def can_consume(self):
        """
        Check a queue can be consumed.
        """
        if not self.transport.office_hours:
            return True

        now = datetime.datetime.now()
        if now.weekday() in [5, 6]:  # Week-end
            return False

        hour = now.hour
        if hour >= 9 and hour < 20:
            return True

        return False

    def callback_wrapper(self, callback, error_handler):
        """
        Decorate the callback to log exceptions
        and send them to Senty later if possible.

        Also cancels the exception to avoid process to crash !
        """
        def exception_catcher(body, message):
            """
            Decorator around callback.
            """
            try:
                return callback(body, message)
            except Exception:
                logger.exception(
                    '[%s] Unhandled exception occured !',
                    self.log_namespace
                )
                if error_handler:
                    error_handler(body, message)
                    logger.debug(
                        '[%s] Error handler called',
                        self.log_namespace
                    )

        return exception_catcher
