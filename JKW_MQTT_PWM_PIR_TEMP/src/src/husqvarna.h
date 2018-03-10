#ifndef husqvarna_h
	#define husqvarna_h


#include "main.h"
#include "../lib/softserial/SoftwareSerial.h"

	#define CMD_PROGRAMMING       0
	#define CMD_BLADE_RPM         1
	#define CMD_REQUEST_STATUS    2
	#define CMD_CAPACITY          3
	#define CMD_TEMP              4
	#define CMD_TIME_SINCE_CHARGE 5
	#define CMD_YES_KEY           6
	#define CMD_VOLTAGE           7
	#define CMD_MODE              8

	static constexpr char MQTT_HUSQVARNA_MODE_TOPIC[]            = "husqvarna_mode";     // publish
	static constexpr char MQTT_HUSQVARNA_STATUS_TOPIC[]          = "husqvarna_status";   // publish
	static constexpr char MQTT_HUSQVARNA_BATTERY_CAP_TOPIC[]     = "husqvarna_bat_cap";  // publish
	static constexpr char MQTT_HUSQVARNA_BATTERY_TEMP_TOPIC[]    = "husqvarna_bat_temp"; // publish
	static constexpr char MQTT_HUSQVARNA_BATTERY_TIME_TOPIC[]    = "husqvarna_bat_time"; // publish
	static constexpr char MQTT_HUSQVARNA_BATTERY_VOLTAGE_TOPIC[] = "husqvarna_bat_volt"; // publish

	static constexpr uint8_t time_programming_cmd[5] = { 0x0F, 0x00, 0x38, 0x00, 0x00 }; // maehzeit
	static constexpr uint8_t blade_rpm_cmp[5] = { 0x0F, 0x00, 0x4D, 0x00, 0x00 };
	static constexpr uint8_t request_status_cmd[5] = { 0x0F, 0x01, 0xF1, 0x00, 0x00 };
	static constexpr uint8_t battery_capacity_cmd[5] = { 0x0F, 0x01, 0xF0, 0x00, 0x00 };
	static constexpr uint8_t battery_temp_cmd[5] = { 0x0F, 0x02, 0x33, 0x00, 0x00 };
	static constexpr uint8_t time_since_charging_cmd[5] = { 0x0F, 0x02, 0x34, 0x00, 0x00 };
	static constexpr uint8_t yes_key_cmd[5] = { 0x0F, 0x80, 0x5F, 0x00, 0x12 };
	static constexpr uint8_t manuell_mode_cmd[5] = { 0x0F, 0x81, 0x2C, 0x00, 0x00 };
	static constexpr uint8_t auto_mode_cmd[5] = { 0x0F, 0x81, 0x2C, 0x00, 0x01 };
	static constexpr uint8_t goHome_cmd[5] = { 0x0F, 0x81, 0x2C, 0x00, 0x03 };
	static constexpr uint8_t battery_voltage_cmd[5] = { 0x0F, 0x2E, 0xF4, 0x00, 0x00 };

	class husqvarna : public peripheral {
public:
		husqvarna();
		~husqvarna();
		bool init();
		bool loop();
		void interrupt();
		bool intervall_update(uint8_t slot);
		bool subscribe();
		uint8_t count_intervall_update();
		bool receive(uint8_t * p_topic, uint8_t * p_payload);
		bool parse(uint8_t * config);
		uint8_t * get_key();
		bool publish();
private:
		void send_cmd(uint8_t * cmd);
		mqtt_parameter_8 m_last_cmd;
		uint8_t * last_command_send;
		mqtt_parameter_32 m_state;
		uint32_t last_received;
		uint8_t key[4];
		uint8_t minute_counter;
		uint8_t response[5] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF }; // Resultat leer initialisieren
		SoftwareSerial * swSer1;
	};


#endif // ifndef husqvarna_h
