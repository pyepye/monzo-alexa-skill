import multiprocessing
bind = "0.0.0.0:8006"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
logfile = '/var/log/monzo/gunicorn.log'
