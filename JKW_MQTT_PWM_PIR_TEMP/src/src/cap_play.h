#ifndef play_h
#define play_h

#include "main.h"
#include "i2s.h"
#include <WiFiUdp.h>


// avconv -i Downloads/Madonna\ -\ Hung\ Up\ www.my-free-mp3.net\ .mp3 -f s32be -acodec pcm_u16be -ac 1 -ar 44100 tcp://192.168.2.27:5522
// avconv -i https://c1icy.prod.playlists.ihrhls.com/2281_icy -f s32be -acodec pcm_u16be -ac 1 -ar 44000 tcp://192.168.2.27:5522

// I2S_LRS -  GPIO 02
// I2S_BCLK - GPIO 15
// I2S_DIN -  GPIO 03
// Enable -   GPIO 14

// valid buffer Sizes are e.g. 0x1000, 0x2000, 0x4000
#define BUFFER_SIZE    	0x4000 // 4k, 8k, 16k byte
#define AMP_ENABLE_PIN 	14 // D5
#define PLAY_PORT 			5523
static constexpr char MQTT_play_TOPIC[]           = "play";         // publish
static constexpr char MQTT_play_VOL_TOPIC[]           = "play_vol";         // publish


class play : public peripheral {
	public:
		play();
		~play();
		bool init();
		bool loop();
		bool loop_tcp();
		bool intervall_update(uint8_t slot);
		bool subscribe();
		bool parse(uint8_t* config);
		uint8_t count_intervall_update();
		bool receive(uint8_t* p_topic, uint8_t* p_payload);
		bool publish();
		uint8_t* get_key();
	private:
		WiFiUDP *udp_server;

		uint8_t *buffer8b;
		uint16_t bufferPtrIn;
		uint16_t bufferPtrIn2;
		uint16_t bufferPtrOut;
		uint16_t bufferPtrOut2;
		uint32_t ultimeout;
		uint8_t bit_mode;
		uint16_t samples_played;
		bool connected;
		bool run_noninterrupted;
		uint32_t last_call;

		uint8_t gainF2P6; // Fixed point 2.6
		//typedef int32_t fixed24p8_t;
		void shutdown();
		int16_t Amplify(int16_t s);
		bool SetGain(float f);

		uint8_t key[3];
};


#endif