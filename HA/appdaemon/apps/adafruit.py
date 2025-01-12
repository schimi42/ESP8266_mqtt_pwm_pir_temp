import appdaemon.plugins.hass.hassapi as hass
import datetime, time
import urllib.request


#
# Hellow World App
#
# Args:
#

class AdafruitWorld(hass.Hass):

	def initialize(self):
		self.log("Starting Adafruit Service")
		self.listen_state(self.start,"sensor.adafruit")

	def roundshot(self, url, msg):
		try:
			self.log("downloading "+url)
			fn = "/tmp/ad_tmp.jpg"
			urllib.request.urlretrieve(url, fn)
			self.log("sending")
			self.call_service("notify/pb", data={"file": fn}, message=msg)
		except:
			pass


	def start(self, entity, attribute, old, new,kwargs):
		new = new.lower()
		self.log("New Adafruit input: "+new)

		if(new=="amplifier aus" or new=="tv aus"):
			self.turn_on("script.tvoff")
		if(new=="amplifier an" or new=="tv an"):
			self.turn_on("script.start_chromaudio")
		elif(new=="livingroom an"):
			self.turn_on("light.joiner_livingroom")
		elif(new=="livingroom aus"):
			self.turn_off("light.joiner_livingroom")
		elif(new=="kitchen an"):
			self.turn_on("light.joiner_kitchen")
		elif(new=="kitchen aus"):
			self.turn_off("light.joiner_kitchen")
		elif(new=="spotcleanup"):
			self.call_service("vacuum/clean_spot", entity_id="vacuum.xiaomi_vacuum_cleaner")
		elif(new=="esszimmer"):
			self.turn_on("script.vacuum_kitchen")
		elif(new=="wir_gehen_schlafen"):
			self.turn_off("light.joiner_livingroom")
			self.turn_off("light.joiner_kitchen")
			self.turn_off("light.dev18")
			self.turn_off("light.dev22")
			self.turn_on("script.tvoff")
			self.turn_on("light.dev54_2")
			self.turn_on("light.dev12")
			self.turn_on("light.dev15")
		elif(new=="garage"):
			self.turn_on("light.dev8")
		elif(new=="roundshot"):
			self.log("roundshot!")
			self.roundshot("http://192.168.2.53/snapshot.jpg","Roundshot 3")
			self.roundshot("http://192.168.2.43/snapshot.jpg","Roundshot 4")
			self.roundshot("http://192.168.2.45/snapshot.jpg","Roundshot 5")
			self.roundshot("http://192.168.2.56/snapshot.jpg","Roundshot 6")
		elif(new=="0"):
			self.log("ignore 0")
		else:
			self.log(":( no handle found for "+new)
		self.set_state("sensor.adafruit",state="0")


