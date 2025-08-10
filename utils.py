import re

def sanitize_topic(topic):
    return re.sub(r'\W+', '_', topic.lower().strip())