import json
import re
import sys
from ldif import LDIFParser

extract_pattern = r'cn=(.+),mail=(.+)'
dn_email_dict = {}
cn_email_dict = {}


def parse_ldif(filename):
    try:
        with open(filename, 'rb') as f:
            ldif_parser = LDIFParser(f)
            for dn, record in ldif_parser.parse():
                if 'mail' in record:
                    email = record['mail'][0]
                    dn_email_dict[email] = json.dumps(record)
                if 'cn' in record:
                    cn_email_dict[email] = dn
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def process_groups(filename):
    group_members = {}

    try:
        with open(filename, 'rb') as ldif_file:
            parser = LDIFParser(ldif_file)

            for dn, record in parser.parse():
                name = dn.split(',')[0].split('=')[1]
                groups = record.get('memberOf', [])

                for group in groups:
                    if group in group_members:
                        if dn in group_members[group]:
                            print(f"{name}, {group}")

                object_class = record.get('objectClass', []) if record.get('objectClass', []) != [] else record.get('objectclass', [])

                if 'groupOfNames' in object_class:
                    process_group_record(dn, record, group_members)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def process_group_record(dn, record, group_members):
    group_name = dn.split(',')[0].split('=')[1]
    members = record.get('member', [])

    for member in members:
        member_details = re.search(extract_pattern, member)
        if member_details is not None:
            email = member_details.group(2)
            first_name, last_name = extract_name(member_details.group(1))
            print(f"'{first_name}', '{last_name}', '{email}', '{cn_email_dict.get(email, '')}', '{dn_email_dict.get(email, '')}', '{group_name}'")

    group_members[group_name] = members


def extract_name(name):
    name = name.replace("\"", "")
    if ',' in name:
        first_name, last_name = name.split(',', 1)
    elif ' ' in name:
        first_name, last_name = name.split(' ', 1)
    else:
        first_name, last_name = name, ""
    return first_name.strip(), last_name.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide the path to an LDIF file as an argument.")
        sys.exit(1)

    ldif_filename = sys.argv[1]

    try:
        parse_ldif(ldif_filename)
        process_groups(ldif_filename)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)