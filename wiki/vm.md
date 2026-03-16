# Virtual machine

<h2>Table of contents</h2>

- [What is a VM](#what-is-a-vm)
- [Your VM](#your-vm)
- [`<your-vm-name>`](#your-vm-name)
- [`<your-vm-ip-address>`](#your-vm-ip-address)
- [Connect to the correct network](#connect-to-the-correct-network)
- [Go to the VMs site](#go-to-the-vms-site)
- [Create a VM](#create-a-vm)
  - [Create a subscription](#create-a-subscription)
  - [Create a VM using the subscription](#create-a-vm-using-the-subscription)
- [Go to the VM page](#go-to-the-vm-page)
- [Get the IP address of the VM](#get-the-ip-address-of-the-vm)
- [Delete the VM](#delete-the-vm)

## What is a VM

A VM (virtual machine) is a software-emulated computer that runs on a physical [host machine](./computer-networks.md#host), with its own [operating system](./operating-system.md#what-is-an-operating-system) and isolated environment.

In this lab, you use a VM provided by the university to deploy and run the application remotely over [`SSH`](./ssh.md#what-is-ssh).

Docs:

- [What is a virtual machine?](https://azure.microsoft.com/en-us/resources/cloud-computing-dictionary/what-is-a-virtual-machine)

## Your VM

The university provides you a virtual machine (VM) for labs and home experiments for the duration of the `Software Engineering Toolkit` course.

You probably won't have access to the VMs after the course finishes.

See [VM image](./vm-info.md) for the information about your VM.

## `<your-vm-name>`

The name you chose when [creating the VM](#create-a-vm-using-the-subscription) (without `<` and `>`).

## `<your-vm-ip-address>`

The [IP address](./computer-networks.md#ip-address) (without `<` and `>`) of [your VM](#your-vm) in the `UniversityStudent` [network](./computer-networks.md#what-is-a-network).

Example: `192.0.2.1`.

See [Get the IP address of the VM](#get-the-ip-address-of-the-vm).

## Connect to the correct network

1. Disable `VPN`.

2. Connect your local machine (laptop) to the `Wi-Fi` network `UniversityStudent`.

## Go to the VMs site

1. Open the [https://vm.innopolis.university](https://vm.innopolis.university) site in a browser.

## Create a VM

Complete these steps to create a VM:

<!-- no toc -->
1. [Create a subscription](#create-a-subscription)
2. [Create a new `SSH` key](./vm-access.md#create-a-new-ssh-key)
3. [Create a VM using the subscription](#create-a-vm-using-the-subscription)

### Create a subscription

1. [Go to the VMs site](#go-to-the-vms-site).
2. Click `NEW`.
3. Click `ADD SUBSCRIPTION`.
4. Click `Software Engineering Toolkit`.
5. Click checkmark.
6. Go to the [`SUBSCRIPTIONS`](https://vm.innopolis.university/#Workspaces/MyAccountExtension/subscriptions) tab.
7. Look at the `SUBSCRIPTION` column.

   You should see there `Software Engineering Toolkit`.

   The `Status` of this subscription can be `Syncing` or `Active`.

   It can be `Syncing` for a long time.

   Nevertheless, you'll be able to [create a VM using this subscription](#create-a-vm-using-the-subscription) in approximately 15 minutes.

   Don't just sit and wait. Complete other steps.

### Create a VM using the subscription

1. [Create a new `SSH` key](./vm-access.md#create-a-new-ssh-key) if not created.
2. [Go to the `vm.innopolis.university` site](#go-to-the-vms-site).
3. Click `+ NEW`.
4. Click `STANDALONE VIRTUAL MACHINE`.
5. Click `FROM GALLERY`.
6. Click `ALL`.
7. Click `Linux Ubuntu 24.04 Software Engineering Toolkit`.
8. Click `->` to go to the page 2.
9. Fill in the fields:
    - `NAME`: Write the name of your VM (we'll refer to it as [`<your-vm-name>`](#your-vm-name) in the instructions).
    - `NEW PASSWORD`: Write the password.
    - `CONFIRM`: Write the same password.
    - `ADMINISTRATOR SSH KEY`:
       1. [Find the `SSH` key files](./vm-access.md#find-the-ssh-key-files).
       2. Copy the **full content** of the public key file.
       3. Paste the content into the input field.
10. Note that the user's name on the VM is [`root`](./linux.md#the-user-root).
11. Click `->` to go to the page 3.
12. Go to `NETWORK ADAPTER 1`.
13. Click `Not Connected`.
14. In the drop-down list, click `StudentsCourses01;10.93.24.0/22`.
15. Click checkmark to complete the setup.
16. The VM will become available in approximately 20 minutes.

## Go to the VM page

1. [Go to the VMs site](#go-to-the-vms-site).
2. Open the `VIRTUALS MACHINES` tab ([https://vm.innopolis.university/#Workspaces/VMExtension/VirtualMachines](https://vm.innopolis.university/#Workspaces/VMExtension/VirtualMachines)).
3. Look at the `NAME`.
4. Find `<your-vm-name>`.
5. The `STATUS` should be `Running`.
6. Click `<your-vm-name>`.
7. Click `DASHBOARD`.
8. You should be on the VM page.

## Get the IP address of the VM

1. [Go to the VM page](#go-to-the-vm-page).
2. Go to the `quick glance` sidebar (on the right).
3. Go to `IP Address(es)`.
4. You should see there `StudentsCourses01` - [`<your-vm-ip-address>`](#your-vm-ip-address).

   Example: `StudentsCourses01` - `192.0.2.1`

## Delete the VM

1. [Go to the VM page](#go-to-the-vm-page).
2. Click `DELETE`.
