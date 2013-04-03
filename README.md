android-to-ubuntutouch-contactlist
==================================

This is a very simple, very basic script that convert default android contact list to ubuntu-touch 

First of all, you should export your contacts from your android device then convert it with this script.

## Usage

```
	converter.py exported_contact_list.vcf
```

You should replace your result data with this file in your device:

```
	/usr/share/demo-assets/contacts-data/data.csv
```
and on your device run:

```
	manage-address-books.py
```

It is better to reboot your your device after importing your contacts.

## License
	GPL3