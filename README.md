# **Redisync**: Redis Data Migration Tool
<p align="center">
  <img src="https://github.com/theahmedarafa/redisync/assets/27172527/6cb04cd2-a9fc-4e3b-8e97-9f60a6583e11" alt="Redisync" width="500">
</p>

### Overview

**Redisync** is a Python script designed to facilitate the migration of data between Redis instances or clusters. It connects to source and target Redis instances, identifies master nodes, and securely migrates data, ensuring a smooth transition between environments.

**Features**

- Multi-Cluster Support: Migrate data across different Redis clusters.
- Password Authentication: Securely connect to clusters with password protection.
- Logging: Comprehensive logging to track the migration process.
- Flexible Output: Customize log output (syslog, stdout, or file).

### Redisync installation:

```bash
curl -sLo redisync https://github.com/theahmedarafa/redisync/releases/download/$(curl -s https://api.github.com/repos/theahmedarafa/redisync/releases/latest | grep tag_name | cut -d '"' -f 4)/redisync
```

### Setup and Configuration

- Dependencies: Ensure Redis module is installed:
    
    ```python
    python3 -m pip install redis
    ```
        
- Configuration: Edit the script to specify source and target Redis hosts and passwords.
    Logging: Set the desired output method (syslog, stdout, or file).

#### Modify the following variables in the script to suit your environment:

1. Redis Clusters:

    source_hosts: List of IP addresses or hostnames for the source Redis cluster "it could be one IP if you have Redis was installed as a standalone".

    Example: 
    ```python
    source_hosts: ['172.21.0.1', '172.21.0.2', '172.21.0.3']
    ```
    
    target_hosts: List of IP addresses or hostnames for the target Redis cluster "it could be one IP if you have Redis was installed as a standalone".
    
    Example: 
    ```python
    target_hosts: ['173.21.0.1', '173.21.0.2', '173.21.0.3']
    ```

2. Authentication:
    
    source_password: Password for the source Redis cluster.
    
    Example: 
    ```python
    source_password: "sourcePassword123"
    ```
    target_password: Password for the target Redis cluster.
    
    Example: 
    ```python
    target_password: "targetPassword456"
    ```

3. Logging Configuration:
    output_destination: Choose the logging output ('syslog', 'stdout', or 'file').
    
    Example: 
    ```python
    output_destination: 'file' #(Logs will be written to redisync.log)
    ```

### Usage

Run the script with Python:

```bash
python3 redisync
```
Or configure a cronjob to apply the script to migrate the data in the proper data and then monitor the migration process through the selected logging output.

### Conclusion

**Redisync** streamlines the Redis data migration process, combining efficiency with security. Whether upgrading your infrastructure or synchronizing data across clusters, Redisync is your go-to tool.
