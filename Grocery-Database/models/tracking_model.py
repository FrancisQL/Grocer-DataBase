from db import get_db_connection

def create_tracking_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tracking(
            Tracking_ID varchar(100) primary key,
            Order_ID int not null,
            Status varchar(100) default 'Pending',
            Last_Updated timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def get_all_tracking():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tracking ORDER BY Last_Updated DESC")
    tracking = cursor.fetchall()

    cursor.close()
    conn.close()
    return tracking

def get_tracking_by_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tracking WHERE Order_ID = %s", (order_id,))
    tracking = cursor.fetchone()

    cursor.close()
    conn.close()
    return tracking

def add_tracking(tracking_id, order_id, status="Pending"):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tracking (Tracking_ID, Order_ID, Status) VALUES (%s, %s, %s)",
        (tracking_id, order_id, status)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return tracking_id

def update_tracking_status(tracking_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tracking SET Status = %s WHERE Tracking_ID = %s",
        (status, tracking_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

def insert_tracking_synthetic_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""INSERT IGNORE INTO tracking (Tracking_ID, Order_ID, Status) VALUES
    ('T001', 1, 'Delivered'),
    ('T002', 2, 'Shipped'),
    ('T003', 3, 'Processing'),
    ('T004', 4, 'Pending'),
    ('T005', 5, 'Delivered'),
    ('T006', 6, 'Shipped'),
    ('T007', 7, 'Processing'),
    ('T008', 8, 'Cancelled'),
    ('T009', 9, 'Delivered'),
    ('T010', 10, 'Pending')""")

    conn.commit()
    cursor.close()
    conn.close()
