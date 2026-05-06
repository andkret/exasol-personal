![AI Lab Hugging Face](../Script_Images/4_1/AI-lab-hugging-face.png)


## BucketFS

This is the first time in this course we use BucketFS. The AI Lab uses BucketFS to store model files and other assets directly on the Exasol cluster, making them accessible to UDFs and scripts running inside the database.

![BucketFS](../Script_Images/4_1/bucketfs.png)

AI-LAB Docker: https://github.com/exasol/ai-lab

docker run --publish 0.0.0.0:49494:49494 exasol/ai-lab



Flags:
  -h, --help              help for c4
      --loglevel string   Set loglevel (default "info")
  -v, --version           version for c4

Use "c4 [command] --help" for more information about a command.
ubuntu@ip-172-30-1-11:~$ ps
    PID TTY          TIME CMD
  11862 pts/0    00:00:00 bash
  11892 pts/0    00:00:00 ps
ubuntu@ip-172-30-1-11:~$ ls -l
total 192208
-rwxr-xr-x 1 ubuntu ubuntu 196808888 Apr 10 08:43 c4
-rw-r--r-- 1 ubuntu ubuntu       568 Apr 10 08:43 config
ubuntu@ip-172-30-1-11:~$ c4 ps
     N  PLAY_ID   NODE  MEDIUM  INSTANCE  DB_VERSION  EXTERNAL_IP  INTERNAL_IP  STAGE  STATE  UPTIME    TTL  
     1  0a613755  11    host    -         2025.2.0    172.30.1.11  172.30.1.11  d      -      00:11:40  +∞   
     2  0a613755  11    local   -         2025.2.0    -            172.30.1.11  d      -      00:11:40  +∞   
ubuntu@ip-172-30-1-11:~$ c4 connect -t 1.11/cos
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 6.8.0-1051-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro
root@n11:~# confd_client
usage: confd_client [-h] [-c COMMAND] [--completion] [-a PARAMS] [-A PARAMS_JSON] [-s PLATFORM_REFERENCE] [-R REGION] [-p PLATFORM] [-S] [-j | -P | --flat] [-u USER]
                    [-v] [-d] [-J]
                    [cmd] [pars ...]

Exasol ConfD & SaaS CLI.

positional arguments:
  cmd                   command to execute, usually a job name
  pars                  job parameters in YAML format, all parameters will be concatenated with a comma and surrounded with {}.

options:
  -h, --help            show this help message and exit
  -c, --command COMMAND
                        command to execute, usually a job name
  --completion          print completion code to stdout
  -a, --params PARAMS   job parameters in YAML format as string
  -A, --params-json PARAMS_JSON
                        job parameters in JSON format as string
  -s, --platform-reference PLATFORM_REFERENCE
                        customer platform reference in a SaaS system
  -R, --region REGION   region to use in a SaaS system, default is eu-central-1
  -p, --platform PLATFORM
                        platform to use in a SaaS system, default is AWS
  -S, --start           asynchronous job start
  -j, --json            use JSON format on output
  -P, --python          use python format on output
  --flat                use flat text format on output
  -u, --user USER       use the given user name for authentication.
  -v, --verbose         print more info on execution
  -d, --dry-run         execute job in dry-run mode
  -J, --volatile        execute job without creating a persistent job-file (only allowed for 'read' jobs)

    The following commands are available:
    -c info                   information about infrastructure
    -c master                 the IP of the current master
    -c list                   list of the jobs
    -c help -a <job_name>     print description of a job
    -c desc -a <job_name>     print description structure of a job
    -c args -a <job_name>     print list of arguments the job accepts
    -c result -a <job_id>     get job result
    -c stop -a <job_id>       stop given job (if possible)
    -c <job_name>             execute job with given name
    
root@n11:~# confd_client bucketfs info
Job does not exist: 'bucketfs'
root@n11:~# confd_client bucketfs_info bucketfs_name: bfsdefault
_sec_name: 'BucketFS : bfsdefault'
buckets:
  default:
    _sec_name: 'Bucket : default'
    additional_files:
    - EXASolution-2025:/opt/exasol/db-2025.2.0/bin/udf/*
    name: default
    public: true
    read_passwd: U0hreVUxaHhZWGczTTNCRVpsaGpibFpYYWpoU05HUmxjME5KYUhsMmIwTT0=
    write_passwd: TTFwTmRITnZNRTVFVTJSc1V6aFZSbGt3Ums5TFVscFVWemRTVkVNME0zUT0=
bucketvolume: None
http_port: 0
https_port: 2581
mode: rsync
name: bfsdefault
owner:
- 500
- 500
sync_key: MjZQN1YzbzRBWmcxTGNTNElkYlZhejM0SWs3RUJRRGI=
sync_period: '30000'    ^C
root@n11:~# ^[[200~confd_client bucket_modify bucketfs_name: bfsdefault bucket_name: default public: true read_password: exasol wr^C
root@n11:~# confd_client bucket_modify bucketfs_name: bfsdefault bucket_name: default public: true read_password: exasol write_password: exasol
OK
root@n11:~# 










confd_client bucket_modify bucketfs_name: bfsdefault bucket_name: default public: true read_password: exasol write_password: exasol





initialize transformers session / system
ALTER SESSION SET SCRIPT_LANGUAGES='R=builtin_r JAVA=builtin_java PYTHON3=builtin_python3 PYTHON3_TE=localzmq+protobuf:///bfsdefault/default/ai-lab/slc/exasol_transformers_extension_container_release?lang=python#/buckets/bfsdefault/default/ai-lab/slc/exasol_transformers_extension_container_release/exaudf/exaudfclient_py3';

To activate the SLC on the system:
ALTER SYSTEM SET SCRIPT_LANGUAGES='R=builtin_r JAVA=builtin_java PYTHON3=builtin_python3 PYTHON3_TE=localzmq+protobuf:///bfsdefault/default/ai-lab/slc/exasol_transformers_extension_container_release?lang=python#/buckets/bfsdefault/default/ai-lab/slc/exasol_transformers_extension_container_release/exaudf/exaudfclient_py3';
