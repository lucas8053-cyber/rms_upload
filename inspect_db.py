import sqlite3,os
DB='hotel_rms.db'
DB_PATH=os.path.join(os.getcwd(),DB)
conn=sqlite3.connect(DB_PATH)
cur=conn.cursor()
print('monitored_hotels:')
for r in cur.execute('SELECT hotel_name FROM monitored_hotels').fetchall():
    print('-',r[0])
print('\nroom_performance distinct hotels:')
for r in cur.execute('SELECT DISTINCT hotel_name FROM room_performance').fetchall():
    print('-',r[0])
print('\nota_offers distinct hotels:')
for r in cur.execute('SELECT DISTINCT hotel_name FROM ota_offers').fetchall():
    print('-',r[0])
conn.close()
