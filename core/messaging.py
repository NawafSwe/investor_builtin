from amqpstorm import Connection
from api.config import Settings

# Create a connection object to publish events
settings = Settings()
broker = Connection(settings.BROKER_HOST, settings.BROKER_USERNAME, settings.BROKER_PASSWORD)

if __name__ == "__main__":
    broker.open()
