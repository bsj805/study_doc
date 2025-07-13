a=dict()

a["holidays"] = {
    "koreaHolidayUseYn" : True,
    "serviceHolidays":[
        "2024-01-02",
        "2024-01-03",
    ]
}

a["scheduleOperationMode"] = "AUTOMATIC"
a["standbyBeforeOperation"] = "10_MIN_BEFORE_START"
a["serviceBusinessTimes"] =  {
    "weekday": {
      "work": {
        "end": "23:59",
        "start": "00:00"
      }
    },
    "weekend": {
      "work": {
        "end": "23:59",
        "start": "00:00"
      },
        "break": {
        "end": "14:00",
        "start": "16:00"
      }
    }
}

import json
print(json.dumps(a, indent=2, ensure_ascii=False))