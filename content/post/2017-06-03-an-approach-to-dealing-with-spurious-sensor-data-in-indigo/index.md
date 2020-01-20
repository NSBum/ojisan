---
title: An approach to dealing with spurious sensor data in Indigo
date: 2017-06-03 06:14:01
aliases: ['/2017/06/03/An-approach-to-dealing-with-spurious-sensor-data-in-Indigo/']
tags:
- programming
- home automation
- indigo
- python
categories:
- home automation
---
{{< figure src="images/ghgraph.jpg" >}}

Spurious sensor data can wreak havoc in an otherwise finely-tuned home automation system. I use temperature data from an [Aeotech Multisensor 6](http://aeotec.com/z-wave-sensor) to monitor the environment in our greenhouse. Living in Canada, I cannot rely solely on passive systems to maintain the temperature, particularly at night. So, using the temperature and humidity measurements transmitted back to the controller over Z-wave, I control devices inside the greenhouse that heat and humidify the environment.

But spurious temperature and humidity data mean that I often falsely trigger the heating and humidification devices. After dealing with this for several weeks, I came up with a workable solution that can be applied to other sensor data. It's important to note that the solution I developed uses time-averaging of the data. If it's important to react to the data quickly, then the averaging window needs to be shortened or you may need to look for a different solution.

I started by trying to ascertain exactly what the spurious temperature data were. It turns out that usually the spurious data points were 0's. But occasionally odd non-zero data would crop up. In all cases the values were _lower_ than the actual value and always by a lot (i.e. 40 or more degrees F difference.)

In most cases with Indigo, for simplicity, we simply trigger events based on absolute values. When spurious data are present, for whatever reason, false triggers will result. My approach takes advantage of the fact that Indigo keeps a [database of sensor data](http://wiki.indigodomo.com/doku.php?id=indigo_7_documentation:plugins:sql_logger). By default it logs these data points to a SQLite database. This database is at `/Library/Application Support/Perceptive Automation/Indigo 7/Logs/indigo_history.sqlite`. I used the application [Base](https://menial.co.uk/base/) a GUI SQLite client on macOS to explore the structure a bit. Each device has a table named `device_history_xxxxxxxx`. You simply need to know the device identifier which you can easily find in the Indigo application. Exploring the table, you can see how the data are stored.

{{< figure src="images/base.jpg" >}}

To employ a strategy of time-averaging and filtering the data, I decided to pull the last 10 values from the SQLite database. As I get data about every 30 seconds from the sensor, my averaging window is about 5 minutes. It turns out this is quite easy:

{{< highlight python >}}
import sqlite3

SQLITE_PATH = '/Library/Application Support/Perceptive Automation/ \
Indigo 7/Logs/indigo_history.sqlite'
SQLITE_TN = 'device_history_114161618'
SQLITE_TN_ALIAS = 'gh'

conn = sqlite3.connect(SQLITE_PATH)
c = conn.cursor()
SQL = "SELECT gh.sensorvalue from {tn} as {alias} \
ORDER BY ts DESC LIMIT 10".format(tn=SQLITE_TN,alias=SQLITE_TN_ALIAS)
c.execute(SQL)
all_rows = c.fetchall()
{{< /highlight >}}

Now `all_rows` contains a list of single-item tuples that we need to compact into a list. In the next step, I filter obviously spurious values and compact the list of tuples into a list of values:

{{< highlight python >}}
tempsF = filter(lambda a: a > 1, [i[0] for i in all_rows])
{{< /highlight >}}

But some spurious data remains. Remember that many of the errant values are 0.0 but some are just lower than the actual values. To do this, I create a list of the differences from one value to the next and search for significant deviations (5°F in this case.) Having found which value creates the large difference, I exclude it from the list.^[As I was preparing this post, I realized that it this approaches misses the possibility of a dataset having _more than one_ spurious data point. Empirically, I did not notice any occurrence of that, but it's possible. I have to account for that in the future.]

{{< highlight python >}}
diffs = [abs(x[1]-x[0]) for x in zip(tempsF[1:],tempsF[:-1])]
idx = 0
for diff in diffs:
	if diff > 5:
		break;
	else:
		idx = idx+1
filtTempsF = tempsF[:idx+1] + tempsF[idx+2:]
{% endcodeblock %}

Finally, since it's a _moving average_ I need to actually average the data.

{% codeblock lang:python %}
avgTempsF = reduce(lambda x,y : x + y, filtTempsF) / len(filtTempsF)
{{< /highlight >}}

In summary, this gives me a filtered, time-averaged dataset that excludes spurious data. For applications that are very time-sensitive, this approach won't work as is. But for most environmental controls, it's a workable solution to identifying and filtering wonky sensor data.

For reference, the entire script follows:

{{< highlight python >}}
#	Update the greenhouse temperature in degrees C
#	The sensor reports values in F, so we will update
#	the value to see whenever the primary data has any change.

import sqlite3

# device and variable definitions
IDX_CURRENT_TEMP = 1822850463
IDX_FORMATTED = 1778207310
DEV_GH_TEMP = 114161618
SQLITE_PATH = '/Library/Application Support/Perceptive Automation/Indigo 7/Logs/indigo_history.sqlite'
SQLITE_TN = 'device_history_114161618'
SQLITE_TN_ALIAS = 'gh'

DEBUG_GH = True

def F2C(ctemp):
	return round((ctemp - 32) / 1.8,1)

def CDeviceTemp(deviceID):
	device = indigo.devices[deviceID]
	tempF = device.sensorValue
	return F2C(tempF)

def movingAverageF():
	conn = sqlite3.connect(SQLITE_PATH)
	c = conn.cursor()
	SQL = "SELECT gh.sensorvalue from {tn} as {alias} ORDER BY ts DESC LIMIT 10".format(tn=SQLITE_TN,alias=SQLITE_TN_ALIAS)
	c.execute(SQL)
	all_rows = c.fetchall()
	tempsF = filter(lambda a: a > 1, [i[0] for i in all_rows])
	diffs = [abs(x[1]-x[0]) for x in zip(tempsF[1:],tempsF[:-1])]
	idx = 0
	for diff in diffs:
		if diff > 5:
			break;
		else:
			idx = idx+1
	filtTempsF = tempsF[:idx+1] + tempsF[idx+2:]
	avgTempsF = reduce(lambda x,y : x + y, filtTempsF) / len(filtTempsF)
	return avgTempsF

def movingAverageC():
	return F2C(movingAverageF())

# 	compute moving average
avgC = F2C(movingAverageF())

# current greenhouse temperature in degrees C
ghTempC = F2C(indigo.devices[DEV_GH_TEMP].sensorValue)
indigo.server.log("GH temp: raw={0}F, filtered moving avg={1}C".format(ghTempC,avgC))

#	update the server variables (°C temp and formatted string)
indigo.variable.updateValue(IDX_CURRENT_TEMP,value=unicode(avgC))
indigo.variable.updateValue(IDX_FORMATTED, value="{0}°C".format(avgC))

{{< /highlight >}}
