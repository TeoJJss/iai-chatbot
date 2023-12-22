import requests, datetime

TOKEN = "MTE4NTQ5MTc1OTQ5Nzc1NjY5Mg.GmDf32.mk_Jiy6oWMa6v_u4aMk_asYr67hDJIfENoqKi8"
ID = ["1185519671873638501", "1185517094385745962"]

# Bus Schedule
schedules = requests.get("https://api.apiit.edu.my/transix-v2/schedule/active")
schedules = schedules.json()
def bus_schedule(start, end):
    try:
        print("time again")
        for schedule in schedules['trips']:
            if start in schedule["trip_from"]["name"]:
                if end in schedule["trip_to"]["name"]:
                    bus = schedule["bus_assigned"] if schedule["bus_assigned"] != None else "Unknown"
                    time = schedule["time"]
                    print("Time scheduled", datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z'))
                    print("now",datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')+"+08:00", '%Y-%m-%dT%H:%M:%S%z'))
                    if datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z') < datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')+"+08:00", '%Y-%m-%dT%H:%M:%S%z'):
                        continue
                    time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
                    return f"Next bus {bus} will depart from {start} to {end} at **{time}**"
        else:
            return f"No bus schedule available at this moment for {start}-{end}"
    except:
        return "Sorry, the bus schedule is unavailable at the moment. Please refer to webspace or https://www.apu.edu.my/CampusConnect"

# Holidays Schedule
holiday_res = requests.get("https://api.apiit.edu.my/transix-v2/holiday/active").json()
def holidays():
    holiday_ls = holiday_res[0]['holidays']
    upcoming_ls = []
    today = datetime.datetime.utcnow()
    res=""
    for holiday in holiday_ls:
        holiday_startdate = datetime.datetime.strptime(holiday["holiday_start_date"], "%a, %d %b %Y %H:%M:%S %Z")
        holiday_enddate = datetime.datetime.strptime(holiday["holiday_end_date"], "%a, %d %b %Y %H:%M:%S %Z")
        if holiday_startdate < today and holiday_enddate > today:
            res += "We are in " + holiday["holiday_description"] + "now.\n\n"
        if holiday_startdate > today:
            if "Upcoming holidays" not in res:
                res += "**Upcoming holidays**\n"
            holiday_startdate = holiday_startdate.strftime('%a, %d %b %Y')
            holiday_enddate = holiday_enddate.strftime("%a, %d %b %Y")
            res += holiday["holiday_description"] + " : " + f"from {holiday_startdate} to {holiday_enddate}" + "\n"
    if not res:
        res = "No Upcoming Holidays"
    return res

