import os
import csv
import re
import unicodedata
import psycopg2


# # # # DATA BASE MANIPULATION # # # #

class DatabaseConnection:
	def __init__ (self):
		try:
			self.connection = psycopg2.connect("dbname='bd_bitcoin' user='postgres' host='localhost' password='*******' port='5432'")
			self.connection.autocommit = True
			self.cursor = self.connection.cursor()
		except:
			print("Cannot connect to database")

	def query_all(self):
		self.cursor.execute("SELECT * FROM noticias")
		result = self.cursor.fetchall()
		return result

	def insert(self, date, text, user):
		self.cursor.execute("SELECT max(codigo) FROM noticias")
		last_cod = self.cursor.fetchall()
		next_cod = last_cod[0][0]+1

		# add line in data base
		self.cursor.execute("INSERT INTO noticias (codigo, data, texto, usuario) VALUES ('%s', '"+date+"', '"+text+"', '"+user+"')", (next_cod, ))


# # # # DATA BASE MANIPULATION # # # #


# # # # TWEET MANIPULATION # # # #
class TweetManipulation():

	# limpa todo o conteudo desnecessário do texto
	def clean_tweet(self, tweet):
		
	    # Unicode normalize transforma um caracter em seu equivalente em latin.
	    nfkd = unicodedata.normalize('NFKD', tweet)
	    word_without_accent = u"".join([c for c in nfkd if not unicodedata.combining(c)])

	    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
	    return re.sub("(@ [A-Za-z0-9]+)|([^0-9A-Za-z $])|(\w+:\/\/\S+)", "", word_without_accent)

	# retorna numero correspondente a cada mes
	def translate_month(self, month):

		correct_month = 0

		months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

		for m in months:
			correct_month += 1
			if(m == month):
				return str(correct_month)

	# retorna data no padrao (dia mes ano)
	def format_date(self, full_tweet):
		
		# separa a data do resto do tweet
		date = full_tweet

		if(len(date.split(' ')) > 2):
			day = date.split(' ')[0]
			month = self.translate_month(date.split(' ')[1])
			year = date.split(' ')[2]
		else:
			day = date.split(' ')[1]
			month = self.translate_month(date.split(' ')[0])
			year = '2019'

		date = day + "." + month + "." + year 

		return date

	def format_text(self, full_tweet):

		text = self.clean_tweet(full_tweet)

		return text

	# verifica se é um tweet valido (formato data e tweet)
	def validation_of_date(self, full_tweet):
		
		tweet = full_tweet.split('\t')

		if(tweet[0] != '' and len(tweet) == 2 and tweet[1][0] != 'No results'):
			return 1
		else:
			return 0
# # # # TWEET MANIPULATION # # # #



if __name__ == '__main__':

	database_connection = DatabaseConnection()
	tweet_manipulation = TweetManipulation()

	tweets_file = open('/home/administrador/Documentos/UFOP/5º Periodo/BITCOIN/proximo_passo/tweetsOglobo.csv', 'r')

	tweet_list = csv.reader(tweets_file)

	for line in tweet_list:

		date = tweet_manipulation.format_date(line[0])	
		text = tweet_manipulation.format_text(line[1])
		user = line[2]	

		database_connection.insert(date, text, user)


	tweets_file.close()

# # # # END CODE # # # #