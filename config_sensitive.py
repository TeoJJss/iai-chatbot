import requests, datetime
from copy import deepcopy

TOKEN = "MTE4NTQ5MTc1OTQ5Nzc1NjY5Mg.GmDf32.mk_Jiy6oWMa6v_u4aMk_asYr67hDJIfENoqKi8"
ID = ["1185519671873638501", "1185517094385745962"]

# Bus Schedule API
try:
    schedules = requests.get("https://api.apiit.edu.my/transix-v2/schedule/active")
    schedules = schedules.json()
    tmp_schedules = schedules['trips'].copy()
except:
    pass

async def bus_schedule(start, end):
    now = datetime.datetime.now()
    try:
        schedule_ind = 0
        while schedule_ind in range(len(tmp_schedules)):
            schedule = tmp_schedules[schedule_ind]
            # No bus on weekend
            if now.weekday() > 4:
                break
            # Skip the "friday only" schedules if it's not Friday
            if schedule['day'] == "friday only" and now.weekday() != 4:
                continue
            time = schedule["time"]
            if datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z') < datetime.datetime.strptime(now.strftime('%Y-%m-%dT%H:%M:%S%z')+"+08:00", '%Y-%m-%dT%H:%M:%S%z'):
                tmp_schedules.remove(schedule)
                continue
            # "Mon-Fri" schedule
            if start in schedule["trip_from"]["name"]:
                if end in schedule["trip_to"]["name"]:
                    bus = schedule["bus_assigned"] if schedule["bus_assigned"] != None else "Unknown"
                    time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z').strftime('%H:%M')
                    return f"Next shuttle `{bus}` will depart **from {start} to {end}** at **{time}**" # Found schedule
            schedule_ind += 1
                
        # No schedule found        
        return f"NO SHUTTTLE SERVICE SCHEDULE available at this moment for **{start} to {end}**. Please refer to APSpace or https://www.apu.edu.my/CampusConnect."
    except:
        # API response error
        return "Sorry, the shuttle schedule is unavailable at the moment. Please refer to APSpace or https://www.apu.edu.my/CampusConnect."

# Holidays Schedule API
holiday_res = requests.get("https://api.apiit.edu.my/transix-v2/holiday/active").json()
holidays_ls = deepcopy(holiday_res)
async def holidays():
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    res=""
    count = 0
    for holiday_list in holidays_ls:
        holiday_ls = holiday_list['holidays']
        holiday_ind = 0
        while holiday_ind < len(holiday_ls):
            if count > 2:
                break
            holiday = holiday_ls[holiday_ind]
            holiday_startdate = datetime.datetime.strptime(holiday["holiday_start_date"], "%a, %d %b %Y %H:%M:%S %Z")
            holiday_enddate = datetime.datetime.strptime(holiday["holiday_end_date"], "%a, %d %b %Y %H:%M:%S %Z")
            holiday_startdate_str = holiday_startdate.strftime('%d %b %Y (%a)')
            holiday_enddate_str = holiday_enddate.strftime("%d %b %Y (%a)")
            if today > holiday_enddate:
                holiday_ls.remove(holiday)
                continue

            if holiday_startdate <= today and holiday_enddate >= today: # Ongoing holiday
                res += "We are in **" + holiday["holiday_description"] + f"** now, from {holiday_startdate_str} to {holiday_enddate_str}.\n"
            elif today < holiday_startdate: # upcoming holiday
                if "Upcoming holidays" not in res:
                    res += "\n**Upcoming holidays**\n"
                if holiday_startdate_str != holiday_enddate_str:
                    res += holiday["holiday_description"] + " - " + f"from {holiday_startdate_str} to {holiday_enddate_str}" + "\n"
                else:
                    res += holiday["holiday_description"] + " - " + f"{holiday_startdate_str}" + "\n"
                count += 1
            holiday_ind+=1
        if not res:
            res = "No Upcoming Holidays"
    return res

# convo list
async def get_qa():
    holidays_str = await holidays()
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
        holidays_str : [
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
            "APU library",
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
            \nYou may also pay with **JomPay**\nBiller Code: 67223\nRef 1: Student ID or NRIC or Passport No\n\
            \n*Remember to email the payment receipt with student name and ID to __bursary@apu.edu.my__*":[
                "What is the Maybank account of APU",
                "Maybank Acc of APU",
                "Maybank Acc of the school",
                "Make payment with Maybank",
                "Pay with Maybank",
                "Maybank",
                "APU Maybank"
        ],
        "**CIMB Account of APU**\n(MYR) 8602647663  \nA/C Name: ASIA PACIFIC UNIVERSITY SDN BHD\n\
            \n*Remember to email the payment receipt with student name and ID to __bursary@apu.edu.my__*":[
                "What is the CIMB account of APU",
                "CIMB Acc of APU",
                "CIMB Acc of the school",
                "Make payment with CIMB",
                "Pay with CIMB",
                "CIMB", 
                "APU CIMB"
        ],
    }

    # Bus schedule algorithm
    added_set = set()
    count = 0
    if schedules: # If schedules from API not empty
        for schedule in schedules['trips']:
            start = str(schedule["trip_from"]["name"]).strip()
            end = str(schedule["trip_to"]["name"]).strip()
            if (start, end) in added_set:
                continue
            else:
                added_set.add((start,end)) # trip has response although no schedule
    for tuple_item in added_set:
        print("tuple: ",tuple_item)
        s_str = await bus_schedule(*tuple_item)
        start = (str(tuple_item[0]).split(" ", 1))[0]
        end = (str(tuple_item[1]).split(" ", 1))[0]
        qa[s_str] = [
            f"What time is the next bus from {start} to {end}",
            f"What time next bus from {start} to {end}", 
            f"What time bus {start} to {end}",
            f"when next bus to {start} to {end}",
            f"{start} to {end} bus",
            f"I am at {end}, going {start}, where bus",
            f"next bus to {end} from {start}",
            f"where bus to {end}",
            f"bus {start} {end}",
            f"trip {start} {end}",
            f"trips from {start} to {end}",
            f"{start} {end} bus",
            f"{start} to {end}"
        ]
        if "Please refer to APSpace or https://www.apu.edu.my/CampusConnect" not in s_str:
            qa[s_str].extend(["bus schedule", "bus trip", "bus", "trip", "shuttle", "shuttle schedule"])
            count += 1
    if not count:
        qa["Sorry, the shuttle service schedule is unavailable at the moment. Please refer to APSpace or https://www.apu.edu.my/CampusConnect."] = [
            "bus schedule", "bus trip", "bus", "trip", "shuttle", "shuttle schedule", "bus to", "bus from", "shuttle to", "shuttle from"]
        
    return qa