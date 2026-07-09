import sqlite3

# ---------------- DATABASE CONNECTION ---------------- #

conn = sqlite3.connect("blood_bank.db")
cursor = conn.cursor()

# ---------------- CREATE TABLES ---------------- #

cursor.execute("""
CREATE TABLE IF NOT EXISTS donors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    blood_group TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blood(
    blood_group TEXT PRIMARY KEY,
    units INTEGER NOT NULL
)
""")

conn.commit()

# Valid Blood Groups
VALID_BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


# ---------------- FUNCTIONS ---------------- #

def add_donor():
    print("\n----- Add Donor -----")

    name = input("Enter Name: ").strip()

    if not name.replace(" ", "").isalpha():
        print("❌ Invalid Name!")
        return

    try:
        age = int(input("Enter Age: "))
    except ValueError:
        print("❌ Age must be a number!")
        return

    if age < 18 or age > 65:
        print("❌ Age should be between 18 and 65.")
        return

    blood = input("Enter Blood Group: ").upper().strip()

    if blood not in VALID_BLOOD_GROUPS:
        print("❌ Invalid Blood Group!")
        return

    phone = input("Enter Phone Number: ").strip()

    if not phone.isdigit() or len(phone) != 10:
        print("❌ Phone number must contain exactly 10 digits.")
        return

    cursor.execute(
        "INSERT INTO donors(name, age, blood_group, phone) VALUES (?, ?, ?, ?)",
        (name, age, blood, phone),
    )

    conn.commit()

    print("✅ Donor added successfully!")


def view_donors():
    print("\n----- Donor List -----")

    cursor.execute("SELECT * FROM donors")
    data = cursor.fetchall()

    if not data:
        print("No donors found.")
        return

    print("-" * 65)

    for row in data:
        print(
            f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Blood: {row[3]} | Phone: {row[4]}"
        )


def add_blood():
    print("\n----- Add Blood Stock -----")

    blood = input("Enter Blood Group: ").upper().strip()

    if blood not in VALID_BLOOD_GROUPS:
        print("❌ Invalid Blood Group!")
        return

    try:
        units = int(input("Enter Units: "))
    except ValueError:
        print("❌ Units must be a number.")
        return

    if units <= 0:
        print("❌ Units must be greater than zero.")
        return

    cursor.execute(
        "SELECT units FROM blood WHERE blood_group=?",
        (blood,),
    )

    data = cursor.fetchone()

    if data:
        cursor.execute(
            "UPDATE blood SET units = units + ? WHERE blood_group=?",
            (units, blood),
        )
    else:
        cursor.execute(
            "INSERT INTO blood(blood_group, units) VALUES(?, ?)",
            (blood, units),
        )

    conn.commit()

    print("✅ Blood stock updated successfully!")


def view_stock():
    print("\n----- Blood Stock -----")

    cursor.execute("SELECT * FROM blood")

    data = cursor.fetchall()

    if not data:
        print("No blood stock available.")
        return

    print("-" * 30)

    for row in data:
        print(f"Blood Group: {row[0]} | Units: {row[1]}")


def search_blood():
    print("\n----- Search Blood -----")

    blood = input("Enter Blood Group: ").upper().strip()

    if blood not in VALID_BLOOD_GROUPS:
        print("❌ Invalid Blood Group!")
        return

    cursor.execute(
        "SELECT units FROM blood WHERE blood_group=?",
        (blood,),
    )

    data = cursor.fetchone()

    if data:
        print(f"🩸 Available Units: {data[0]}")
    else:
        print("❌ Blood not available.")


def issue_blood():
    print("\n----- Issue Blood -----")

    blood = input("Enter Blood Group: ").upper().strip()

    if blood not in VALID_BLOOD_GROUPS:
        print("❌ Invalid Blood Group!")
        return

    try:
        units = int(input("Enter Units Required: "))
    except ValueError:
        print("❌ Invalid units.")
        return

    if units <= 0:
        print("❌ Units must be greater than zero.")
        return

    cursor.execute(
        "SELECT units FROM blood WHERE blood_group=?",
        (blood,),
    )

    data = cursor.fetchone()

    if data is None:
        print("❌ Blood group not found.")
        return

    available = data[0]

    if available >= units:
        cursor.execute(
            "UPDATE blood SET units = units - ? WHERE blood_group=?",
            (units, blood),
        )

        conn.commit()

        print("✅ Blood issued successfully.")
        print(f"Remaining Units: {available - units}")

    else:
        print(f"❌ Only {available} units available.")


def delete_donor():
    print("\n----- Delete Donor -----")

    try:
        donor_id = int(input("Enter Donor ID: "))
    except ValueError:
        print("❌ Invalid ID.")
        return

    cursor.execute(
        "SELECT * FROM donors WHERE id=?",
        (donor_id,),
    )

    donor = cursor.fetchone()

    if donor:
        cursor.execute(
            "DELETE FROM donors WHERE id=?",
            (donor_id,),
        )

        conn.commit()

        print("✅ Donor deleted successfully.")

    else:
        print("❌ Donor ID not found.")


# ---------------- MAIN MENU ---------------- #

try:

    while True:

        print("\n")
        print("=" * 45)
        print("      BLOOD BANK MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. Add Donor")
        print("2. View Donors")
        print("3. Add Blood Stock")
        print("4. View Blood Stock")
        print("5. Search Blood")
        print("6. Issue Blood")
        print("7. Delete Donor")
        print("8. Exit")
        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_donor()

        elif choice == "2":
            view_donors()

        elif choice == "3":
            add_blood()

        elif choice == "4":
            view_stock()

        elif choice == "5":
            search_blood()

        elif choice == "6":
            issue_blood()

        elif choice == "7":
            delete_donor()

        elif choice == "8":
            print("\nThank you for using Blood Bank Management System.")
            break

        else:
            print("❌ Invalid choice! Please try again.")

except KeyboardInterrupt:
    print("\n\nProgram interrupted by user.")

finally:
    conn.close()
    print("Database connection closed.")