/* Edge Impulse ingestion SDK
 * Copyright (c) 2022 EdgeImpulse Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

/* Includes ---------------------------------------------------------------- */
#include <ngoc_lam-project-1_inferencing.h>
#include <Arduino_LSM6DSOX.h> //Click here to get the library: http://librarymanager/All#Arduino_LSM6DSOX
#include "PluggableUSBHID.h"
#include "USBMouse.h"
#include <ezButton.h>
#include <SPI.h>
#include <WiFiNINA.h>

enum sensor_status {
    NOT_USED = -1,
    NOT_INIT,
    INIT,
    SAMPLED
};

/** Struct to link sensor axis name to sensor value function */
typedef struct{
    const char *name;
    float *value;
    uint8_t (*poll_sensor)(void);
    bool (*init_sensor)(void);
    int8_t status;  // -1 not used 0 used(unitialized) 1 used(initalized) 2 data sampled
} eiSensors;

/* Constant defines -------------------------------------------------------- */
#define CONVERT_G_TO_MS2    9.80665f
#define MAX_ACCEPTED_RANGE  4.0f        // starting 03/2022, models are generated setting range to +-2,
                                        // but this example use Arudino library which set range to +-4g.
                                        // If you are using an older model, ignore this value and use 4.0f instead
/** Number sensor axes used */
#define N_SENSORS     6

// Initialize mouse object
USBMouse Mouse;

/* Forward declarations ------------------------------------------------------- */
float ei_get_sign(float number);
static bool ei_connect_fusion_list(const char *input_list);

bool init_IMU(void);
uint8_t poll_acc(void);
uint8_t poll_gyr(void);

/* Private variables ------------------------------------------------------- */
static const bool debug_nn = false; // Set this to true to see e.g. features generated from the raw signal
static float data[N_SENSORS];
static int8_t fusion_sensors[N_SENSORS];
static int fusion_ix = 0;

// mouse coordinate configuration
const	float	gyr_OFST_Y = 0.5;
const	float	gyr_OFST_Z = 0.5;
const	float	air_SENS = 1.;				// air: sensitivity (1~256 times)
float dx,dy;

// classification threshold
float threshold = 0.7;

// wifi configuration
char ssid[] = "EZI Coffee";          //  your network SSID (name)
char pass[] = "74phandangluu";   // your network password

int status = WL_IDLE_STATUS;
char servername[]="127.0.0.1";  // remote server we will connect to

WiFiUDP Udp;
unsigned int localUdpPort = 42000;

// button configuration
ezButton button(7);  // create ezButton object that attach to pin 7;

String queryStr;

/** Used sensors value function connected to label name */
eiSensors sensors[] =
{
    "ax", &data[0], &poll_acc, &init_IMU, NOT_USED,
    "ay", &data[1], &poll_acc, &init_IMU, NOT_USED,
    "az", &data[2], &poll_acc, &init_IMU, NOT_USED,
    "gx", &data[3], &poll_gyr, &init_IMU, NOT_USED,
    "gy", &data[4], &poll_gyr, &init_IMU, NOT_USED,
    "gz", &data[5], &poll_gyr, &init_IMU, NOT_USED,
};

/**
* @brief      Arduino setup function
*/
void setup()
{
  /* Init serial */
  Serial.begin(115200);
  // comment out the below line to cancel the wait for USB connection (needed for native USB)
  while (!Serial);

  /* set up for wifi */
  Serial.println("Wifi setup");
  status = WiFi.begin(ssid, pass);
  if (status != WL_CONNECTED) {
    Serial.println("Couldn't get a WiFi connection");
    // don't do anything else:
    while(true);
  }

  /* set up for button */
  Serial.println("Button setup");
  button.setDebounceTime(50); // set debounce time to 50 milliseconds


  Serial.println("Edge Impulse Sensor Fusion Inference\r\n");
  /* Connect used sensors */
  if(ei_connect_fusion_list("ax + ay + az + gx + gy + gz") == false) {
      ei_printf("ERR: Errors in sensor list detected\r\n");
      return;
  }

  /* Init & start sensors */
  for(int i = 0; i < fusion_ix; i++) {
    if (sensors[fusion_sensors[i]].status == NOT_INIT) {
      sensors[fusion_sensors[i]].status = (sensor_status)sensors[fusion_sensors[i]].init_sensor();
      if (!sensors[fusion_sensors[i]].status) {
        ei_printf("%s axis sensor initialization failed.\r\n", sensors[fusion_sensors[i]].name);
      }
      else {
        ei_printf("%s axis sensor initialization successful.\r\n", sensors[fusion_sensors[i]].name);
      }
    }
  }
  Udp.begin(localUdpPort);
}

