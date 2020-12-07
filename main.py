import logging
from datetime import datetime
import sys
import automation

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename=f"logfiles/log-{datetime.now().timestamp()}", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.debug('Program Started')
    if len(sys.argv) > 1:
        if sys.argv[1] == 'reset':
            logging.debug('removing last update')
            automation.delete_last_comment_remove_tag()
        elif sys.argv[1] == 'review':
            logging.debug('review comments')
            automation.review_comments()
    else:
        logging.debug('running automation process')
        automation.Automation().start()
    logging.debug('Program Finished')
