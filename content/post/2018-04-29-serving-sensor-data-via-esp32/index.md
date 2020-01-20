---
title: Serving sensor data via ESP32
date: 2018-04-29 19:46:26
tags:
- c
- electronics
- esp32
- programming
- i2c
categories:
- electronics
---
[Previously](/2018/04/26/ESP32-reading-Si7102-temperature-and-humidity-data-via-I2C-bus/), I [wrote](/2018/04/26/ESP32-reading-Si7102-temperature-and-humidity-data-via-I2C-bus/) about using the [ESP32](http://www.esp32.net/) to read sensor data over I2C from the [Si7021](/2018/03/11/Reading-data-from-Si7021-temperature-and-humidity-sensor-using-Raspberry-Pi/Si7021-A20.pdf) temperature and humidity monitor. Today, I'm going to briefly take you through the process of serving this data via the web.

{{< figure src="images/process.png" title="Basic project setup" >}}

### Description

The project plan is to connect to WiFi in `STA` mode, collect temperature and humidity data every 5 seconds from a [Si7021](/2018/03/11/Reading-data-from-Si7021-temperature-and-humidity-sensor-using-Raspberry-Pi/Si7021-A20.pdf) sensor via the I2C bus. We will launch a web server and whenever we have a `GET/` request we'll serve a simple web page that reports the temperature and humidity. If the URL path is /h (e.g. 192.168.1.x/h) then we'll turn on an LED connected to GPIO 4. If the path is /l (e.g. 192.168.1.x/l) then we'll turn off the LED. In both latter cases, we'll also serve the same page showing the temperature and humidity.

Essentially, we have three tasks to consider:

- Read sensor data from the Si7021 over the I2C bus. We [covered this part](/2018/04/26/ESP32-reading-Si7102-temperature-and-humidity-data-via-I2C-bus/) previously; so I'll only say that we're using the same component and launching a periodic tasks to read the sensor.
- Connect to the WiFi network[ <i class="fa fa-arrow-circle-down" aria-hidden="true"></i>](#connectwifi)
- Configure and serve the web page incorporating the sensor data. [ <i class="fa fa-arrow-circle-down" aria-hidden="true"></i>](#webserver)

<!-- more -->

<a id="connectwifi"></a>
### Connecting to the WiFi network

We use the ESP-IDF framework to connect to the WiFi network. Since we aren't in control of the some of the steps in the process and cannot control how long certain parts of the process take, we use an event-driven interface to the WiFi driver. Otherwise, we would block the main program execution.

If you take a look at the [esp_event.h](https://github.com/espressif/esp-idf/blob/master/components/esp32/include/esp_event.h) file in the ESP-IDF framework, you'll see the enumeration for all of the types of events we may need to respond to during the process of connecting to the WiFi network. We won't need to respond to _every_ single event, but we'll handle several of them as you'll see in a moment.

{{< highlight c >}}
typedef enum {
    SYSTEM_EVENT_WIFI_READY = 0,           /**< ESP32 WiFi ready */
    SYSTEM_EVENT_SCAN_DONE,                /**< ESP32 finish scanning AP */
    SYSTEM_EVENT_STA_START,                /**< ESP32 station start */
    SYSTEM_EVENT_STA_STOP,                 /**< ESP32 station stop */
    SYSTEM_EVENT_STA_CONNECTED,            /**< ESP32 station connected to AP */
    SYSTEM_EVENT_STA_DISCONNECTED,         /**< ESP32 station disconnected from AP */
    SYSTEM_EVENT_STA_AUTHMODE_CHANGE,      /**< the auth mode of AP connected by ESP32 station changed */
    SYSTEM_EVENT_STA_GOT_IP,               /**< ESP32 station got IP from connected AP */

    /* several more constants in the esp_event.h file */
} system_event_id_t;
{{< /highlight >}}

How do we launch the process of connecting to WiFi? Here we encapsulate the WiFi initialization in the function `initialize_wifi`.

{{< highlight c >}}
//  wifi task flags
static EventGroupHandle_t wifi_event_group;
const int CONNECTED_BIT = BIT0;

static void initialise_wifi(void) {
    tcpip_adapter_init();
    wifi_event_group = xEventGroupCreate();
    ESP_ERROR_CHECK( esp_event_loop_init(event_handler, NULL) );
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK( esp_wifi_init(&cfg) );
    ESP_ERROR_CHECK( esp_wifi_set_storage(WIFI_STORAGE_RAM) );
    ESP_ERROR_CHECK( esp_wifi_set_mode(WIFI_MODE_STA) );
    wifi_config_t sta_config = {
        .sta = {
            .ssid = EXAMPLE_ESP_WIFI_SSID,
            .password = EXAMPLE_ESP_WIFI_PASS,
            .bssid_set = false
        }
    };
    ESP_ERROR_CHECK( esp_wifi_set_config(WIFI_IF_STA, &sta_config) );
    ESP_ERROR_CHECK( esp_wifi_start() );
}
{{< /highlight >}}

To initialise the WiFi, we must first initialise the TCP/IP adapter, creating an LwIP core task and begin LwIP related work.^[LwIP stands for _"Lightweight IP stack"_. In essence, it is a smaller implementation of a full TCP/IP stack. You can read more about this open source stack in the [lwIP 2.0 documentation.](http://www.nongnu.org/lwip/2_0_x/index.html).] Next we create an EventGroupHandle_t type which is an opaque data type that just holds connection flags that we'll set and check as needed to coordinate between tasks. Next in line 8 above, we initialize the wifi event loop handler.

Next we load default WiFi configuration parameters using the macro `WIFI_INIT_CONFIG_DEFAULT()`. The [ESP-IDF framework documentation](http://esp-idf.readthedocs.io/en/latest/api-reference/wifi/esp_wifi.html?highlight=wifi_storage_t) for the WiFi driver states that a) `WIFI_INIT_CONFIG_DEFAULT()` should always be used to initialize the driver with default values and b) `esp_wifi_init()` should be called before any other function in the WiFi driver API.

The function `esp_wifi_set_storage()` allows us to specify where to store the configuration values, either flash or RAM. Finally, we use the values for the SSID and password from our configuration to pass as configuration values, assign the configuration, and start the WiFi driver.

#### WiFi event handler

 Now that our WiFi driver is configured and the process of connecting has been started, we have to respond to connection events as they come in. In the initialisation process, we created an EventGroupHandle_t instance and provided a function `event_handler` as the wifi driver's event handler for the process.

{{< highlight c >}}
//    event handler for wifi task
static esp_err_t event_handler(void *ctx, system_event_t *event) {
    switch(event->event_id) {
        case SYSTEM_EVENT_STA_START:
            esp_wifi_connect();
            break;
        case SYSTEM_EVENT_STA_GOT_IP:
            xEventGroupSetBits(wifi_event_group, CONNECTED_BIT);
            printf("got ip\n");
            printf("netmask: " IPSTR "\n", IP2STR(&event->event_info.got_ip.ip_info.netmask));
            printf("gw: " IPSTR "\n", IP2STR(&event->event_info.got_ip.ip_info.gw));
            printf("\n");
            fflush(stdout);
            break;
        case SYSTEM_EVENT_STA_DISCONNECTED:
            esp_wifi_connect();
            xEventGroupClearBits(wifi_event_group, CONNECTED_BIT);
            break;
        default:
            break;
    }
    return ESP_OK;
}
{{< /highlight >}}

The first event we'll encounter `SYSTEM_EVENT_STA_START` arises if `esp_wifi_start()` returns `ESP_OK`, the mode is Station or SoftAP+Station. Typically, all that's needed is to have the device connect to the WiFi network with `esp_wifi_connect()` as we do here.

Once we receive the `SYSTEM_EVENT_STA_GOT_IP` event, it means that the ESP32 has connected to the network and we're ready to do whatever our application does with that connectivity. In our case, we'll be serving an html page. In addition to printing out our addresses, we set a bit in our event handler type. This bit will serve as a flag for our connection status so that other parts of the application are aware of our connection status.

What happens if we disconnect for some reason? If that happens, our event handler receives notification via the `SYSTEM_EVENT_STA_DISCONNECTED` event. There, we just need to clear our connection flag and try to connect again.

<a id="webserver"></a>
### Web server

Now that we have a WiFi connection, we're ready to start a web server.

We'll use the [Netconn API](http://lwip.wikia.com/wiki/Netconn_API) from the lwIP stack to serve our page. Esentially, this  is a sequential API that handles the protocol and keeps us out of the messy implementation details. Mostly.

{{< highlight c >}}
//  http server task
static void http_server(void *pvParameters) {
    struct netconn *conn, *newconn;
    err_t err;
    conn = netconn_new(NETCONN_TCP);
    netconn_bind(conn, NULL, 80);
    netconn_listen(conn);
    do {
        err = netconn_accept(conn, &newconn);
        if (err == ERR_OK) {
            http_server_netconn_serve(newconn);
            netconn_delete(newconn);
        }
    } while(err == ERR_OK);
    netconn_close(conn);
    netconn_delete(conn);
}
{{< /highlight >}}

This is the FreeRTOS task that we start to run the server. First, we'll create a new TCP connection and bind it to our address^[When the address is NULL, `netconn_bind` uses the local IP address and is determined by the networking system. [Source](http://www.ecoscentric.com/ecospro/doc/html/ref/lwip-api-sequential-netconn-bind.html)] and port 80. Next we begin listening on that TCP connection.

In the inner loop, we attempt to make a connection. Once `netconn_accept` returns `ERR_OK` we have a prospective new connection and we can ask our application to serve the page via that connection. To do that we call our function `http_server_netconn_serve()`.

A simplified version of that function looks like:

{{< highlight c >}}
static void http_server_netconn_serve(struct netconn *conn) {
    struct netbuf *inbuf;
    char *buf;
    u16_t buflen;
    err_t err;

    //  read data from the port
    err = netconn_recv(conn, &inbuf);

    if (err == ERR_OK) {
        netbuf_data(inbuf, (void**)&buf, &buflen);
        if( buflen >= 5 && strstr(buf,"GET /") != NULL ) {
            printf("buf[5] = %c\n", buf[5]);        
            netconn_write(conn, http_html_hdr, sizeof(http_html_hdr)-1, NETCONN_NOCOPY);
            netconn_write(conn, str, strlen(str), NETCONN_NOCOPY);
        }
    }
    netconn_close(conn);
    netbuf_delete(inbuf);
}
{{< /highlight >}}

In this function, we simply read the request from the port, make sure it's a GET request, then write the HTTP header and our page. When done, we close our connection and delete the receive buffer.

#### Serving data in our web page.

To serve data from the Si7021 in our page, we create the page dynamically from three parts, two of which are static. All of the page contents _before_ the line with our sensor data are in `htmlA[]` and everything _after_ the sensor data line is in `htmlB[]`. We glue the parts together in a function:

{{< highlight c >}}
void format_html(char *buffer,float t, float h) {
    char f[100];
    sprintf(f,"\t\t<p>Temp = %0.2f Humidity = %0.2f\n", t, h);
    sprintf(buffer,"%s%s%s",htmlA,f,htmlB);
}
{{< /highlight >}}

And that's it. You can find the complete application on [github](https://github.com/NSBum/esp32_server_si7021) to download and try on your own. Obviously you'll need a Si7021 device to try it on. Mine is from [Adafruit](https://www.adafruit.com/product/3251) but you can find them on Aliexpress for considerably less.

### References

- [Complete code for this project](https://github.com/NSBum/esp32_server_si7021)
- [ESP-IDF Wi-Fi API reference](http://esp-idf.readthedocs.io/en/latest/api-reference/wifi/esp_wifi.html)
- [ESP-IDF Wi-Fi Driver API guide](http://esp-idf.readthedocs.io/en/latest/api-guides/wifi.html)
- [lwIP 2.0 documentation](http://www.nongnu.org/lwip/2_0_x/index.html)
- [Netconn API](http://www.nongnu.org/lwip/2_0_x/group__netconn.html)
- [Si7021 datasheet](/2018/03/11/Reading-data-from-Si7021-temperature-and-humidity-sensor-using-Raspberry-Pi/Si7021-A20.pdf)
- [Luca Dentella's tutorial on connecting to a WiFi network using ESP32](http://www.lucadentella.it/en/2017/01/16/esp32-6-collegamento-ad-una-rete-wifi/) and [his sample code](https://github.com/lucadentella/esp32-tutorial/tree/master/02_wifi_connection)
