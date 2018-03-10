import sqlite3


conn= sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute("""Drop table  users""")
cur.execute("""create table users(
	fname text,
	lname text,
	emorph text primary key,
	encpasswd text
	)""")


conn.commit()
conn.close()
