import sqlite3,os,subprocess,sys
DB='hotel_rms.db'
DB_PATH=os.path.join(os.getcwd(),DB)
conn=sqlite3.connect(DB_PATH)
cur=conn.cursor()
cur.execute('SELECT hotel_name FROM monitored_hotels')
h=cur.fetchall()
if not h:
    print('no monitored hotels')
    conn.close()
    raise SystemExit
hotel=h[-1][0]
print('chosen to delete:',hotel)
cur.execute('DELETE FROM monitored_hotels WHERE hotel_name=?',(hotel,))
conn.commit()
print('deleted from monitored_hotels')
conn.close()
print('running main.py')
subprocess.run([sys.executable,'main.py'],check=True)
conn=sqlite3.connect(DB_PATH)
cur=conn.cursor()
cur.execute('SELECT COUNT(1) FROM room_performance WHERE hotel_name=?',(hotel,))
p_count=cur.fetchone()[0]
cur.execute('SELECT COUNT(1) FROM ota_offers WHERE hotel_name=?',(hotel,))
o_count=cur.fetchone()[0]
print('room_performance rows for deleted hotel:',p_count)
print('ota_offers rows for deleted hotel:',o_count)
# show remaining monitored
cur.execute('SELECT hotel_name FROM monitored_hotels')
print('monitored remaining:', [r[0] for r in cur.fetchall()])
conn.close()
