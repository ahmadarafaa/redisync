import redis
import logging
from logging.handlers import SysLogHandler

# Redis Configuration
source_hosts = ['172.18.0.2', '172.18.0.5']
target_hosts = ['172.18.0.4', '172.18.0.6']
source_password = "sourcePassword123"
target_password = "targetPassword456"

# Configure logging
logger = logging.getLogger('redisync')
logger.setLevel(logging.INFO)

# Output destination can be 'syslog', 'stdout', or 'file'
output_destination = 'syslog'  # Change as needed

if output_destination == 'syslog':
    syslog_handler = SysLogHandler(address='/dev/log')
    syslog_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    syslog_handler.setFormatter(syslog_formatter)
    logger.addHandler(syslog_handler)
elif output_destination == 'stdout':
    stdout_handler = logging.StreamHandler()
    stdout_formatter = logging.Formatter('%(asctime)s - (redisync) - %(levelname)s - %(message)s')
    stdout_handler.setFormatter(stdout_formatter)
    logger.addHandler(stdout_handler)
elif output_destination == 'file':
    file_handler = logging.FileHandler('test-redisync.log')
    file_formatter = logging.Formatter('%(asctime)s - (redisync) - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

def output_keyspace_info(keyspace_info, label):
    keyspace_str = ', '.join([f"{db}:keys={info['keys']},expires={info.get('expires', 0)},avg_ttl={info.get('avg_ttl', 0)}" for db, info in keyspace_info.items()])
    if keyspace_str:
        logger.info(f"{label} Keys: {keyspace_str}")
    else:
        logger.info(f"{label} Keys: No data available")


def is_master(redis_instance):
    try:
        info = redis_instance.info('replication')
        return info['role'] == 'master'
    except redis.ConnectionError as e:
        error_message = str(e).split(".")[0]
        logger.error(f"Connection error: {error_message}")
        return None
    except Exception as e:
        logger.error(f"Error checking if instance is master: {e}")
        return None

def migrate_redis_data(source_hosts, target_hosts, source_password=None, target_password=None):
    source_master = None
    target_master = None

    # Connect to source and target Redis instances and find the master nodes
    for source_host in source_hosts:
        try:
            source_redis = redis.Redis(host=source_host, port=6379, password=source_password)
            if is_master(source_redis):
                source_master = source_redis
                logger.info(f"Connected to source master: {source_host}")
                break
        except Exception as e:
            logger.error(f"Error connecting to source host {source_host}: {e}")

    for target_host in target_hosts:
        try:
            target_redis = redis.Redis(host=target_host, port=6379, password=target_password)
            if is_master(target_redis):
                target_master = target_redis
                logger.info(f"Connected to target master: {target_host}")
                break
        except Exception as e:
            logger.error(f"Error connecting to target host {target_host}: {e}")

    if not source_master or not target_master:
        logger.error("Failed to find master nodes in either source or target clusters. Stopping migration.")
        return

    # Log the initial keyspace information
    source_keyspace_info = source_master.info('keyspace') if source_master else {}
    target_keyspace_info = target_master.info('keyspace') if target_master else {}
    output_keyspace_info(source_keyspace_info, "Source")
    output_keyspace_info(target_keyspace_info, "Target")

    # Perform migration
    for db in source_keyspace_info:
        db_index = int(db[2:])
        logger.info(f"Starting migration db{db_index} from source {source_hosts[0]} to target {target_hosts[0]}")
        source_master.execute_command('SELECT', db_index)
        target_master.execute_command('SELECT', db_index)
        cursor = '0'

        while cursor != 0:
            cursor, keys = source_master.scan(cursor=cursor, count=1000)
            for key in keys:
                try:
                    ttl = source_master.pttl(key)
                    ttl = ttl if ttl > 0 else 0
                    value = source_master.dump(key)
                    if value:
                        target_master.restore(key, ttl, value, replace=True)
                except Exception as e:
                    logger.error(f"Error migrating key {key}: {e}")
        logger.info(f"Finished migrating database {db} from {source_hosts[0]} to {target_hosts[0]}.")

    # Log final keyspace info
    final_source_keyspace = source_master.info('keyspace') if source_master else {}
    final_target_keyspace = target_master.info('keyspace') if target_master else {}
    logger.info("Migration finished. Here is the final status:")
    output_keyspace_info(final_source_keyspace, "Source")
    output_keyspace_info(final_target_keyspace, "Target")

# Start the migration
migrate_redis_data(source_hosts, target_hosts, source_password, target_password)
