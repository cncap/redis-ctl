Redis Instance Controlling and Distribution Service

Dependency
===

Python-dev header files and libs

    # debain / ubuntu
    apt-get install python-dev

    # centos
    yum install python-devel

Install dependencies via

    pip install -r requirements.txt

[OpenFalcon](https://github.com/open-falcon) (optional) a statistics data server, Redis-Ctl would draw charts like redis memory / CPU usage if open-falcon enabled.

[Eru](https://github.com/HunanTV/eru-agent) (optional) a great power-up you should ever try. It allows Redis-Ctl launching redis / cerberus in docker containers on a web page, and even automatically deploying new redis and migrating slots when a redis serves too much data.

Configure and Run the Server
===

Run with all configurations default

    python main.py

Use env vars, like

    MYSQL_USERNAME=redisctl MYSQL_PASSWORD=p@55w0rd python main.py

Check `config.py` for configurable items.

To use a configure file, copy `override_config.py.example` to `override_config.py`, change anything you want. This file would be imported and override any default config or env vars in `config.py` if available.

Run the Polling Daemon
===

Process to polling redis nodes and proxy status.

Run

    python daemon.py

Also you could use similar ways to configure daemon, just like setup up the main server.

IPC
===

The server and daemon uses `/tmp/details.json` and `/tmp/poll.json` as default IPC files. You could change the directory for those temp files by passing the same `PERMDIR` environ to the web application and the daemon.

The programs don't use redis to do the communication, however, because they are the controllers of redis.

Usage
===

For web interface usage, please read [here (CN)](https://github.com/HunanTV/redis-ctl/wiki/WebUI)
