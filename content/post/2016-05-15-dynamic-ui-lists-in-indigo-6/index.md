---
title: "Dynamic UI lists in Indigo 6"
date: 2016-05-15 06:24:28
aliases: ['/2016/05/15/Dynamic-UI-lists-in-Indigo-6/']
authorbox: false
tags:
- indigo
- home automation
- python
categories:
- home automation
---
[Indigo 6](https://www.indigodomo.com) is a popular home automation controller software package on the Mac. Extensibility is one of its main features and it allows users to add a range of features to suit their needs.

Using Python scripting, users can create plugins that provide extended functionality. These plugins can provide a custom configuration UI to the user. Since the [documentation](http://wiki.indigodomo.com/doku.php?id=indigo_6_documentation:plugin_guide) around a particular feature - [_dynamic lists_](http://wiki.indigodomo.com/doku.php?id=indigo_6_documentation:plugin_guide#dynamic_lists) was lacking, I've written up my approach here.

Since I live in Canada, the excellent [NOAA plugin](https://www.indigodomo.com/library/188/) doesn't work for me. However [Environment Canada](https://weather.gc.ca/canada_e.html) provides an XML-based weather data API that we could package into an Indigo plugin. Since the number of Environment Canada station locations is large, I would like the user to select a province first then select locations within that province. This means that I must use a dynamic list for the locations and reload the location list dynamically when the province changes. The solution turned out to be simple. Perhaps it could be even simpler. This is just what I came up with.

### Devices.xml configuration

{{< highlight xml >}}
<?xml version="1.0"?>
<Devices>
    <!-- define devices -->
    <Device type="custom" id="station">
        <Name>Weather station</Name>
        <ConfigUI>
            <!-- choose location -->
            <Field id="province" type="menu">
                <Label>Province:</Label>
                <List class="self" filter="" method="listProvinces"/>
                <CallbackMethod>provinceChanged</CallbackMethod>
            </Field>
            <!-- choose location within province -->
            <Field id="location" type="menu">
                <Label>Location:</Label>
                <List class="self" filter="" method="listStations" dynamicReload="true"/>
            </Field>
        </ConfigUI>
    </Device>
</Devices>
{{< /highlight >}}

In the device configuration I've specified a `province` field and a `location` field. The former provides a callback method `provinceChanged` where I can deal with filtering the locations based on the province selection. The other key here is to make the location field dynamically-reloadable (`dynamicReload="true"`.) By doing this, we get another call to the list generator method `listStations` when the province is selected.

### Province selection callback ###

In plugin.py, I must provide a callback method `provinceChanged` to save my selection:

{{< highlight python >}}
def provinceChanged(self, valuesDict, typeId, devId):
    self.selectedProvince = valuesDict['province']
{{< /highlight >}}

Here's where the solution _might_ be simpler. The documentation is ambiguous about the status of `valuesDict` if the device hasn't been saved yet. Based on that ambiguity, I decided to save the selected province as an instance variable of my Plugin class.

### Providing a filtered location list ###

My dynamic list generator for the locations takes the selected province instance variable into consideration so that when the list is dynamically reloaded, I get a chance to filter the list by province.

{{< highlight python >}}
def listStations(self, filter="", valuesDict=None, typeId="", targetId=0):
    locations = []
    stations = []
    self.debugLog(u"Generating stations")
    stations = self.locationDB.stationsForProvice(self.selectedProvince)
    for loc in stations:
        option = loc[0]
        city,province = loc[1].encode('utf-8'),loc[2].encode('utf-8')
        stationName = "{0} ({1})".format(city,province)
        locations.append(stationName)
    return locations
{{< /highlight >}}

I have a suspicion there's an easier way. If you know of one, [let me know](mailto:duncan.alan@me.com) and I'll share it.
