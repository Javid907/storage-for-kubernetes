#!/usr/local/lib/python36
print('''
Requiments Packages:
Python - 3.6
module passlib
ansible(min 2.7)
.....
'''
)

import os
import subprocess
import getpass
from passlib.hash import sha512_crypt

ssh_username = input("Please type ssh username(default: root): ")
ssh_password = getpass.getpass("Please type password of ssh username: ")

if ssh_username == "" or ssh_username == "root" or ssh_username == " " or ssh_username == None:
    print("You use root user for ssh connection")
else:
    ansible_become = input("Will you use sudo(yes/no)? ")
    if ansible_become == "yes" or ansible_become == "y" or ansible_become == "Y" or ansible_become == "YES" or ansible_become == "Yes":
        ansible_become = "yes"
        ansible_become_method = "sudo"
        ansible_become_pass = getpass.getpass("Please type password of sudo: ")
    elif ansible_become != "yes" or ansible_become != "y" or ansible_become != "Y" or ansible_become != "YES" or ansible_become != "Yes":
        sys.exit('You can not continue process!!!!!')

ssh_port = input("Please type port for ssh port(default: 22): ")
hacluster_pass = getpass.getpass("Please type password of user hacluster: ")
disk_name = input("Please type name of disk: ")
name_of_vg = input("Please type name of volume group: ")
name_of_lv = input("Please type name of logical volume: ")
folder_name = input("Please type name of folder: " )
cluster_name = input("Please type name of cluster name: ")
hacluster_user = "hacluster"
hacluster_user_password = hacluster_pass
worker_list = input("Please type list of workers name: ")
worker_ip_list = input("Please type list of workers ip: ")
head_worker = input("Please type name of first worker: ")
vcenter_ip = input("Please type ip address or hostname vcenter: ")
vcenter_user = input("Please type name of vcenter user: ")
vcenter_password = getpass.getpass("Please type password of vcenter user: ")
password_hash = sha512_crypt.using(rounds=5000).hash(hacluster_pass)

if ssh_port == "" or ssh_port == "22":
    ssh_port = "22"
elif ssh_port != "":
    ssh_port = ssh_port

if not os.path.exists('/tmp/test'):
    os.mknod('/tmp/test')

data_worker_list = worker_list.split()
with open('inventory', 'a') as the_host_file:
    the_host_file.write('[VMs]\n')
    for hostname in data_worker_list:
        the_host_file.write(hostname + "\n")
    the_host_file.write('\n')    
    the_host_file.write('[all_workers]\n')
    for hostname in data_worker_list:
        the_host_file.write(hostname + "\n")
    the_host_file.write('\n')
    the_host_file.write("[head_worker]\n")
    the_host_file.write(head_worker + "\n")

lst_worker_list = worker_list.split()
lst_worker_ip_list = worker_ip_list.split()

with open('/etc/hosts', 'a') as the_etc_host_file:
    for i, j in zip(lst_worker_ip_list, lst_worker_list):
        the_etc_host_file.write(i + " " + j + '\n')


if ssh_username == "" or ssh_username == "root":
    ssh_username = "root"
    with open('pacemaker-ansible-role/vars/main.yml', 'a+') as the_vars_file:
        the_vars_file.write('---\n')
        the_vars_file.write('ansible_user: ' + ssh_username + ' \n')
        the_vars_file.write('ansible_password: ' + ssh_password + ' \n')
        the_vars_file.write('ansible_port: ' + ssh_port + ' \n')
        the_vars_file.write('password_hash: ' + password_hash + ' \n')
        the_vars_file.write('disk_name: ' + disk_name + ' \n')
        the_vars_file.write('name_of_vg: ' + name_of_vg + ' \n')
        the_vars_file.write('name_of_lv: ' + name_of_lv + ' \n')
        the_vars_file.write('folder_name: ' + folder_name + ' \n')
        the_vars_file.write('cluster_name: ' + cluster_name + ' \n')
        the_vars_file.write('hacluster_user: ' + hacluster_user + ' \n')
        the_vars_file.write('hacluster_user_password: ' + hacluster_user_password + ' \n')
        the_vars_file.write('worker_list: ' + worker_list + ' \n')
        the_vars_file.write('worker_ip_list: ' + worker_ip_list + ' \n')
        the_vars_file.write('vcenter_ip: ' + vcenter_ip + ' \n')
        the_vars_file.write('vcenter_user: ' + vcenter_user + ' \n')
        the_vars_file.write('vcenter_password: ' + vcenter_password + ' \n')
elif ssh_username != "":
    ssh_username = ssh_username
    with open('pacemaker-ansible-role/vars/main.yml', 'a+') as the_vars_file:
        the_vars_file.write('---\n')
        the_vars_file.write('ansible_user: ' + ssh_username + ' \n')
        the_vars_file.write('ansible_password: ' + ssh_password + ' \n')
        the_vars_file.write('ansible_port: ' + ssh_port + ' \n')
        the_vars_file.write('ansible_become: yes\n')
        the_vars_file.write('ansible_become_method: sudo\n')
        the_vars_file.write('ansible_become_pass: ' + ansible_become_pass + ' \n')
        the_vars_file.write('password_hash: ' + password_hash + ' \n')
        the_vars_file.write('disk_name: ' + disk_name + ' \n')
        the_vars_file.write('name_of_vg: ' + name_of_vg + ' \n')
        the_vars_file.write('name_of_lv: ' + name_of_lv + ' \n')
        the_vars_file.write('folder_name: ' + folder_name + ' \n')
        the_vars_file.write('cluster_name: ' + cluster_name + ' \n')
        the_vars_file.write('hacluster_user: ' + hacluster_user + ' \n')
        the_vars_file.write('hacluster_user_password: ' + hacluster_user_password + ' \n')
        the_vars_file.write('worker_list: ' + worker_list + ' \n')
        the_vars_file.write('worker_ip_list: ' + worker_ip_list + ' \n')
        the_vars_file.write('vcenter_ip: ' + vcenter_ip + ' \n')
        the_vars_file.write('vcenter_user: ' + vcenter_user + ' \n')
        the_vars_file.write('vcenter_password: ' + vcenter_password + ' \n')

ansible_command = 'ansible-playbook -i inventory run.yml'
os.system(ansible_command)

os.remove("inventory")
os.remove("pacemaker-ansible-role/vars/main.yml")
