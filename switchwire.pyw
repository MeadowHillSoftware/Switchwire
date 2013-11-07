#!/usr/bin/python

# Switchwire 0.1.8
# Copyright 2008-2011 Meadow Hill Software
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Affero General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, time

operator = ""

if os.name in ["posix", "mac"]:
	operator = "nix"
elif os.name == "nt":
	operator = "nt"
	import win32api, win32pdh

sunday = {}
monday = {}
tuesday = {}
wednesday = {}
thursday = {}
friday = {}
saturday = {}
delay = 60
multiple = 1
itineraries = [sunday, monday, tuesday, wednesday, thursday, friday, saturday]

def loadData():
	schedule = open("schedule.txt", "r")
	global sunday
	global monday
	global tuesday
	global wednesday
	global thursday
	global friday
	global saturday
	global delay
	global multiple
	dictionary = {}
	while True:
		entry = schedule.readline()
		if not entry:
			break
		items = entry.split(" ")
		del items[(len(items) - 1)]
		if items[0] == "delay":
			delay = int(items[1])
			if delay not in [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]:
				delay = 60
			multiple = (60 / delay)
		elif items[0] == "day":
			phasenum = 0
			itnum = int(items[1])
			itinerary = itineraries[itnum]
			itinerary["caps"] = {}
			itinerary["hits"] = []
		elif items[0] == "hit":
			index = 1
			while index < len(items):
				itinerary["hits"].append(items[index])
				index += 1
		elif items[0] == "cap":
			index = 1
			while index < len(items):
				itinerary["caps"][items[index]] = int(items[(index + 1)])
				index += 2
		elif items[0] == "phase":
			phasename = ("phase" + str(phasenum))
			itinerary[phasename] = {}
			itinerary[phasename]["start"] = int(items[1])
			itinerary[phasename]["end"] = int(items[2])
			itinerary[phasename]["exceptions"] = []
			index = 3
			while index < len(items):
				itinerary[phasename]["exceptions"].append(items[index])
				index += 1
			phasenum += 1
	schedule.close()

def discipline():
	weekday = 7
	while True:
		day = int(time.strftime('%w'))
		now = int(time.strftime('%H%M'))
		if weekday != day:
			phase = 0
			weekday = day
			itinerary = itineraries[day]
			caps = itinerary["caps"]
		meter = {}
		if caps != {}:
			for x in caps.keys():
				meter[x] = -1
		if itinerary != {}:
			hitlist = itinerary["hits"]
		if meter != {}:
			if operator == "nix":
				for process in caps.keys():
					meter_value = meter[process]
					check = "pidof %s" % process
					if os.system(check) == 0:
						meter_value += 1
						meter[process] = meter_value
						caps_value = caps[process]
						kill = "killall %s" % process
						if meter_value >= (caps_value * multiple):
							os.system(kill)
							print "%s killed" % process
			elif operator == "nt":
				win32pdh.EnumObjects(None, None, win32pdh.PERF_DETAIL_WIZARD)
				items = win32pdh.EnumObjectItems(None, None, "process", win32pdh.PERF_DETAIL_WIZARD)
				for process in caps.keys():
					if process in items[1]:
						meter_value += 1
						meter[process] = meter_value
						caps_value = caps[process]
						if meter_value >= (caps_value * multiple):
							while process in items[1]:
								hQuery = win32pdh.OpenQuery()
								path = win32pdh.MakeCounterPath((None, "process", process, None, 0, "ID Process"))
								handle = win32pdh.AddCounter(hQuery, path)
								win32pdh.CollectQueryData(hQuery)
								value = win32pdh.GetFormattedCounterValue(handle, win32pdh.PDH_FMT_LONG)
								pyhandle = win32api.OpenProcess(1, 0, value[1])
								win32api.TerminateProcess(pyhandle, 0)
								win32pdh.CloseQuery(hQuery)
								items[1].remove(process)
		if itinerary != {}:
			phasename = "phase0"
			num = 0
			while phasename in itinerary.keys():
				if now >= itinerary[phasename]["start"]:
					if now <= itinerary[phasename]["end"]:
						period = num
						if phase != period:
							phase = period
							survivors = itinerary[phasename]["exceptions"]
							targets = [item for item in hitlist if item not in survivors]
						if operator == "nix":
							for process in targets:
								check = "pidof %s" % process
								if os.system(check) == 0:
									kill = "killall %s" % process
									os.system(kill)
						elif operator == "nt":
							win32pdh.EnumObjects(None, None, win32pdh.PERF_DETAIL_WIZARD)
							items = win32pdh.EnumObjectItems(None, None, "process", win32pdh.PERF_DETAIL_WIZARD)
							for process in targets:
								if process in items[1]:
									while process in items[1]:
										hQuery = win32pdh.OpenQuery()
										path = win32pdh.MakeCounterPath((None, "process", process, None, 0, "ID Process"))
										handle = win32pdh.AddCounter(hQuery, path)
										win32pdh.CollectQueryData(hQuery)
										value = win32pdh.GetFormattedCounterValue(handle, win32pdh.PDH_FMT_LONG)
										pyhandle = win32api.OpenProcess(1, 0, value[1])
										win32api.TerminateProcess(pyhandle, 0)
										win32pdh.CloseQuery(hQuery)
										items[1].remove(process)
							items = ()
						phasename = "blah"
					else:
						num += 1
						strnum = str(num)
						phasename = "phase" + strnum
				else:
						phasename = "blah"
		time.sleep(delay)

loadData()
discipline()
