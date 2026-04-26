from connect import connect
import csv
import json


def run_sql_file(filename):
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    with open(filename, "r", encoding="utf-8") as file:
        cur.execute(file.read())

    conn.commit()
    cur.close()
    conn.close()


def setup_database():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")
    run_sql_file("functions.sql")
    print("Database is ready!")


def get_group_id(cur, group_name):
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
        (group_name,)
    )
    cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cur.fetchone()[0]


def add_contact():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group_name = input("Group (Family/Work/Friend/Other): ")
    phone = input("Phone: ")
    phone_type = input("Phone type (home/work/mobile): ")

    group_id = get_group_id(cur, group_name)

    cur.execute(
        """
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (name) DO UPDATE
        SET email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id
        RETURNING id
        """,
        (name, email, birthday, group_id)
    )

    contact_id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
        (contact_id, phone, phone_type)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added!")


def show_all_contacts(order_by="name"):
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    allowed_sort = {
        "name": "c.name",
        "birthday": "c.birthday",
        "date": "c.created_at"
    }

    sort_column = allowed_sort.get(order_by, "c.name")

    cur.execute(f"""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY {sort_column}
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_contact():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    query = input("Search text: ")

    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    group_name = input("Group name: ")

    cur.execute("""
        SELECT
            c.name,
            c.email,
            c.birthday,
            g.name,
            COALESCE(STRING_AGG(p.phone || ' (' || p.type || ')', ', '), '') AS phones
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name ILIKE %s
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.name
    """, (group_name,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_email():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()
    email = input("Email search: ")

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        WHERE c.email ILIKE %s
        ORDER BY c.name
    """, (f"%{email}%",))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def paginated_navigation():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    limit = int(input("Page size: "))
    offset = 0

    while True:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()

        print("\n--- PAGE ---")
        if not rows:
            print("No contacts on this page.")
        else:
            for row in rows:
                print(row)

        command = input("\nnext / prev / quit: ").lower()

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Invalid command!")

    cur.close()
    conn.close()


def update_contact():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    name = input("Contact name to update: ")
    new_email = input("New email: ")
    new_birthday = input("New birthday (YYYY-MM-DD): ")
    new_group = input("New group: ")

    group_id = get_group_id(cur, new_group)

    cur.execute("""
        UPDATE contacts
        SET email = %s,
            birthday = %s,
            group_id = %s
        WHERE name = %s
    """, (new_email, new_birthday, group_id, name))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated!")


def delete_contact():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    name = input("Name to delete: ")

    cur.execute("DELETE FROM contacts WHERE name = %s", (name,))

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted!")


def add_phone_to_existing_contact():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    name = input("Contact name: ")
    phone = input("New phone: ")
    phone_type = input("Type (home/work/mobile): ")

    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()
    print("Phone added!")


def move_contact_to_group():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    name = input("Contact name: ")
    group_name = input("New group: ")

    cur.execute("CALL move_to_group(%s, %s)", (name, group_name))

    conn.commit()
    cur.close()
    conn.close()
    print("Moved to group!")


def import_from_csv():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    filename = input("CSV filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            group_id = get_group_id(cur, row["group"])

            cur.execute(
                """
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                SET email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id
                """,
                (row["name"], row["email"], row["birthday"], group_id)
            )

            contact_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, row["phone"], row["type"])
            )

    conn.commit()
    cur.close()
    conn.close()
    print("CSV imported!")


def export_to_json():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            p.phone,
            p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        ORDER BY c.name
    """)

    rows = cur.fetchall()

    contacts = {}

    for contact_id, name, email, birthday, group_name, phone, phone_type in rows:
        if contact_id not in contacts:
            contacts[contact_id] = {
                "name": name,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group_name,
                "phones": []
            }

        if phone:
            contacts[contact_id]["phones"].append({
                "phone": phone,
                "type": phone_type
            })

    with open("contacts.json", "w", encoding="utf-8") as file:
        json.dump(list(contacts.values()), file, indent=4, ensure_ascii=False)

    cur.close()
    conn.close()
    print("Exported to contacts.json!")


def import_from_json():
    conn = connect()
    if conn is None:
        return

    cur = conn.cursor()

    filename = input("JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        name = item["name"]

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"{name} already exists. skip/overwrite? ").lower()

            if choice == "skip":
                continue

            if choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name = %s", (name,))

        group_id = get_group_id(cur, item["group"])

        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (item["name"], item["email"], item["birthday"], group_id))

        contact_id = cur.fetchone()[0]

        for phone_item in item["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone_item["phone"], phone_item["type"]))

    conn.commit()
    cur.close()
    conn.close()
    print("JSON imported!")


def menu():
    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1. Setup database")
        print("2. Add contact")
        print("3. Show all contacts")
        print("4. Search contacts")
        print("5. Search by email")
        print("6. Filter by group")
        print("7. Sort contacts")
        print("8. Paginated navigation")
        print("9. Update contact")
        print("10. Delete contact")
        print("11. Add phone to contact")
        print("12. Move contact to group")
        print("13. Import from CSV")
        print("14. Export to JSON")
        print("15. Import from JSON")
        print("16. Exit")

        choice = input("Choose: ")

        if choice == "1":
            setup_database()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            show_all_contacts()
        elif choice == "4":
            search_contact()
        elif choice == "5":
            search_by_email()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            sort_choice = input("Sort by name/birthday/date: ")
            show_all_contacts(sort_choice)
        elif choice == "8":
            paginated_navigation()
        elif choice == "9":
            update_contact()
        elif choice == "10":
            delete_contact()
        elif choice == "11":
            add_phone_to_existing_contact()
        elif choice == "12":
            move_contact_to_group()
        elif choice == "13":
            import_from_csv()
        elif choice == "14":
            export_to_json()
        elif choice == "15":
            import_from_json()
        elif choice == "16":
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    menu()
