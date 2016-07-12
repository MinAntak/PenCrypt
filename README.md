# PenCrypt
Python script for Linux which creates, mount, automount VeraCrypt container. Also normal and hidden.

Description:
Pencrypt let create hidden volumines in file. User can choose name, location, password, filesystem, size, encryption method. User can also create hidden volume inside container. This volume has diffrent password and size, so it can keep there diffrent files. Program creates special file on pendrive, which let him autodetect container to mount.

Requirements:
	veracrypt
	mount
	umount
	lsblk
	cron
	python3

More details in pencrypt file (Linux manual).