# convo list
def get_qa():
    print("get qa")
    qa = {
        # Campus
        "APU campus is at Jalan Teknologi 5, Taman Teknologi Malaysia, 57000 Kuala Lumpur, Wilayah Persekutuan Kuala Lumpur": [
            "campus",
            "How to go to the campus",
            "How to go campus",
            "How to go APU",
            "Where is campus",
            "Where is APU",
            "Where is APU campus",
            "How do I get to the campus?",
            "How do I get to the APU?",
            "What is the address of the campus?",
            "What is the address of the APU?",
            "go campus",
            "give me the location of the campus",
            "go APU",
            "give me the location of the APU",
        ],
        holidays() : [
            "When is the next holiday",
            "holidays", 
            "holiday",
            "holiday schedule",
            "do we have holiday",
            "APU holiday",
            "upcoming holidays",
            "next holiday",
            "when no class",
            "malaysia holiday",
            "school holidays"
        ],
        # Library
        "You can go to the library by taking the stairs or elevator to Level 4, APU": [
            "library",
            "APU library"
            "How to go to the library",
            "How to go library",
            "How to go to library",
            "go library",
            "Where is library",
            "How do I get to the library?",
            "What is the address of the library?",
            "How to go to the APU library",
            "How to go APU library",
            "How to go to library at APU",
            "go APU library",
            "Where is APU library",
            "How do I get to the APU library?",
            "What is the address of the APU library?",
        ],
        "**Operating hour of library**\nMonday – Friday: 8:30 a.m. – 7:00 p.m.,\nSaturday : 9:00 a.m. - 1:00 p.m.,\nSunday / Public Holidays: Closed":[
            "What is the operating hours of library",
            "Operation hour of library",
            "Operation hour of APU library",
        ],
        "Email: __library@apu.edu.my__\nYou may also call __+603 8992 5207__ (Library Counter) and __+603 8992 5209__ (Reference Desk)":[
            "How to contact library",
            "What is the contacts of library",
            "What is the email of library",
            "How should I contact library",
            "How to email library",
            "How to call library",
            "email library",
            "call library",
            "contact library",
            "talk to library",
            "I need to email library", 
            "I need to call library",
            "I need to contact library",
            "I want to contact library",
            "I want to email library",
            "I want to call library"
        ],
        # Bursary
        "Please check your course fees at APSpace > More > Fees.\nYou may also access the page through https://apspace.apu.edu.my/fees.":[
            "How to check course fee",
            "How do I check course fees",
            "How much is my course fees",
            "How much I need to pay"
        ],
        "Please find the payment details at https://www.apu.edu.my/life-apu/student-services/apu-apiit-bursary-details \
            \nRemember to email the payment receipt with student name and ID to __bursary@apu.edu.my__":[
            "How to make payment",
            "How to pay course fee",
            "How to pay resit fee",
            "What is the bank account details of APU",
            "I need to pay",
            "I need to make payment",
            "Payment Method",
            "How to pay",
            "How should I pay",
            "What is the payment method",
            "How do pay",
            "How to pay fee",
            "How do pay fee",
            "How should I pay fee",
            "How do I pay fee",
        ],
        "**Maybank Account of APU**\n(MYR) 514413500658\n(USD) 714413000532\n A/C Name: ASIA PACIFIC UNIVERSITY SDN BHD\n\
            \nYou may also pay with JomPay\nBiller Code: 67223\nRef 1: Student ID or NRIC or Passport No\n\
            \n*Remember to email the payment receipt with student name and ID to __bursary@apu.edu.my__*":[
                "What is the Maybank account of APU",
                "Maybank Acc of APU",
                "Maybank Acc of the school",
                "Make payment with Maybank",
                "Pay with Maybank",
                "Maybank"
        ],
        "**CIMB Account of APU**\n(MYR) 8602647663  \nA/C Name: ASIA PACIFIC UNIVERSITY SDN BHD\n\
            \n*Remember to email the payment receipt with student name and ID to __bursary@apu.edu.my__*":[
                "What is the CIMB account of APU",
                "CIMB Acc of APU",
                "CIMB Acc of the school",
                "Make payment with CIMB",
                "Pay with CIMB",
                "CIMB"
        ],

        # Transportation
        bus_schedule("LRT", "APU") : [
            "What time is the next bus from LRT to APU",
            "What time next bus from LRT to APU", 
            "What time bus LRT to APU",
            "when next bus to APU from LRT",
            "LRT to APU bus",
            "I am at LRT, going APU, where bus",
            "next bus to APU from LRT",
            "bus schedule",
            "where bus to APU",
            "bus LRT APU",
            "trip LRT APU",
            "trips from LRT to APU",
            "LRT APU bus",
            "LRT to APU"
        ],
        bus_schedule("APU", "LRT") : [
            "What time is the next bus from APU to LRT",
            "What time next bus from APU to LRT", 
            "What time bus APU to LRT",
            "when next bus to LRT from APU",
            "APU to LRT bus",
            "I am at APU, going LRT, where bus",
            "next bus to LRT from APU",
            "where bus to LRT",
            "bus APU to LRT",
            "bus APU LRT",
            "trip APU LRT",
            "trips from APU to LRT",
            "APU LRT bus",
            "APU to LRT"
        ],
        bus_schedule("LRT", "APIIT") : [
            "What time is the next bus from LRT to APIIT",
            "What time next bus from LRT to APIIT", 
            "What time bus LRT to APIIT",
            "when next bus to APIIT from LRT",
            "LRT to APIIT bus",
            "I am at LRT, going APIIT, where bus",
            "next bus to APIIT from LRT",
            "where bus to APIIT",
            "bus LRT APIIT",
            "trip LRT APIIT",
            "trips from LRT to APIIT",
            "LRT APIIT bus",
            "LRT to APIIT"
        ],
        bus_schedule("APIIT", "LRT") : [
            "What time is the next bus from APIIT to LRT",
            "What time next bus from APIIT to LRT", 
            "What time bus APIIT to LRT",
            "when next bus to LRT from APIIT",
            "APIIT to LRT bus",
            "I am at APIIT, going LRT, where bus",
            "next bus to LRT from APIIT",
            "bus APIIT to LRT",
            "bus APIIT LRT",
            "trip APIIT LRT",
            "trips from APIIT to LRT",
            "APIIT LRT bus",
            "APIIT to LRT"
        ],
        bus_schedule("APU", "APIIT") : [
            "What time is the next bus from APU to APIIT",
            "What time next bus from APU to APIIT", 
            "What time bus APU to APIIT",
            "when next bus to APIIT from APU",
            "APU to APIIT bus",
            "I am at APU, going APIIT, where bus",
            "next bus to APIIT from APU",
            "where bus to APIIT",
            "bus APU APIIT",
            "trip APU APIIT",
            "trips from APU to APIIT",
            "APU APIIT bus",
            "APU to APIIT"
        ],
        bus_schedule("APIIT", "APU") : [
            "What time is the next bus from APIIT to APU",
            "What time next bus from APIIT to APU", 
            "What time bus APIIT to APU",
            "when next bus to APIIT to APU",
            "APIIT to APU bus",
            "I am at APIIT, going APU, where bus",
            "next bus to APU from APIIT",
            "where bus to APU",
            "bus APIIT APU",
            "trip APIIT APU",
            "trips from APIIT to APU",
            "APIIT APU bus",
            "APIIT to APU"
        ],
    }
    return qa