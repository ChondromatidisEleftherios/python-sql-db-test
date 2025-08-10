import psycopg2 as pg 

#Σύνδεση στην ήδη υπάρχουσα βάση με τα στοιχεία μας
conn = pg.connect(host="localhost", dbname="Mentoudakis", user="postgres",
	password="Terhs2004.", port=5432)

cur= conn.cursor()

def main():
	while(True):
		print("Μεντουδάκης - Δοκιμάζοντας την SQL") #Κυρίως μενού
		print("1. Εκτέλεση Query")
		print("2. Εισαγωγὴ Δεδομένων")
		print("3. Έξοδος")
		choice=input() #Επιλογη του χρήστη
		choice = int(choice)
		if choice == 3:
			print("Αντίο")
			return 0
		elif choice==1:
			while(True):
				print("Δώστε ένα Query!")
				user_query=input() #Ο χρήστης εισάγει ένα Query
				res=queries(user_query) #Κλήση της συνάρτησης που εκτελεί queries
				if res==0: #Εαν η συνάρτηση επιστρέψει 0, σημαίνει πως έτρεξε σωστά
					print("Θελετε να δοκιμασετε ξανα; [1-Nαι/2-Όχι]")
					choice=input()
					choice=int(choice)
					if choice==2:
						break #Έξοδος από τη while αν ο χρήστης το αποφασίσει, άρα επιστροφή στο κυρίως μενού
		elif choice==2:
			print("[1-SignUp/2-Login]")
			choice=input()
			choice=int(choice)
			if choice==1:
				sign_up() #Κλήση συνάρτησης για δημιουργία λογαριασμού
			elif choice==2:
				login() #Κλήση συνάρτησης για σύνδεση σε λογαριασμό


def sign_up():
	print("Παρακαλώ εισάγετε ένα όνομα χρήστη (τουλάχιστον 3 χαρακτήρες και μικρότερο από 13)")
	user_name=input()
	user_name_test=list(user_name) #Μετρατροπή σε λίστα για να ελέγξουμε το πλήθος των γραμμάτων
	if len(user_name_test) > 2 and len(user_name_test) < 14:
		print("Καλό όνομα χρήστη!")
		print("Παρακαλω πολυ εισάγετε έναν κωδικό (τουλαχιστον 8 χαρακτηρες και μικρότερος από 25)")
		password=input()
		password_test=list(password)
		if len(password_test) > 7 and len(password_test) < 26:
			print("Ορθός Κωδικός")
			command = "INSERT INTO USER_TABLE VALUES ('" + user_name.upper() + "', '" + password.upper() + "');" #Σχηματισμός του query
			cur.execute(command) #Εκτέλεση του query με τα στοιχεία του χρήστη
			conn.commit() #Αποθήκευση των αλλαγών
			return 0

def login():
	while(True):
		print("Παρακαλώ εισάγετε ένα όνομα χρήστη")
		user_name = input()
		command="SELECT NAME FROM USER_TABLE WHERE NAME LIKE '" + user_name.upper() + "';" #Σχηματισμός του query
		cur.execute(command) #Εκτέλεση της εντολής
		conn.commit() #Αποθήκευση των αλλαγών
		result = cur.fetchone() #Πάρε από την εκτέλεση της εντολής, το πρώτο αποτέλεσμα
		result = str(result)
		result = result[2:-3] #Κόψε τα σκουπιδια από το αποτέλεσμα
		if result != user_name.upper():
			print("Δεν βρέθηκε το όνομα χρήστη :(")
			print("Θέλετε να προσπαθήσετε ξανά; [1-Ναι/2-Όχι]")
			choice=input()
			choice=int(choice)
			if choice==2:
				return 1
		else:
			print("Το όνομα χρήστη υπάρχει, τώρα εισάγετε τον κωδικό πρόσβασης")
			password = input()
			command="SELECT PASSWORD FROM USER_TABLE WHERE NAME LIKE '" + user_name.upper() + "' AND password LIKE '" + password.upper() + "';" #Σχηματισμός του query
			cur.execute(command) #Εκτέλεση της εντολής
			conn.commit() #Αποθήκευση των αλλαγών
			result = cur.fetchone() #Πάρε από την εκτέλεση της εντολής, το πρώτο αποτέλεσμα
			result = str(result)
			result = result[2:-3] #Πάρε από την εκτέλεση της εντολής, το πρώτο αποτέλεσμα 
			if result != password.upper():
				print("Λανθασμένος Κωδικός για αυτον το ονομα χρηστη! :(")
				print("Θέλετε να προσπαθήσετε ξανά; [1-Ναι/2-Όχι]")
				choice=input()
				choice=int(choice)
				if choice==2:
					return 1
			else:
				print("Σωστά creds, καλωσόρισες", user_name, "!!! ^-^")
				return 0



def queries(q):
	q.upper() #κάνει όλο το query με κεφαλαία γράμματα
	cur.execute(q) #Εκτέλεση του Query
	conn.commit() #Αποθὴκευση των αλλαγών
	print("Επιτυχής εκτέλεση του Query")
	if "SELECT" in q: #Εμφάνιση των αποτελεσμάτων αν είχαμε τύπου select εντολή
		rows=[]
		print("Η εντολή SELECT επέστρεψε τα εξής: ")
		rows = cur.fetchall() #Πάρε ΟΛΑ τα αποτελέσματα απο την εκτέλεση της εντολής, και βάλε τα σε μια λίστα
		for i in range(len(rows)): #Πέρνα από όλα τα αποτελέσματα γραμμή προς γραμμή
			print("Γραμμή", i+1, ":",rows[i])
			print("-----")
	return 0

if __name__ == '__main__':
	main() #Κλήση της κύριας συνάρτησης με το κυρίως μενού επιλογών
	cur.close() #Αποσύνδεση από τη βάση δεδομένων