/**
* @brief      Get data and run inferencing
*/
void loop()
{ 
  button.loop(); // MUST call the loop() function first
  if (button.isPressed()){
    return;
  }
  if(button.isReleased()){
    delayMicroseconds(150);
    if (EI_CLASSIFIER_RAW_SAMPLES_PER_FRAME != fusion_ix) {
        ei_printf("ERR: Sensors don't match the sensors required in the model\r\n"
        "Following sensors are required: %s\r\n", EI_CLASSIFIER_FUSION_AXES_STRING);
        return;
    }

    ei_printf("Sampling...\r\n");

    // Allocate a buffer here for the values we'll read from the sensor
    float buffer[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE] = { 0 };

    for (size_t ix = 0; ix < EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE; ix += EI_CLASSIFIER_RAW_SAMPLES_PER_FRAME) {
        // Determine the next tick (and then sleep later)
        int64_t next_tick = (int64_t)micros() + ((int64_t)EI_CLASSIFIER_INTERVAL_MS * 1000);

        for(int i = 0; i < fusion_ix; i++) {
            if (sensors[fusion_sensors[i]].status == INIT) {
                sensors[fusion_sensors[i]].poll_sensor();
                sensors[fusion_sensors[i]].status = SAMPLED;
            }
            if (sensors[fusion_sensors[i]].status == SAMPLED) {
              buffer[ix + i] = *sensors[fusion_sensors[i]].value;
              sensors[fusion_sensors[i]].status = INIT;
            }
        }
        int64_t wait_time = next_tick - (int64_t)micros();

        if(wait_time > 0) {
            delayMicroseconds(wait_time);
        }
    }
    Serial.println(1);
    // Turn the raw buffer in a signal which we can the classify
    signal_t signal;
    int err = numpy::signal_from_buffer(buffer, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
    if (err != 0) {
        ei_printf("ERR:(%d)\r\n", err);
        return;
    }

    // Run the classifier
    ei_impulse_result_t result = { 0 };

    err = run_classifier(&signal, &result, debug_nn);
    if (err != EI_IMPULSE_OK) {
        ei_printf("ERR:(%d)\r\n", err);
        return;
    }
    if (result.classification[0].value > threshold){
      queryStr = "click 0.0 0.0\n";
    } else if (result.classification[1].value > threshold){
      queryStr = "scroll_down 0.0 0.0\n";
    } else if (result.classification[2].value > threshold){
      queryStr = "scroll_up 0.0 0.0\n";
    } else {
      queryStr = "uncertain 0.0 0.0\n";
    }
    print_inference_result(result);
  } else {
    // report rate
    float	gyr_x;
    float	gyr_y;
    float	gyr_z;
    
    // read imu
    IMU.readGyroscope(gyr_x, gyr_y, gyr_z);

    dx = -(gyr_z - gyr_OFST_Z);
    dy = -(gyr_y - gyr_OFST_Y);

    dx = dx / (256. / air_SENS);
    dy = dy / (256. / air_SENS);

    dx = (dx < -128.) ? -128.: (dx > 127.) ? 127.: dx;
    dy = (dy < -128.) ? -128.: (dy > 127.)? 127.: dy;

    queryStr = String("move ") + String(dx) + " " + String(dy) + "\n";
    //Mouse.move(int(dx * 15.), int(dy * 15.));
  }

/*
  Udp.beginPacket("192.168.1.4", 20001);
  Udp.write(queryStr.c_str());
  Udp.endPacket();
  */
}

/**
 * @brief Go through sensor list to find matching axis name
 *
 * @param axis_name
 * @return int8_t index in sensor list, -1 if axis name is not found
 */
static int8_t ei_find_axis(char *axis_name)
{
    int ix;
    for(ix = 0; ix < N_SENSORS; ix++) {
        if(strstr(axis_name, sensors[ix].name)) {
            return ix;
        }
    }
    return -1;
}

/**
 * @brief Check if requested input list is valid sensor fusion, create sensor buffer
 *
 * @param[in]  input_list      Axes list to sample (ie. "accX + gyrY + magZ")
 * @retval  false if invalid sensor_list
 */
static bool ei_connect_fusion_list(const char *input_list)
{
    char *buff;
    bool is_fusion = false;

    /* Copy const string in heap mem */
    char *input_string = (char *)ei_malloc(strlen(input_list) + 1);
    if (input_string == NULL) {
        return false;
    }
    memset(input_string, 0, strlen(input_list) + 1);
    strncpy(input_string, input_list, strlen(input_list));

    /* Clear fusion sensor list */
    memset(fusion_sensors, 0, N_SENSORS);
    fusion_ix = 0;

    buff = strtok(input_string, "+");

    while (buff != NULL) { /* Run through buffer */
        int8_t found_axis = 0;

        is_fusion = false;
        found_axis = ei_find_axis(buff);

        if(found_axis >= 0) {
            if(fusion_ix < N_SENSORS) {
                fusion_sensors[fusion_ix++] = found_axis;
                sensors[found_axis].status = NOT_INIT;
            }
            is_fusion = true;
        }

        buff = strtok(NULL, "+ ");
    }

    ei_free(input_string);

    return is_fusion;
}

/**
 * @brief Return the sign of the number
 *
 * @param number
 * @return int 1 if positive (or 0) -1 if negative
 */
float ei_get_sign(float number) {
    return (number >= 0.0) ? 1.0 : -1.0;
}

bool init_IMU(void) {
  static bool init_status = false;
  if (!init_status) {
    init_status = IMU.begin();
  }
  return init_status;
}

uint8_t poll_acc(void) {

    if (IMU.accelerationAvailable()) {

      IMU.readAcceleration(data[0], data[1], data[2]);
      for (int i = 0; i < 3; i++) {
          if (fabs(data[i]) > MAX_ACCEPTED_RANGE) {
              data[i] = ei_get_sign(data[i]) * MAX_ACCEPTED_RANGE;
          }
      }

      data[0] /= 4.0;
      data[1] /= 4.0;
      data[2] /= 4.0;
      //data[0] *= CONVERT_G_TO_MS2;
      //data[1] *= CONVERT_G_TO_MS2;
      //data[2] *= CONVERT_G_TO_MS2;
    }

    return 0;
}

uint8_t poll_gyr(void) {

    if (IMU.gyroscopeAvailable()) {
        IMU.readGyroscope(data[3], data[4], data[5]);
        data[3] /= 2000.0;
        data[4] /= 2000.0;
        data[5] /= 2000.0;
    }
    return 0;
}

void print_inference_result(ei_impulse_result_t result) {

    // Print how long it took to perform inference
    ei_printf("Timing: DSP %d ms, inference %d ms, anomaly %d ms\r\n",
            result.timing.dsp,
            result.timing.classification,
            result.timing.anomaly);

    ei_printf("Predictions:\r\n");
    for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
        ei_printf("  %s: ", ei_classifier_inferencing_categories[i]);
        ei_printf("%.5f\r\n", result.classification[i].value);
    }

    // Print anomaly result (if it exists)
#if EI_CLASSIFIER_HAS_ANOMALY == 1
    ei_printf("Anomaly prediction: %.3f\r\n", result.anomaly);
#endif

}

#if !defined(EI_CLASSIFIER_SENSOR) || (EI_CLASSIFIER_SENSOR != EI_CLASSIFIER_SENSOR_FUSION && EI_CLASSIFIER_SENSOR != EI_CLASSIFIER_SENSOR_ACCELEROMETER)
#error "Invalid model for current sensor"
#endif