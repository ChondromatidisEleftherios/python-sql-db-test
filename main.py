import psycopg2 as pg 
#
conn = pg.connect(host="localhost", dbname="Mentoudakis", user="postgres",
	password="Terhs2004.", port=5432)

cur= conn.cursor()

def main():
	while(True):
		print("Μεντουδάκης - Δοκιμάζοντας την SQL")
		print("1. Εκτέλεση Query")
		print("2. Εισαγωγὴ Δεδομένων")
		print("3. Έξοδος")
		choice=input()
		choice = int(choice)
		if choice == 3:
			print("Αντίο")
			return 0
		elif choice==1:
			while(True):
				print("Δώστε ένα Query!")
				user_query=input()
				res=queries(user_query)
				if res==0:
					print("Θελετε να δοκιμασετε ξανα; [1-Nαι/2-Όχι]")
					choice=input()
					choice=int(choice)
					if choice==2:
						break
		elif choice==2:
			print("[1-Login/2-SignUp]")
			choice=input()
			choice=int(choice)
			if choice==2:
				sign_up()
			elif choice==1:
				login()


def sign_up():
	print("Παρακαλώ εισάγετε ένα όνομα χρήστη (τουλάχιστον 3 χαρακτήρες και μικρότερο από 13)")
	user_name=input()
	user_name_test=list(user_name)
	if len(user_name_test) > 2 and len(user_name_test) < 14:
		print("Καλό όνομα χρήστη!")
		print("Παρακαλω πολυ εισάγετε έναν κωδικό (τουλαχιστον 8 χαρακτηρες και μικρότερος από 25)")
		password=input()
		password_test=list(password)
		if len(password_test) > 7 and len(password_test) < 26:
			print("Ορθός Κωδικός")
			command = "INSERT INTO USER_TABLE VALUES ('" + user_name.upper() + "', '" + password.upper() + "');"
			cur.execute(command)
			conn.commit()
			return 0

def login():
	while(True):
		print("Παρακαλώ εισάγετε ένα όνομα χρήστη")
		user_name = input()
		command="SELECT NAME FROM USER_TABLE WHERE NAME LIKE '" + user_name.upper() + "';"
		cur.execute(command)
		result = cur.fetchone()
		result = str(result)
		result = result[2:-3]
		if result != user_name.upper():
			print("Δεν βρέθηκε το όνομα χρήστη :(")
			print("Θέλετε να προσπαθήσετε ξανά; [1-Ναι/2-Όχι]")
			choice=input()
			choice=int(choice)
			if choice==2:
				return 1
		else:
			print("Το όνομα χρήστη υπάρχει, εισάγετε τον κωδικό πρόσβασης")
			password = input()
			command="SELECT PASSWORD FROM USER_TABLE WHERE NAME LIKE '" + user_name.upper() + "' AND password LIKE '" + password.upper() + "';"
			cur.execute(command)
			result = cur.fetchone()
			result = str(result)
			result = result[2:-3]
			if result != password.upper():
				print("Λανθασμένος Κωδικός για αυτον το ονομα χρηστη! :(")
				print("Θέλετε να προσπαθήσετε ξανά; [1-Ναι/2-Όχι]")
				choice=input()
				choice=int(choice)
				if choice==2:
					return 1
			else:
				print("Σωστά creds, καλωσόρισες", user_name, "!!! ")
				return 0



def queries(q):
	q.upper()
	cur.execute(q)
	conn.commit()
	print("Επιτυχής εκτέλεση του Query")
	if "SELECT" in q:
		print("Η εντολή SELECT επέστρεψε τα εξής: ")
		rows = cur.fetchall()
		for i in range(len(rows)):
			print("Γραμμή", i+1, ":",rows[i])
			print("----")
	return 0

if __name__ == '__main__':
	main()
	cur.close()
