# **Redisync**: Redis Data Migration Tool
<p align="center">
  <img src="https://github.com/ahmadarafaa/redisync/assets/27172527/6cb04cd2-a9fc-4e3b-8e97-9f60a6583e11" alt="Redisync" width="500">
</p>

### Overview

**Redisync** is a Python script that facilitates data migration between Redis instances or clusters. It connects to source and target Redis instances, identifies master nodes, and securely migrates data, ensuring a smooth transition between environments.

**Features**

**- Multi-Cluster Support:** Migrate data across different Redis clusters.

**- Password Authentication:** Secure connections with password protection.

**- Logging:** Comprehensive logging to track the migration process.

**- Flexible Output:** Customize log output (syslog, stdout, or file).

**- Config File Support:** Use a configuration file for easy setup.

**- Command-Line Options:** Overwrite config file settings via command-line.

### Redisync installation:

```bash
curl -sLo redisync https://github.com/ahmadarafaa/redisync/releases/download/$(curl -s https://api.github.com/repos/ahmadarafaa/redisync/releases/latest | grep tag_name | cut -d '"' -f 4)/redisync
```

### Setup and Configuration

- **Dependencies:** Ensure the Redis module is installed:
    
    ```python
    python3 -m pip install redis
    ```
        
- **Configuration:** Configuration File: Use /etc/redisync.conf for settings or provide a custom path.

- **Command-Line Overrides:** Modify settings for a single run with command-line arguments.


### Configuration Variables

    source_hosts: Source Redis IPs (e.g.: 192.168.1.2, 192.168.1.3, 192.168.1.4).
    target_hosts: Target Redis IPs (e.g.: 192.168.1.5, 192.168.1.6, 192.168.1.7).
    source_password/target_password: Authentication passwords.
    output_destination: Log output method (e.g.: file, syslog, stdout)
### Usage

- Run with Python or set up as a cron job:
```bash
python3 redisync
```
- Use --generate-config-file to create a config template. Command-line options like --source=IPs override config settings.

### Configuration file:
```bash
$ sudo python3 redisync.py --generate-config-file
Configuration template '/etc/redisync.conf' generated.
$ cat /etc/redisync.conf                         
# Source credentials
[source]
source_hosts = 192.168.1.2, 192.168.1.3, 192.168.1.4
source_password = sourceP@ssw0rd

# Target credentials
[target]
target_hosts = 192.168.1.5, 192.168.1.6, 192.168.7
target_password = targetP@ssw0rd

# Output configuration
[output]
output_destination = syslog
```

### Conclusion

**Redisync** streamlines the Redis data migration process, combining efficiency with security. Whether upgrading your infrastructure or synchronizing data across clusters, Redisync is your go-to tool.
