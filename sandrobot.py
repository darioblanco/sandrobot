# coding=utf-8

# Copyright (C) 2012  Darío Blanco Iturriaga

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


from twitter.api import Twitter, TwitterError, TwitterHTTPError
from twitter.oauth import OAuth, write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance
# http://mike.verdone.ca/twitter/ - (easy_install twitter)

import os
import random
import re
import time
import sys

byebye = " Bendiciones y buenas noches"

sandro_reply = [
	u"Predicciones exactas. Tu número de la suerte es el %s, y cada día el de más gente.",
	u"Cariño coge un boli rápido que me aparece tu número de la suerte: el %s.",
	u"Yo en su armario veo un abrigo marrón. Su nº de la suerte que le dará suerte: %s.",
	u"Su número de la suerte es el %s. Va a encontrar trabajo en x^2 días, predicciones exactas.",
	u"Líneas preferentes sin esperas, tu nº de la suerte por los astros y las estrellas es %s.",
	u"Cariño, deberías denunciar. No te preocupes que aquí está tu número de la suerte: %s.",
	u"Bienvenida sea usted señora. Sé que le preocupa algo. Su número de la suerte es el %s.",
	u"Bienvenida sea usted, deberías consultar al mejor homeópata. Coja el número rápido: %s.",
	u"Eso se llama predicciones exactas, afirmaciones exactas. Su número de la suerte: %s.",
	u"Te preocupa la economía. Esto son predicciones exactas. Tome su número de la suerte: %s.",
	u"Te veo delante de un ordenador, predicciones exactas. Su número de la suerte: %s.",
	u"Usas Twitter habitualmente, ¿verdad? Sandro vuelve a acertar, y le doy su número: %s.",
	u"Esta noche quiero marcar una gran diferencia. Yo afirmo, su número de la suerte: %s.",
	u"Bienvenida sea usted señora. Por el poder de los santos y los gamusinos, tu número: %s.",
	u"¿De donde me llama usted? Bonita ciudad, su número de la suerte: %s.",
	u"En abril, predicciones mil. Su número de la suerte: %s.",
	u"Hay en su familia alguien a quien le gustan mucho los búhos. Su nº de la suerte: %s.",
	u"Yo perfecto no soy, y siempre lo he dicho, su número de la suerte es %s, toca seguro.",
	u"¿Está preocupada por sus hijos verdad? Ah, que no tiene hijos. Tome su nº de la suerte: %s.",
	u"¿El número de la lotería? Y tanto faltaría más, el %s.",
	u"¿He fallado? Es que estoy percibiendo la energía de la próxima llamada. Su número: %s.",
	u"Tu denúncialo, porque si no lo haces, no te va a respetar nunca. La suerte está en %s.",
	u"Sandro Rey a su servicio, ¿qué le pasa a usted? Todo se arreglará con el %s.",
	u"Los pendientes, no van a aparecer, se los ha llevado esa chica. Tu número de la suerte: %s.",
	u"Mi tercer ojo de la percepción percibe percebes y tu número de la suerte, el %s."
	u"Pide al universo que se potencie y apunta tu número de la suerte: %s.",
	u"Enciende siete velas amarillas y ponlas por toda la casa con el número %s en cada vela.",
	u"Sandro Rey afirma, no pregunta, te veo desde mi tercer ojo y veo tu número de la suerte: %s.",
	u"Usted conoce a alguien llamado Juan. Predicciones exactas, su número de la suerte es %s.",
	u"Los ángeles me comunican que usted tiene conexión a Internet. Predicciones exactas, nº %s.",
	u"Hay un McDonalds en su ciudad, predicciones exactas. Su número de la suerte: %s.",
	u"A usted le cuesta mucho afeitarse, predicciones exactas. Su número de la suerte: %s.",
	u"Escúchame lo que le voy a decir, su ilusión era haber tenido una granja. Su número: %s.",
	u"Me estoy quedando sin maná, pero siempre me queda un poco para darte tu número, el %s.",
	u"Noche de predicciones, mi percepción percibe percebes y tu número de la suerte: %s.",
	u"Los planetas están alineados, Venus me ha tweeteado su número de la suerte, el %s.",
	u"Veo que la espalda la tiene usted mal con el lumbar. Su número de la suerte es el %s.",
	u"Sandro Rey a su servicio, un hombre le acompaña a usted. Apunte su número de la suerte: %s.",
	u"Que no te suene no significa que no sea cierto, toma tu número de la suerte: %s.",
	u"Diga que sí señora, que es usted muy guapa, apunta rápido tu número de la suerte: %s.",
	u"Si quieres abrir puertas interdimensionales, hazlo con precaución. Tu número es el %s.",
	u"La gente es como si te chupara la energía, te sientes como cansado. Apuesta por el %s.",
	u"Aquí su número de la suerte, el %s. Hemos repartido 9 millones en Palencia.",
	u"Durante muchos años he demostrado ser un profesional en TV, su número de la suerte: %s.",
	u"Estás en directo conmigo. Estás preocupada por el trabajo, ¿verdad? Su número: %s.",
	u"No abras puertas interdimensionales sin ayuda de un experto como yo. Toma tu número, el %s.",
	u"Noto una fuerte energía en ti, debes fluirla de forma adecuada y el nº %s te va a ayudar.",
	u"En tu caso lo veo claro, tu número es el %s. Apúntalo cariño y a seguir así de guapa.",
	u"Conoces a alguien a quien le gusta el chocolate. ¡Predicciones exactas! Y tu nº es el %s.",
	u"Hoy por la calle has visto un coche negro. ¡Predicciones exactas! Y tu número es el %s.",
	u"Esta señora me dice no a todo y así no se puede predecir nada. Le doy su nº señora, %s.",
	u"Por el poder del pentagrama, hexagrama, septagrama y tetragrammaton obtengo su número: %s.",
	u"Por el ojo de Horus, que el símbolo te proteja de los Zubat de la cueva celeste. Su nº: %s.",
	u"Soy un vidente internacional, el otro día predije la victoria a Chuck Norris. Tu nº es %s.",
	u"Gracias a mis números de la suerte la lotería ya no tiene emoción. Compra el número %s.",
	u"Se me pasa muy rápido la noche, las noches son cortas. Cariño tu número es el %s. Guapa.",
	u"Conecta conmigo, fruto de esa conexión saldrá tu número de la suerte. Veo que es el %s.",
	u"Te estoy viendo un espíritu, es transparente con toques grisáceos. También veo tu nº: %s.",
	u"Hay un espíritu al lado tuyo, ah, que es tu novio, pues que apunte su nº de la suerte: %s.",
	u"Soy el descendiente de los Anunakis, en este día de ascensión tu número es el %s.",
	u"Los segadores nos recolectarán a todos, pero tu número de la suerte te salvará, es el %s.",
	u"Se acaban las consultas gratuitas de pago con visa, aprovechad. Toma tu nº de la suerte: %s.",
	u"Vas a conocer a alguien nuevo. Predicciones exactas y tu número de la suerte es el %s.",
	u"Mira Paco, he tirado tus cartas y me sale el mundo y la luna. Tu nº es el %s. Un beso de luz.",
	u"He leído las cartas, órdago a grande. Aprovecho para darte tu número de la suerte: %s.",
	u"Para combatir contra los reptilianos Sandro te da el número %s, te dará suerte.",
	u"Estoy ayudando a muchas personas y mis predicciones se confirman. Tú número de la suerte: %s.",
	u"Yo perfecto no soy, de 100 predicciones puedo fallar en 2. Tu número de la suerte es el %s.",
	u"En el nombre del padre, del hijo y del pájaro del Twitter, el %s es tu número de la suerte.",
	u"El %s es tu número de la suerte. Es personal, no lo compartas con nadie, es astral.",
	u"El %s es tu número de la suerte. Si lo compartes con alguien y echas la lotería, no va a tocar.",
	u"Conecto contigo y lo veo absolutamente todo, afirmo la información que te da. Tu nº es %s.",
	u"Te hablo con palabras y con información muy certera. Nací con el don de la videncia. Tu nº: %s.",
	u"Escuche atentamente, concéntrese: %s. Ese es su número de la suerte. Conecto contigo amiga.",
	u"Ese juicio lo vas a perder, no te puedo engañar. Pero el nº de la suerte te dará dinero: %s.",
	u"Yo no me invento absolutamente nada, no vendo humo, vendo realidades. Tu nº de la suerte: %s.",
	u"No pronuncio palabras que se lleva el viento, te doy la ayuda directa a tu problema. Nº: %s.",
	u"¿Verdad que no ha tenido que esperar usted absolutamente nada? Su nº de la suerte es el %s.",
	u"Quiero hablar con toda España y que me paséis todas las llamadas. Tu nº de la suerte: %s.",
	u"Es muy fácil decir se ha ido con otra. Esa otra le da el cariño que tu no le das. Tu nº: %s.",
	u"Veo problemas de economía, pero tranquila, con este número %s que te he dado todo solucionado.",
	u"Por favor no invoque espíritus sin la presencia de un adulto. Tu número de la suerte es el %s.",
	u"Hay poderes interestelares que no llegáis a comprender, de ahí sale tu nº de la suerte: %s.",
	u"Este es tu número de la suerte personal que está dentro de la baraja del tarot, el %s.",
	u"Las larvas astrales que se quedan pegadas en el universo a las personas dan tu número: %s",
	u"9 millones de euros en la administración 6 de Palencia han tocado, es mucho dinero. Tu nº: %s.",
	u"En ningún programa esotérico encontraréis tanta rentabilidad. Tu número de la suerte es el %s.",
	u"(Música de piratas del caribe de fondo sin pagar derechos) Tu número de la suerte cariño: %s.",
	u"Atraigo el dinero a tu vida, lo sabe toda España, comparto contigo tu número de la suerte: %s",
	u"Claro que sí señora, faltaría más. Para usted el número de la suerte es el %s.",
	u"Aquí tengo el cambio de su destino, la felicidad suya y de su familia, el %s es tu número.",
	u"No te compensa dejar de fumar para un año de vida que te queda. Tu número de la suerte: %s.",
	u"Yo le pido a la energía de Don Juan del dinero, que te entre dinero. Tu número es el %s.",
]

