import sqlite3


# ---------------------------------------------------------------------------------------------------------------------- Fabric
def fabric_show_all(order):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    if order == "name":
        cursor.execute("SELECT rowid, * FROM fabrics ORDER BY name ASC")
    elif order == "color":
        cursor.execute("SELECT rowid, * FROM fabrics ORDER BY color ASC")
    elif order == "material":
        cursor.execute("SELECT rowid, * FROM fabrics ORDER BY material ASC")
    elif order == "length":
        cursor.execute("SELECT rowid, * FROM fabrics ORDER BY length DESC")
    elif order == "width":
        cursor.execute("SELECT rowid, * FROM fabrics ORDER BY width DESC")
    else:
        cursor.execute("SELECT rowid, * FROM fabrics ORDER BY rowid DESC")

    items = cursor.fetchall()
    """
    for item in items:
        print(item)
    """

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()

    return items


def fabric_add_one(name, color, material, length, width, other):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    if name is None:
        name = ""
    if color is None:
        color = ""
    if material is None:
        material = ""
    if length is None:
        length = 0
    if width is None:
        width = 0
    if other is None:
        other = ""

    cursor.execute("INSERT INTO fabrics VALUES (?, ?, ?, ?, ?, ?)", (name, color, material, length, width, other))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


def fabric_delete_one(rowid):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("DELETE FROM fabrics WHERE rowid = " + str(rowid))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


def fabric_lookup(rowid):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM fabrics WHERE rowid = (?)", (rowid,))
    items = cursor.fetchone()
    '''
    for item in items:
        print(item)
    '''
    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()

    return items


def fabric_update(rowid, name, color, material, length, width, other):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE fabrics
    SET name = (?),
    color = (?),
    material = (?),
    length = (?),
    width = (?),
    other = (?)
    WHERE rowid = (?)""", (name, color, material, length, width, other, rowid))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


# ---------------------------------------------------------------------------------------------------------------------- Project
def project_show_all(order):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    if order == "name":
        cursor.execute("SELECT rowid, * FROM projects ORDER BY name ASC")
    elif order == "completed":
        cursor.execute("SELECT rowid, * FROM projects ORDER BY completed ASC")
    else:
        cursor.execute("SELECT rowid, * FROM projects ORDER BY rowid DESC")

    items = cursor.fetchall()
    '''
    for item in items:
        print(item)
    '''

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()

    return items


def project_add_one(name, notes, supplies, measurements, ref, cost, due, completed):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    if name is None:
        name = ""
    if notes is None:
        notes = ""
    if supplies is None:
        supplies = ""
    if measurements is None:
        measurements = ""
    if ref is None:
        ref = ""
    if cost is None:
        cost = ""
    if due is None:
        due = ""
    if completed is None:
        completed = False

    cursor.execute("INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, notes, supplies, measurements, ref, cost, due, completed))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


def project_delete_one(rowid):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("DELETE FROM projects WHERE rowid = " + str(rowid))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


def project_lookup(rowid):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM projects WHERE rowid = (?)", (rowid,))
    items = cursor.fetchone()
    """
    for item in items:
        print(item)
    """
    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()

    return items


def project_update(rowid, name, notes, supplies, measurements, ref, cost, due, completed):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE projects
    SET name = (?),
    notes = (?),
    supplies = (?),
    measurements = (?),
    ref = (?),
    cost = (?),
    due = (?),
    completed = (?)
    WHERE rowid = (?)""", (name, notes, supplies, measurements, ref, cost, due, completed, rowid))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


# ---------------------------------------------------------------------------------------------------------------------- Shopping
def shopping_show_all(order):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    if order == "name":
        cursor.execute("SELECT rowid, * FROM shopping ORDER BY item ASC")
    else:
        cursor.execute("SELECT rowid, * FROM shopping ORDER BY rowid DESC")

    items = cursor.fetchall()
    '''
    for item in items:
        print(item)
    '''

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()

    return items


def shopping_add_one(name):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    if name is None:
        name = ""

    cursor.execute("INSERT INTO shopping VALUES (?)", (name,))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


def shopping_delete_one(rowid):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("DELETE FROM shopping WHERE rowid = " + str(rowid))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


# ---------------------------------------------------------------------------------------------------------------------- Measure
def measure_show_all(order):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    if order == "name":
        cursor.execute("SELECT rowid, * FROM measurements ORDER BY name ASC")
    else:
        cursor.execute("SELECT rowid, * FROM measurements ORDER BY rowid DESC")

    items = cursor.fetchall()
    '''
    for item in items:
        print(item)
    '''
    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()

    return items


def measure_add_one(name, height, bust, waist, hips, in_seam, other, last_date):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    if name is None:
        name = ""
    if height is None:
        height = ""
    if bust is None:
        bust = ""
    if waist is None:
        waist = ""
    if in_seam is None:
        in_seam = ""
    if other is None:
        other = ""
    if last_date is None:
        last_date = ""

    cursor.execute("INSERT INTO measurements VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, height, bust, waist, hips, in_seam, other, last_date))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


def measure_delete_one(rowid):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("DELETE FROM measurements WHERE rowid = " + str(rowid))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


def measure_lookup(rowid):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM measurements WHERE rowid = (?)", (rowid,))
    items = cursor.fetchone()
    """
    for item in items:
        print(item)
    """
    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()

    return items


def measure_update(rowid, name, height, bust, waist, hips, in_seam, other, last_date):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE measurements
        SET name = (?),
        height = (?),
        bust = (?),
        waist = (?),
        hips = (?),
        in_seam = (?),
        other = (?),
        last_date = (?)
        WHERE rowid = (?)""", (name, height, bust, waist, hips, in_seam, other, last_date, rowid))

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()


# ---------------------------------------------------------------------------------------------------------------------- Settings
def reset_table(target):
    # Connect to database
    connection = sqlite3.connect("inventory.db")
    # Create a cursor
    cursor = connection.cursor()

    if target == "fabrics":
        cursor.execute("""DROP TABLE fabrics""")
        cursor.execute("""
        CREATE TABLE fabrics (
            name text,
            color text,
            material text,
            length float,
            width float,
            other float
            )
        """)
    elif target == "projects":
        cursor.execute("""DROP TABLE projects""")
        cursor.execute("""
        CREATE TABLE projects (
            name text,
            notes text,
            supplies text,
            measurements text,
            ref text,
            cost text,
            due text,
            completed bool
            )
        """)
    elif target == "shopping items":
        cursor.execute("""DROP TABLE shopping""")
        cursor.execute("""
        CREATE TABLE shopping (
            item text
            )
        """)
    elif target == "measurements":
        cursor.execute("""DROP TABLE measurements""")
        cursor.execute("""
        CREATE TABLE measurements (
            name text,
            height float,
            bust float,
            waist float,
            hips float,
            in_seam float,
            other text,
            last_date text
            )
        """)
    else:
        print("No target found")

    # Commit our command
    connection.commit()
    # Close our connection
    connection.close()
