import math
import appdaemon.plugins.hass.hassapi as hass
import datetime, time
from threading import Timer


class GmotionWorld(hass.Hass):

	def initialize(self):
		self.log("Starting gmotion Service")
		self.listen_state(self.home, "device_tracker.illuminum_caro", new = "home", duration = 10*60, arg1="Caro home")  # everyone is home for 10 min
		self.listen_state(self.home, "device_tracker.illuminum_kolja", new = "home", duration = 10*60, arg1="Kolja home")  # everyone is home for 10 min
		self.sensor = ["6_motion", "8_motion", "15_motion", "54_motion_1", "54_motion_2", "57_motion"]
		self.sensor_name = ["Cellar", "Garage", "World map", "Entrace", "Entrace_cellar", "Floor upstairs"]
		self.sensor_trigger_count = []
		self.sensor_trigger_count_reported = []
		for i in range(0,len(self.sensor)):
			self.listen_state(self.motion, "binary_sensor.dev"+self.sensor[i])
			self.sensor_trigger_count_reported.append(0)
			self.sensor_trigger_count.append(0)
		self.msg_delay = [0,3*60,8*60,15*60]
		self.msg_ts = 0
		self.msg_nr = 0

		self.motion("","","","","")
		self.home("","","","","")


	def home(self, entity, attribute, old, new, kwargs):
		if(self.get_state("device_tracker.illuminum_caro") == "not_home" and self.get_state("device_tracker.illuminum_kolja") == "not_home"):
			self.sensor_trigger_count = []
			self.sensor_trigger_count_reported = []
			for i in range(0,len(self.sensor)):
				self.sensor_trigger_count.append(0)
				self.sensor_trigger_count_reported.append(0)


	def motion(self, entity, attribute, old, new, kwargs):
		#self.log("check motion")
		m = False
		for i in range(0,len(self.sensor)):
			#self.log("binary_sensor.dev"+self.sensor[i]+": "+self.get_state("binary_sensor.dev"+self.sensor[i]))
			if(self.get_state("binary_sensor.dev"+self.sensor[i]) == "on"):
				m = True
				self.sensor_trigger_count[i] = self.sensor_trigger_count[i]+1
		if(not(m)):
			 #self.log("gmotion "+entity)
			 self.set_state("binary_sensor.g_motion",state="off")
		else:
			self.set_state("binary_sensor.g_motion",state="on")
			self.safety()


	def safety(self, kwargs=""):
		#self.log("check safety")
		if(not(self.get_state("input_boolean.alarm_system") == "on")):
			#self.log("Safety disabled, quitting")
			return 0

		changes = False
		for i in range(0,len(self.sensor)):
			if(not(self.sensor_trigger_count_reported[i]==self.sensor_trigger_count[i])):
				changes = True

		if(not(changes)):
			#self.log("no new alarm counts, exiting")
			return 0

		#self.log("call safety")
		## ok, we have some motion, what to do?
		## 1. check if someone is home, if so, ignore it for the safety function
		##    if not, check if the vacuum is cleaning (more states needed?)
		## 2. if the vac is not cleaning and no one is home, send a message that includes:
		## 2.1. The sensor that triggered and their trigger count
		## 2.2. the vacuum status
		## 2.3. the distance of us towards home
		# 1.

		if(self.get_state("device_tracker.illuminum_caro") == "not_home" and self.get_state("device_tracker.illuminum_kolja") == "not_home"):
			# 2.
			vac = self.get_state("vacuum.xiaomi_vacuum_cleaner")
			vac2 = self.get_state("vacuum.xiaomi_vacuum_cleaner_2")
			if(not(vac in ["cleaning", "returning"]) and not(vac in ["cleaning", "returning"])):
				# 2.1.
				#self.log("motion and no-one home and vacuum not cleaning")
				if(time.time() - self.msg_ts >= self.msg_delay[self.msg_nr]):
					self.msg_ts = time.time()
					if(self.msg_nr == 0):
						msg = "Hi, there is some motion at home, "
					elif(self.msg_nr < 4):
						msg = "Hi, there is still something going on, "

					msg += "Sensors: " 
					for i in range(0,len(self.sensor)):
						if(self.sensor_trigger_count[i] - self.sensor_trigger_count_reported[i]>0):
							msg +=self.sensor_name[i]+" ("+str(self.sensor_trigger_count[i] - self.sensor_trigger_count_reported[i])+"x) "
					msg += ". Distances: "
					msg +="Kolja ("+str(self.distance("device_tracker.illuminum_kolja"))+") "
					msg +="Caro ("+str(self.distance("device_tracker.illuminum_caro"))+") "
					msg +="Vacuum status: "+self.get_state("vacuum.xiaomi_vacuum_cleaner")


					self.log(msg)
					self.call_service("notify/pb", title="Motion alert", message=msg)

					if(self.msg_nr +1 < len(self.sensor)):
						self.msg_nr = self.msg_nr +1


				#else:
				#	self.log("have to wait further "+str(self.msg_delay[self.msg_nr]-(time.time()-self.msg_ts))+" sec")
				# call me again in 30 sec
			#else:
			#	self.log("vacuum running")
			self.handle = self.run_in(self.safety,seconds=10)
		else:
			#self.log("someone is home, resetting counters")
			if(self.msg_nr>0):
				self.msg_nr = 0

				msg = "Issue solved, "
				if(self.get_state("device_tracker.illuminum_caro") == "home"):
					msg = "Caro "
				elif(self.get_state("device_tracker.illuminum_kolja") == "home"):
					msg = "Kolja "
				msg += "is home now"
				self.log(msg)
				self.call_service("notify/pb", title="Motion alert", message=msg)

				self.sensor_trigger_count = []
				self.sensor_trigger_count_reported = []
				for i in range(0,len(self.sensor)):
					self.sensor_trigger_count.append(0)
					self.sensor_trigger_count_reported.append(0)

		for i in range(0,len(self.sensor)):
			self.sensor_trigger_count_reported[i]=self.sensor_trigger_count[i]



	def distance(self,d):
		d = self.get_state(d,attribute="all")["attributes"]
		lat1 = d["latitude"]
		lon1 = d["longitude"]

		h = self.get_state("zone.home",attribute="all")["attributes"]
		lat2 = h["latitude"]
		lon2 = h["longitude"]

		radius = 6371  # km
		dlat = math.radians(lat2 - lat1)
		dlon = math.radians(lon2 - lon1)
		a = (math.sin(dlat / 2) * math.sin(dlat / 2) +  math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2))
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		d = radius * c
		d = round(d,2)
		return d

