#include <cap_PWM.h>
#ifdef WITH_PWM

PWM::PWM(uint8_t* k, uint8_t pin0,uint8_t pin1, uint8_t pin2, uint8_t pin3, uint8_t pin4){
	m_pins[0] = pin0;
	m_pins[1] = pin1;
	m_pins[2] = pin2;
	m_pins[3] = pin3;
	m_pins[4] = pin4;
	sprintf((char*)key,(char*)k);
};

PWM::~PWM(){
	uint8_t buffer[15];
	sprintf((char*)buffer,"%s deleted",get_key());
	logger.println(TOPIC_GENERIC_INFO, (char*)buffer, COLOR_YELLOW);
};

uint8_t* PWM::get_key(){
	return key;
}

uint8_t* PWM::get_dep(){
	return (uint8_t*)"LIG";
}

bool PWM::parse(uint8_t* config){
	return cap.parse(config,get_key(),get_dep());
}

bool PWM::init(){
	pinMode(m_pins[0], OUTPUT);
	pinMode(m_pins[1], OUTPUT);
	pinMode(m_pins[2], OUTPUT);
	if(m_pins[3]){
		pinMode(m_pins[3], OUTPUT);
	}
	if(m_pins[4]){
		pinMode(m_pins[4], OUTPUT);
	}
	analogWriteRange(255);
	sprintf(m_msg_buffer,"%s init, pin config %i,%i,%i,%i,%i",get_key(),m_pins[0],m_pins[1],m_pins[2],m_pins[3],m_pins[4]);
	logger.println(TOPIC_GENERIC_INFO, m_msg_buffer, COLOR_GREEN);
}


// bool PWM::loop(){
// 	return false;
// }
//
// bool PWM::intervall_update(uint8_t slot){
// 	return false;
// }
//
// bool PWM::subscribe(){
// 	return true;
// }
//
// bool PWM::receive(uint8_t* p_topic, uint8_t* p_payload){
// 	return false;
// }

uint8_t PWM::getState(led* color){
	color->r = m_light_current.r;
	color->g = m_light_current.g;
	color->b = m_light_current.b;
	return m_state.get_value();
}

void PWM::setState(uint8_t value){
	m_state.set(value);
}

bool PWM::publish(){
	// function called to publish the state of the PWM (on/off)
	return false;
}

void PWM::setColor(uint8_t r, uint8_t g, uint8_t b){
	// make sure that we never have a brightness of zero when we're switched on
	// rather set it to full brightness then to have it auto-off again
	//if (m_state.get_value() && r == 0) {
	//	r = sizeof(intens) - 1;
	//}
	analogWrite(m_pins[0], r);
	analogWrite(m_pins[1], g);
	analogWrite(m_pins[2], b);

	if(m_pins[3]){
		analogWrite(m_pins[3], r);
	}
	if(m_pins[4]){
		analogWrite(m_pins[4], r);
	}

	logger.print(TOPIC_INFO_PWM, F("PWM: "));
	snprintf(m_msg_buffer, MSG_BUFFER_SIZE, "%d,%d,%d", r, g, b);
	logger.pln(m_msg_buffer);
} // setState

#endif