# Words list that you will query to the Twitter API
queries = [
	u"@SoySandroRey",
	u"Sandro Rey",
]

# Bot's Twitter account name
bot_account = u"SoySandroRey"

# FILL THIS WITH YOUR PERSONAL TWITTER API KEYS
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


def main():
	# Twitter client for searching
	twitter = Twitter(domain = 'search.twitter.com')
	twitter.uriparts = ()
	
	# Getting the last id replied (for not answering the same accounts)
	f = open("lastids")
	last_id_replied = f.readline().replace('\n','')
	f.close()


	# Twitter client for posting
	poster = Twitter(
		auth = OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET),
		secure = True,
		api_version = '1',
		domain = 'api.twitter.com')

# --- Uncomment the following code lines (and fix them) if you don't want to set up a cron job
	# while True:
	
	# Queries:
	for query in queries:
		last_id_replied = twitter_search(query, last_id_replied, twitter, poster)

	f = open("lastids", "w")
	f.write(last_id_replied + '\n')
	f.close()
		# 
		# if len(sys.argv) > 1:			
		# 	try:
		# 		print 'Now sleeping '+sys.argv[1]+' seconds (user config)... \n'
		# 		time.sleep(int(sys.argv[1]))
		# 	except TypeError:
		# 		print "TypeError, sleeping 300 seconds (default)"
		# 		time.sleep(300) # Every 10 minutes
		# else:
		# 	print 'Now sleeping'+sys.argv[1]+' seconds (default)... \n'
		# 	time.sleep(300) # Every 10 minutes
