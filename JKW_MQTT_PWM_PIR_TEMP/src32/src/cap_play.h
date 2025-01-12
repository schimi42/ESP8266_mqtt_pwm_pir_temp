#ifndef play_h
#define play_h

#include "main.h"
#ifdef ESP32
  #include "driver/i2s.h"
#else
	#include "i2s.h"
#endif
//#include <WiFiUdp.h>


// avconv -i Downloads/Madonna\ -\ Hung\ Up\ www.my-free-mp3.net\ .mp3 -f s32be -acodec pcm_u16be -ac 1 -ar 44100 tcp://192.168.2.27:5522
// avconv -i https://c1icy.prod.playlists.ihrhls.com/2281_icy -f s32be -acodec pcm_u16be -ac 1 -ar 44000 tcp://192.168.2.27:5522

// I2S_LRS -  GPIO 02 / D4
// I2S_BCLK - GPIO 15 / D8
// I2S_DOUT - GPIO 03 / D9 / RX
// Enable -   GPIO 14 / D5

// valid buffer Sizes are e.g. 0x1000, 0x2000, 0x4000
#define BUFFER_SIZE    	0x4000 // 4k, 8k, 16k byte
#define AMP_ENABLE_PIN 	14 // D5
#define PLAY_PORT 			5523
static constexpr char MQTT_play_TOPIC[]           = "play";         // publish
static constexpr char MQTT_play_VOL_TOPIC[]           = "play_vol";         // publish
static constexpr char MQTT_play_SR_TOPIC[]           = "play_sr";         // publish


class play : public capability {
	public:
		play();
		~play();
		bool init();
		bool loop();
		bool loop_tcp();
		// bool intervall_update(uint8_t slot);
		bool subscribe();
		bool parse(uint8_t* config);
		bool receive(uint8_t* p_topic, uint8_t* p_payload);
		// bool publish();
		uint8_t* get_key();
		void coreTask( void * pvParameters );
	private:
		//WiFiUDP *udp_server;
		WiFiServer *tcp_server;
		WiFiClient tcp_socket;

		enum : uint8_t { APLL_AUTO = 255, APLL_ENABLE = 1, APLL_DISABLE = 0 };
    enum : uint8_t { EXTERNAL_I2S = 0, INTERNAL_DAC = 1, INTERNAL_PDM = 2 };

		uint8_t *buffer8b;
		uint16_t bufferPtrIn;
		uint16_t bufferPtrOut;
		uint32_t ultimeout;
		uint32_t last_data_in;
		uint8_t bit_mode;
		bool client_connected;
		bool amp_active;
		bool i2s_active;
		bool run_noninterrupted;
		uint32_t last_call;

		uint32_t sample_played_timer;
		uint32_t sample_played;
		uint32_t sample_nplayed;

		uint8_t gainF2P6; // Fixed point 2.6
		//typedef int32_t fixed24p8_t;
		void power_amp(bool status);
		bool SetRate(int hz);
		int16_t Amplify(int16_t s);
		bool SetGain(float f);
		void handle_client_disconnect();
};


#endif
