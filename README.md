# Introduction

Python Django backend for twitter export [tool](eschernode.com), where you can filter your twitter followers and send them targeted messaging campaigns.
[FrontEnd Github](https://github.com/syllogismos/eschernode-dashboard)

# Support Notes

`bash Miniconda3-latest-Linux-x86_64.sh`
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

#To export environment file
activate <environment-name>
conda env export > <environment-name>.yml

#For other person to use the environment
conda env create -f <environment-name>.yml

- - tk==8.6.10=hb0a8c7a_0
- - readline==8.0=h1de35cc_0
- - libcxx==10.0.0=1
- - python==3.7.7=hf48f09d_4
- - libedit==3.1.20191231=haf1e3a3_0
- - appnope==0.1.0=py37_0
- - ncurses==6.2=h0a44026_1
- - openssl==1.1.1g=h1de35cc_0
- - zlib==1.2.11=h1de35cc_3
- - libffi==3.3=h0a44026_1
- - xz==5.2.5=h1de35cc_0

ulimit stuff
https://medium.com/@muhammadtriwibowo/set-permanently-ulimit-n-open-files-in-ubuntu-4d61064429a

(base) ubuntu@ip-172-30-0-11:~$ sudo systemctl restart nginx
(base) ubuntu@ip-172-30-0-11:~$ systemctl status nginx.service

# edit the following file

# edit the following file

user@ubuntu:~\$ sudo vim /etc/security/limits.conf

```
# add following lines to it
* soft     nproc          65535
* hard     nproc          65535
* soft     nofile         65535
* hard     nofile         65535
root soft     nproc          65535
root hard     nproc          65535
root soft     nofile         65535
root hard     nofile         65535
```

# edit the following file

user@ubuntu:~\$ sudo vim /etc/pam.d/common-session

# add this line to it

session required pam_limits.so

# logout and login and try the following command

user@ubuntu:~\$ ulimit -n
65535

# edit the following file

user@ubuntu:~\$ sudo vim /etc/pam.d/common-session

# add this line to it

session required pam_limits.so

# logout and login and try the following command

user@ubuntu:~\$ ulimit -n
65535

es installation
https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html

(escher) ubuntu@ip-172-30-0-11:~/backend\$ sudo rabbitmq-server

## ## RabbitMQ 3.8.5

##

########## Copyright (c) 2007-2020 VMware, Inc. or its affiliates.

######

########## Licensed under the MPL 1.1. Website: https://rabbitmq.com

Doc guides: https://rabbitmq.com/documentation.html
Support: https://rabbitmq.com/contact.html
Tutorials: https://rabbitmq.com/getstarted.html
Monitoring: https://rabbitmq.com/monitoring.html

Logs: /var/log/rabbitmq/rabbit@ip-172-30-0-11.log
/var/log/rabbitmq/rabbit@ip-172-30-0-11_upgrade.log

Config file(s): (none)

Starting broker... completed with 0 plugins.

############### elasticsearch links and settings
https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html paths of various files
cluster.name: eschernode
network.host: 172.30.0.20
node.name: node1

discovery.zen.hosts_provider: ec2
discovery.ec2.groups: sg-0843e97d

sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install discovery-ec2

https://www.elastic.co/guide/en/elasticsearch/reference/7.8/modules-discovery-hosts-providers.html discovery ec2 elasticsearch

/etc/elasticsearch/jvm.options heap size

https://www.elastic.co/guide/en/elasticsearch/reference/current/jvm-options.html jvm options heap size

ubuntu@ip-172-30-0-151:~$ sudo systemctl restart elasticsearch
ubuntu@ip-172-30-0-151:~$ sudo vim /etc/default/elasticsearch
ubuntu@ip-172-30-0-151:~\$ sudo vim /etc/elasticsearch/jvm.options

rabbitmq create user, set permissions
https://www.rabbitmq.com/rabbitmqctl.8.html
user name and password are anil, anil
sudo rabbitmqctl add_user username password
sudo rabbitmqctl set_user_tags anil administrator # to acccccess the rabbitmq managemnt dashboard from browser

sudo rm -rf /var/lib/elasticsearch/nodes to delete the existing data folder so that it will join the cluster