# --- End


def random_message():
	lucky_number = str(random.randint(10000, 99999)).encode('utf8')
	message = random.choice(sandro_reply)
	try:
		message = message % lucky_number
	except TypeError:
		message = u"Apunta tu número de la suerte, el "+lucky_number+". Me equivoco como cualquiera pero no miento."
	return message + byebye
	

def twitter_search(query_string, last_id, twitter, poster):
	id = ''
	results = twitter.search(q = query_string, since_id = last_id)['results']

	if not results:
		print '* No results this time...'
		return last_id
	
	users = []
	for result in results:		
		message = result['text']
		user = result['from_user']
		# For avoiding replying twice
		if (user in users) or (user == bot_account) or message[0:16] == "RT @" + bot_account or message[0:14] == "@" + bot_account + ":":
			print "* User already replied or same user"
			break;
		else :
			users.append(user)
		id = str(result['id'])
		if id > last_id : # Always give the greater id
			last_id = id
		# print ">>>>" + user + " - " + message

		# We append part of the ID to avoid duplicates.
		try:
			response_string = random_message()
			msg = '@%s %s' % (user, response_string)
			# print '====> Resp = %s | Id = %s' % (msg, last_id)
			poster.statuses.update(status = msg, in_reply_to_status_id = result['id'])
		except TwitterError, TwitterHTTPError:
			print 'Error connecting to the Twitter API'
			pass

	return last_id
	
	
main()