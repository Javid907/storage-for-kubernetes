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

ip_address_vcenter = str(input("Please type ip address vcenter: "))
worker_list = str(input("Please type list of workers name: "))
data_worker_list = worker_list.split()
head_worker = input("Please type name of first worker: ")
add_share = input("Will you add shared disk in vcenter(yes/no)? ")
if add_share == "yes" or add_share == "y" or add_share == "Y" or add_share == "YES" or add_share == "Yes":
    mkdir = 'mkdir add-share-disk/group_vars'
    cp_1 = 'cp add-share-disk/esxi-role-change-vmx/tasks/main.orig add-share-disk/esxi-role-change-vmx/tasks/main.yaml'
    cp_2 = 'cp add-share-disk/vcenter-poweroff-workers/tasks/main.orig add-share-disk/vcenter-poweroff-workers/tasks/main.yaml'
    cp_3 = 'cp add-share-disk/vcenter-poweron-workers/tasks/main.orig add-share-disk/vcenter-poweron-workers/tasks/main.yaml'
    cp_4 = 'cp add-share-disk/add-disk-to-workers/tasks/secondary_worker.orig add-share-disk/add-disk-to-workers/tasks/secondary_worker.yml'
    cp_5 = 'cp add-share-disk/add-disk-to-workers/tasks/change_vmx_file_1.orig add-share-disk/add-disk-to-workers/tasks/change_vmx_file_1.yml'
    cp_6 = 'cp add-share-disk/add-disk-to-workers/tasks/change_vmx_file_2.orig add-share-disk/add-disk-to-workers/tasks/change_vmx_file_2.yml'
    os.system(cp_1)
    os.system(cp_2)
    os.system(cp_3)
    os.system(cp_4)
    os.system(cp_5)
    os.system(cp_6)
    os.system(mkdir)



    ip_address_esxi = input("Please type ip address esxi: ")
    vcenter_hostname = ip_address_vcenter
    vcenter_username = input("Please type name of Administrator vcenter user: ")
    vcenter_password = getpass.getpass("Please type password of Administrator for VCenter: ")
    vmx_path = "/vmfs/volumes/"
    datastore = input("Please type name of Datastore: ")
    ansible_connection = "ssh"
    ansible_user = "root"
    ansible_root_pass = getpass.getpass("Please type password of root for ESXI: ")
    disk_size = input("Please type size of disk: ")
    with open('add-share-disk/group_vars/all.yaml', 'a+') as the_group_vars_file:
        the_group_vars_file.write('---\n')
        the_group_vars_file.write('vcenter_hostname: ' + vcenter_hostname + ' \n')
        the_group_vars_file.write('vcenter_username: ' + vcenter_username + ' \n')
        the_group_vars_file.write('vcenter_password: ' + vcenter_password + ' \n')
        the_group_vars_file.write('vmx_path: ' + vmx_path + ' \n')
        the_group_vars_file.write('datastore: ' + datastore + ' \n')
        the_group_vars_file.write('disk_size: ' + disk_size + ' \n')
        the_group_vars_file.write('head_worker: ' + head_worker + ' \n')
        number = 0
        for worker in data_worker_list:
            number = number + 1
            the_group_vars_file.write('worker' + str(number) + ': ' + worker + ' \n')

    with open('add-share-disk/esxi-role-change-vmx/tasks/main.yaml', 'a+') as the_main_1_file:
        the_main_1_file.write('  with_items:\n')
        number = 0
        for worker in data_worker_list:
            number = number + 1
            the_main_1_file.write('      - { worker: "{{ worker' + str(number) + ' }}", worker_vmx: "{{ worker' + str(number) + ' }}" }\n')
        the_main_1_file.write('  when: inventory_hostname in groups ["esxi"]\n')

    with open('add-share-disk/vcenter-poweroff-workers/tasks/main.yaml', 'a+') as the_main_2_file:
        the_main_2_file.write('    with_items:\n')
        number = 0
        for worker in data_worker_list:
            number = number + 1
            the_main_2_file.write('          - "{{ worker' + str(number) + ' }}"\n')
        the_main_2_file.write('    delegate_to: localhost\n')

    with open('add-share-disk/vcenter-poweron-workers/tasks/main.yaml', 'a+') as the_main_3_file:
        the_main_3_file.write('    with_items:\n')
        number = 0
        for worker in data_worker_list:
            number = number + 1
            the_main_3_file.write('          - "{{ worker' + str(number) + ' }}"\n')
        the_main_3_file.write('    delegate_to: localhost\n')

    with open('vsphere-inventory', 'a+') as the_vsphere_inventory_file:
        the_vsphere_inventory_file.write('[vcenter]\n')
        the_vsphere_inventory_file.write(ip_address_vcenter + '\n')
        the_vsphere_inventory_file.write('[esxi]\n')
        the_vsphere_inventory_file.write(ip_address_esxi + '\n')
        the_vsphere_inventory_file.write('[esxi:vars]\n')
        the_vsphere_inventory_file.write('ansible_connection=' + ansible_connection + ' \n')
        the_vsphere_inventory_file.write('ansible_user=' + ansible_user + ' \n')
        the_vsphere_inventory_file.write('ansible_ssh_pass=' + ansible_root_pass + ' \n')

    with open('add-share-disk/add-disk-to-workers/tasks/secondary_worker.yml', 'a+') as the_secondary_worker:
        the_secondary_worker.write('  with_items:\n')
        number = 0
        for worker in data_worker_list:
            if worker != head_worker:
                number = number + 1
                the_secondary_worker.write('        - "{{ worker' + str(number) + ' }}"\n')
        the_secondary_worker.write('  delegate_to: localhost\n')

    with open('add-share-disk/add-disk-to-workers/tasks/change_vmx_file_1.yml', 'a+') as the_change_vmx_file_1:
        the_change_vmx_file_1.write('  with_items:\n')
        number = 0
        for worker in data_worker_list:
            number = number + 1
            the_change_vmx_file_1.write('      - { worker: "{{ worker' + str(number) + ' }}", worker_vmx: "{{ worker' + str(number) + ' }}" }\n')
        the_change_vmx_file_1.write('  when: inventory_hostname in groups ["esxi"]\n')

    with open('add-share-disk/add-disk-to-workers/tasks/change_vmx_file_2.yml', 'a+') as the_change_vmx_file_2:
        the_change_vmx_file_2.write('  with_items:\n')
        number = 0
        for worker in data_worker_list:
            number = number + 1
            the_change_vmx_file_2.write('      - { worker: "{{ worker' + str(number) + ' }}", worker_vmx: "{{ worker' + str(number) + ' }}" }\n')
        the_change_vmx_file_2.write('  when: inventory_hostname in groups ["esxi"]\n')

    ansible_command = 'ansible-playbook -i vsphere-inventory vsphere-site.yaml'
    os.system(ansible_command)
    os.remove("add-share-disk/group_vars/all.yaml")
    os.remove("vsphere-inventory")
    os.remove("add-share-disk/esxi-role-change-vmx/tasks/main.yaml")
    os.remove("add-share-disk/vcenter-poweroff-workers/tasks/main.yaml")
    os.remove("add-share-disk/vcenter-poweron-workers/tasks/main.yaml")
    os.remove("add-share-disk/add-disk-to-workers/tasks/secondary_worker.yml")
    os.remove("add-share-disk/add-disk-to-workers/tasks/change_vmx_file_1.yml")
    os.remove("add-share-disk/add-disk-to-workers/tasks/change_vmx_file_2.yml")


elif add_share == "no" or add_share == "n" or add_share == "N" or add_share == "NO" or add_share == "No":
    print('You will continue process  without adding disk if you yourself did not add disk you will see error')


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
    elif ansible_become == "no" or ansible_become == "n" or ansible_become == "N" or ansible_become == "NO" or ansible_become == "No":
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
worker_ip_list = input("Please type list of workers ip: ")
vcenter_ip = ip_address_vcenter
vcenter_user = input("Please type name of vcenter user for fencing: ")
vcenter_password = getpass.getpass("Please type password of vcenter user: ")
password_hash = sha512_crypt.using(rounds=5000).hash(hacluster_pass)

if ssh_port == "" or ssh_port == "22":
    ssh_port = "22"
elif ssh_port != "":
    ssh_port = ssh_port

if not os.path.exists('/tmp/test'):
    os.mknod('/tmp/test')

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
