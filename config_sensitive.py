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
                tmp_schedules.remove(schedule)
                continue
            time = schedule["time"]
            if datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z') < datetime.datetime.strptime(now.strftime('%Y-%m-%dT%H:%M:%S%z')+"+08:00", '%Y-%m-%dT%H:%M:%S%z'):
                tmp_schedules.remove(schedule)
                continue
            # "Mon-Fri" schedule
            if start in schedule["trip_from"]["name"]:
                if end in schedule["trip_to"]["name"]:
                    bus = schedule["bus_assigned"] if schedule["bus_assigned"] else "Unknown"
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
                res += "We are in **" + holiday["holiday_description"] + "** now, "
                if holiday_startdate_str == holiday_enddate_str:
                    res += f"on {holiday_startdate_str}.\n"
                else:
                    res += f"from {holiday_startdate_str} to {holiday_enddate_str}.\n"
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
async def get_qa(inp):
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
            "Where APU"
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

        # General knowledge(Course fees)
        "Please check your course fees at APSpace > More > Fees.\nYou may also access the page through https://apspace.apu.edu.my/fees.":[
            "How to check course fee",
            "How do I check course fees",
            "How much is my course fees",
            "How much I need to pay"
        ],
        
        # Library (Location of APU and APIIT)
        "**__APU Library__**\nYou can go to the library by taking the stairs or elevator to Level 4, APU\
        \n\n**__APIIT Library__**\nYou can go to the library by taking the stairs or elevator to Level 2, APIIT": [
            "library",
            "library location",
            "APU library",
            "APIIT library",
            "APU library location",
            "APIIT library location",
            "How to go to the library",
            "How to go library",
            "How to go to library",
            "Where is library",
            "Where is APU library",
            "Where is APIIT library",
            "Where is the library located?",
            "How do I get to the library?",
            "What is the address of the library?",
            "How to go to the APU library",
            "How to go to the APIIT library",
            "How to go APU library",
            "How to go APIIT library",
            "How to go to library at APU",
            "How to go to library at APIIT",
            "go library",
            "go APU library",
            "go APIIT library",
            "How do I get to the APU library?",
            "How do I get to the APIIT library?",
            "where library"
        ],

        # Library(Operating hours)
        "**Operating hour of APU library**\nMonday – Friday: 8:30 a.m. – 7:00 p.m.,\nSaturday : 9:00 a.m. - 1:00 p.m.,\nSunday / Public Holidays: Closed\
         \n\n**Operating hour of APIIT library**\nMonday – Friday: 8:30 a.m. – 6:00 p.m.,\nSaturday / Sunday / Public Holidays: Closed ": [
            "What is the operating hours of library",
            "Operating hour of APU library",
            "Operating hour of APIIT library",
            "Operation hour of library",
            "Operation hour of APU library",
            "Operation hour of APIIT library",
            "When does the library open?",
            "When does the APU library open?",
            "When does the APIIT library open?",
            "What time does the library open",
            "What time does the APU library open",
            "What time does the APIIT library open",
            "What time does the library open on weekdays?",
            "What time does the APU library open on weekdays?",
            "What time does the APIIT library open on weekdays?",
            "Is the library open on weekends?"
            "Is the APU library open on weekends?"
            "Is the APIIT library open on weekends?"
            "Is the library open on Saturdays?",
            "Can I visit the library on public holidays?",
            "Is the library closed on public holidays?",
            "What is the schedule for the library?",
            "Library open hours",
            "APU Library open hours",
            "APIIT Library open hours",
            "Library open time",
            "APU Library open time",
            "APIIT Library open time",
            "When does the library open and close?",
            "When does the APU library open and close?",
            "When does the APIIT library open and close?",
            "When can I visit the library during the week?",
        ],
    
        # Library(contact)
        "Email: __library@apu.edu.my__\nYou may also call __+603 8992 5207__ (Library Counter) and __+603 8992 5209__ (Reference Desk)": [
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
            "I want to call library",
        ],
    
        # Library(am I allowed to bring food/drinks)
        "Food and canned drinks are strictly not allowed in the library. Drinking water in bottles and spill-proof containers are permitted. ": [
            "Can I bring food to library?",
            "Can I bring food into the library?",
            "Can I bring drink to library?",
            "Can I bring drink into the library?",
            "Can I eat in the library?",
            "Can I drink in the library?",
            "Can I drink anything other than water in the library?",
            "Can I bring my own water bottle to the library?",
            "Library food rules?",
            "Is food allowed in the library?",
            "What is the policy on eating in the library?",
            "What is the policy on drinking in the library?",
            "Are bottled drinks allowed in the library?",
            "Are outside beverages allowed in the library?",
        ],

        # Library(can I sleep)
        "Sleeping is strictly not allowed in the library as we want to maintain a professional ambience and a pleasant environment of the library.\
        \nHowever, you are welcome to relax by listening to music, chatting with friends, and doing other activities that don't disrupt the library's atmosphere.": [
            "Can I sleep in the library?",
            "What happens if I fall asleep in the library?",
            "Can I take a nap in the library",
            "Is it okay to sleep in the library?",
            "Can I use the library for a short nap?",
            "Is sleeping allowed in the library?",
            "Can I lie down in the library?",
            "Can I sleep in the library if I am tired?",
            "Can I sleep on the couch in the library?",
            "Is it ok to sleep in the library?",
            "Is it fine to take a nap in the library?",
            "Can I have a quick nap in the library?",
        ],

        # Library(How to apply for library job vacancies)
        "You will have to submit the online job application form, which will be available once the recruitment advertisement is published on the APSpace and library website.The application form must be submitted along with: **`Cover Letter,Curriculum Vitae (CV),Passport-sized photograph.`**\
        \nYou'll be interviewed if shortlisted. Applicants who were rejected would be contacted by email.": [
            "How to apply for library job vacancies?"
            "How can I apply for a job at the library?",
            "What is the procedure to apply for a job in the library?",
            "What is the process to apply for a library job?",
            "What is the requirement to apply for a library job?",
            "What are the steps to apply for a library job?",
            "I am interested in working at the library",
            "I would like to apply for a job in the library",
            "I am thinking of working in the library",
            "How to apply for a library position?",
            "I want to work in the library",
            "I want to apply for a library job",
            "I wish to apply for a library position.",
            "How to apply to be a librarian",
            "How do I submit an application for a library job?",
            "How can I work part time in a library?",
            "How to get a part time job in a library",
            "How to work as a part time in a library",
            "How to work part-time in a library"
            "I wish to work at the library",
            "How to apply for a position in the library?",
            "How do I apply for a position at the library?",
            "I am interested in a library job",
            "I am looking to work in the library.",
            "Where can I find the application for library vacancies?",
            "What steps do I need to take to apply for a job at the library?",
            "Is there an online application portal for library job opportunities?",
            "What documentation do I need to prepare for my library job application?",
            "What should I include in my resume for a library job application?",
            "What documents do I need to attach when submitting my library job application?",
            "How to apply job in library?",
        ],

        # Library(how to search printed books?)
        "1) Access the OPAC portal using this link: https://opac.apiit.edu.my/ \n2) Search for the book and click “Go“. Select keyword, ISSN, and Subject from the drop-down menu adjacent to the search bar to change search details.\
            \n3) Choose the book that you want and click the title.\n4) Search for the book on the shelf using the call number and also take note of the library's location.\
            \n5) Ensure the book is “Available”. You can reserve if the status is “Checkout”.": [
            "find book",
            "search book",
            "search printed books",
            "How to search for printed book?",
            "How do I search for a specific book?",
            "How do I find a book in the library?",
            "How do I look a book in the library?",
            "How to search for a library book?",
            "How can I locate a book in the library?"
            "What is the best way to search for a book?",
            "Where do I go to find a physical book?",
            "What should I do to get a book in the library?",
            "Where can I search for a library book?",
            "How can I quickly find a book by its title?",
            "What is the fastest way to find a book?",
            "How to locate a book in the library?",
            "What is the easiest way to find a book?",
            "Steps to find a book",
            "What is the process to find a book?",
            "I need help finding a book",
            "What should I do to locate a book in the library?",
        ],
    
        # Library(how to borrow items from the library?)
        "You can either bring the items that you wish to borrow along with your ID to the counter or proceed to our Self-checkout kiosk for a quicker check-out process.": [
            "Borrow book",
            "How to borrow a book?",
            "How do I borrow books from the library?",
            "How to borrow items from the library?",
            "How can I borrow book from the library?",
            "What is the process to borrow a book from the library?",
            "What steps should I follow to borrow a book from the library?",
            "How can I borrow a book from the library?",
            "What is the procedure to borrow items from the library?",
            "What is the procedure to borrow a book from the library?",
            "What do I need to do to borrow books from the library?",
            "What should I do to borrow a book from the library?",
            "Do I need a library card to borrow items?",
            "Do I need my student card to borrow items?",
            "Do I need my student card to borrow a book?",
        ],

        # Library(How many items can students and staff borrow?)
        "Certificate, Foundation, Diploma and Degree Students- 4 items\nPostgraduate Students (Full-time)- 10 items\nPostgraduate Students (Part-time)- 6 items\
        \nAcademic Staff (Full-time)- 20 items\nAcademic Staff (Part-time)-10 items\nAdministrative Staff- 2 items\nEnglish Language Course Students- 2 items\
        \nEFREI Students-2 items": [
            "Amount of borrowing item per time",
            "How many item can a peson borrow?",
            "How many items can a student borrow?",
            "How many items can a staff borrow?",
            "How many books can I borrow?",
            "How many books can I borrow per time?",
            "How many books can I borrow at once?",
            "How many items can I borrow?",
            "How many items can I borrow per time?",
            "How many items can I borrow at once?"
            "How many items am I allowed to borrow",
            "borrowing limit",
            "What is my borrowing limit?",
            "Maximum amount of book to borrow per person",
            "What is the maximum amount of books I can borrow?",
            "How many books can I borrow as a Certificate student?",
            "How many books can I borrow as a Foundation student?",
            "How many books can I borrow as a Diploma student?",
            "How many books can I borrow as a Degree student?",
            "How many books can I borrow as a Full time Postgraduate student?",
            "How many books can I borrow as a Part time Postgraduate student?",
            "How many books can I borrow as a Full time Academic staff?",
            "How many books can I borrow as a Part time Academic staff?",
            "How many books can I borrow as a Administrative Staff?",
            "How many books can I borrow as a English Language Course Students?",
            "How many books can I borrow as a EFREI Students?",
        ],

        # Library(How to extend the borrowing book due date?)
        "You can either renew the items over the counter or you can do an online renewal if you have not reached your renewal limits. If you have reached the renewal limit, you will have to bring the item to the library to see if it can be further extended. \
        \nOnline renewal can be done by logging in to your “My Library Account”, https://library.apu.edu.my/": [
            "renew book",
            "extend book due date",
            "How to extend the borrowing book due date?",
            "How to extend the due date for the library books?",
            "What is the process for renewing my borrowed books?",
            "What are the steps to extend the due date of my library books?",
            "What is the process for renewing books",
            "Can I extend the due date of my books online?",
            "Is there a way to extend the return date of my borrowed books?",
            "How to renew my library books online?",
            "How can I extend the due date for my borrowed books?",
            "Is there an online option to extend the due date for library books?",
            "Can I renew my borrowed books",
            "Can I renew books at the counter",
            "Can I renew books online?",
            "Can I renew my books in person?"
            "Can I request an extension for the due date of my borrowed books?",
            "Steps to extend book due date",
            "Online book renewal process",
            "Procedure to extend book return date",
            "How do I keep my books longer?",
            "How do I renew my books online?",
            "How to renew a book?",
        ],
        
        #Bursary (Payment details)
        "Please find the payment details at https://www.apu.edu.my/life-apu/student-services/apu-apiit-bursary-details \
        \nRemember to email the payment receipt with student name and ID to __bursary@apu.edu.my__": [
            "How to make payment",
            "How to pay course fee",
            "How to pay resit fee",
            "How to pay for accomodation fee",
            "What is the bank account details of APU",
            "I need to pay",
            "I need to make payment",
            "Payment Method",
            "Payment"
        ],

        #Bursary (How to check fee payment on APspace)
        "**Step 1** - Open your APSpace app or web browser.\
        \n**Step 2** - Scroll down to the Financial widget to get quick overview of your fee payment. In the Financial widget, you can filter and hide by tapping on the color-code.\
        \n**Step 3** - If you want to have a detail information/history of fee payment transaction; you can search for **“Fees”** or click **“More”** and scroll down to Finance section.\
        \n**Step 4** - In Finance page, you can see **Summary** and **Details** of your fee payment.\
        \nYou may also click this link to proceed: https://apspace.apu.edu.my/fees.":[
            "Fee payment",
            "Fee payment details",
            "Fee payment status",
            "Fee payment history",
            "Fee payment summary",
            "How to check fee payment?",
            "How to check my fee payment details?",
            "What are the steps to view my fee payment details?",
            "What are the steps to check my fee payment details?"
            "Can you guide me on how to find my fee payment details?",
            "Where to check fee payment details?",
            "Where can I find details about my fee payment?",
            "How can I see my fee payment history ?",
            "Where to check fee payment?",
            "Steps to check fee payment",
            "How can I view my fees on APspace?",
            "How to check my fee pay payment status?",
            "How to find payment information on APspace?",
            "Paid fee details",
            "Paid fee history",
            "Steps to check paid fee",
            "What are my paid fee?",
            "How to check paid fee?",
            "How can I check my paid fee details?",
            "Where can I find information about my Paid fees?",
            "What are the steps to check my Paid fee details?",
            "How to know if I have paid my fee successfully?",
            "Outstanding fee details",
            "Steps to check outstanding fee",
            "What are my outstanding fee?",
            "How to check outstanding fee?",
            "How can I check my Outstanding fee details?",
            "Where can I find information about my Outstanding fees?",
            "What steps should I follow to check my Outstanding fee details?",
            "How much is my outstanding fee?",
            "Overdue fee details",
            "Overdue fee sumary",
            "Steps to check overdue fee",
            "What are my overdue fee?",
            "How to check overdue fee",
            "How can I check my Overdue fee details?",
            "Where can I find information about my Overdue fees?",
            "What steps should I follow to check my Overdue fee details?",
            "How much is my ovedue fee?",
        ],

        #Bursary (Bank details-Maybank APU & APIIT)
        "**Maybank Account of APU**\n\
        \nA/C Name: ASIA PACIFIC UNIVERSITY SDN BHD\nA/C Number (MYR): 514413500658\nA/C Number (USD): 714413000532\nSwift Code: MBBEMYKL\n\
        \nYou may also pay with **JomPay**\nBiller Code: 67223\nRef 1: Student ID or NRIC or Passport No\n\
        \n`******************************************************************************************************************************`\n\
        \n**Maybank Account of APIIT**\n\
        \nA/C Name: APIIT SDN BHD\nA/C Number (MYR): 514413500575\nA/C Number (USD): 714413000518\nSwift Code: MBBEMYKL\n\
        \nYou may also pay with **JomPay**\nBiller Code: 26070\nRef 1: Student ID or NRIC or Passport No\n\
        \n*Remember to email the payment receipt with student name and ID to __bursary@apu.edu.my__*": [
            "What is the Maybank account of APU",
            "What is the Maybank account of APIIT",
            "Maybank Acc of APU",
            "Maybank Acc of APIIT",
            "Maybank Acc of the school",
            "Make payment with Maybank",
            "Pay with Maybank",
            "Maybank",
            "APU Maybank",
            "APU Jompay",
            "Jompay",
            "APIIT Maybank",
            "APIIT JomPay"
            "Maybank account detais",
            "Pay with Maybank",
            "Maybank",
        ],

        #Bursary (Bank details-CIMB APU & APIIT)
        "**CIMB Account of APU**\nA/C Name: ASIA PACIFIC UNIVERSITY SDN BHD\nA/C Number (MYR): 8602647663\n\
        \n`******************************************************************************************************************************`\n\
        \n**CIMB Account of APIIT**\nA/C Name: APIIT SDN BHD\nA/C Number (MYR): 8603504063\n\
        \n*Remember to email the payment receipt with student name and ID to __bursary@apu.edu.my__*": [
            "What is the CIMB account of APU",
            "What is the CIMB account of APIIT",
            "CIMB Acc of APU",
            "CIMB Acc of APIIT",
            "CIMB Acc of the school",
            "Make payment with CIMB",
            "CIMB account details",
            "Pay with CIMB",
            "CIMB",
            "APU CIMB",
            "APIIT CIMB"
        ],

        #Bursary (How does international students make payment)
        "**Flywire**\nPayments can be made at http://apu-my.flywire.com/. \nAPU has partnered with Flywire, to provide international students with an easy and secure method of paying from overseas.To learn more, visit https://www.flywire.com/support.": [
            "overseas payment",
            "How to pay from overseas?",
            "How do I make an international payment?",
            "Ways to make payment from overseas",
            "How does international student make payment?",
            "What are the payment methods for international students?",
            "Are international payments via credit card accepted?",
            "How can international students make payment?",
            "Can international students pay online?",
            "Can international students pay through bank transfer?",
            "Can international students pay in their home currency?",
            "Can international payments be made online?",
            "What are my options for international payments to Malaysia?",
            "Options for overseas payments?",
            "How to pay fees from abroad?",
            "How can I pay for my tuition from abroad?",
            "How do I pay my tuition from another country?",
            "Is it possible for me to pay online from abroad?",
        ],

        # Bursary (pay with cheque)
        "**Cheque or Banker's Draft Payment**\
            \nPayable: ASIA PACIFIC UNIVERSITY SDN BHD \
            \n*You may handover the document to the bursary counter at Level 3 Spine, APU Campus*":[
                "How to pay cheque",
                "How to pay banker's draft",
                "How to pay fee with cheque",
                "pay with cheque",
                "pay with banker draft",
                "pay cheque",
                "payment cheque",
                "pay fee cheque"
        ],

        #Bursary (How to make payment via Flywire?)
        "1) Visit http://apu-my.flywire.com/ to start.\n2) Input your payment amount and where you’re from.\n3) Select your payment method.\n4) Give some basic info to book your payment.\
        \n5) Follow the steps to transfer funds to Flywire.\n6) Get updates via text and email until your payment reaches your institution. You can also track it anytime by creating a Flywire account.": [
            "How to make payment with Flywire",
            "How to make payment using Flywire",
            "How to make payment through Flywire",
            "How to pay with Flywire",
            "How to pay through Flywire",
            "How to pay using FLywire",
            "How to pay fees using Flywire",
            "How to use Flywire to make payment?",
            "How to transfer money through Flywire",
            "How do I make a transaction using Flywire",
            "Steps to transfer money through Flywire",
            "Procedure to make payment with Flywire",
            "Instructions to make payment with Flywire",
            "How do I use Flywire?",
            "How to send money through Flywire?",
            "How does payment work on Flywire?",
            "How do I make a transfer with Flywire?",
            "Steps to pay with Flywire",
            "How can I make payment using FLywire",
            "Guide me how to use Flywire to make payment",
            "Explain how to use Flywire for payments",
            "What are the instructions for Flywire payments",
            "How to use Flywire to make payment",
            "Flywire",
            "APU Flywire",
            "pay flywire"
        ],
    
        # Bursary (APU/APIIT International Student Fees & Refund Policy)
        "- International Students are required to pay all fees due prior to arrival by the respective due dates.\
         \n- The International Student Application Fee and International Student Registration Fee will not be refunded.\
         \n- Course fee payments made are **NON-REFUNDABLE** except if the student visa is refused by EMGS/ Immigration. All Fees paid are **NON-REFUNDABLE** under any circumstances once the visa is approved or after the student has commenced studies at any level, including `Intensive English, Diploma, Certificate, Foundation Programme, and Bachelor’s Degree Programmes.` This includes students who do not qualify for enrolment into the course approved in the Visa Approval Letter (VAL) due to not achieving the required English competency.\
         \n- Students will not be permitted to check-in into our University-managed accommodation without the payment of all required fees and associated deposits as indicated above.\
         \n- A late payment charge is imposed on all overdue fees.\
         \n- Semester Payment is due at the commencement of each semester.": [
            "What are the International Student Fees & Refund Policy?",
            "Refund policy for International Student",
            "Student Fees for International Student",
            "Explain the fees and refund policy for International Student",
            "How does the fee payment and refund process work for International Student?",
            "How does university refund policy and fees for International Student?",
            "Can International Student get a refund if they withdraw from the course?",
            "What happens if International Student pay late?",
            "What is the process for International Student to apply for a refund?",
            "How can International Student apply for a refund?,"
            "What are the penalties for late payment for International Students?",
        ],

        # Bursary (APU/APIIT Malaysian Student Fees & Refund Policy)
        "**APU/APIIT Malaysian Student Fees & Refund Policy** \
        \n- APU/APIIT will provide a refund to cancellations notified and received more than 14 days before the commencement of a course.\
        \n- A charge of 50% of the initial payment will apply for cancellation made 14 days or less before course commencement.\
        \n- An Administrative Fee of RM 200.00 will be charged for any transfer of registration prior and after course commencement, including changes in course specialization.\
        \n- NO REFUND will be entertained after a course has commenced.\
        \n- Applicants who intend to apply for withdrawals from EPF or other approved study loans (including PTPTN, MARA) are required to pay the fee on the monthly installment basis until the loan is disbursed.\
        \n- A late payment charge is imposed on all overdue fees.\
        \n- Semester Payment is due at the commencement of each semester.\
        \n\n*Please refer to the bursary department of APU for details.*": [
            "What are the Malaysian Student Fees & Refund Policy? ",
            "Refund policy for Malaysian Student",
            "Student Fees for Malaysian Student",
            "Explain the fees and refund policy for Malaysian Student",
            "How does the fee payment and refund process work for Malaysian Student?",
            "How does university refund policy and fees for Malaysian Student?",
            "Can Malaysian Student get a refund if they withdraw from the course?"
            "What happens if Malaysian Student pay late?",
            "What is the process for Malaysian Student to apply for a refund?",
            "How can Malaysian Student apply for a refund?",
            "What are the penalties for late payment for Malaysian Student?",
            "refund policy"
        ],
        
        # Bursary Contact
        "Email: __bursary@apu.edu.my__\nYou may also call __+603 8992 5228__":[
            "How to contact bursary",
            "What is the contacts of bursary",
            "What is the email of bursary",
            "How should I contact bursary",
            "How to email bursary",
            "How to call bursary",
            "email bursary",
            "call bursary",
            "contact bursary",
            "talk to bursary",
            "I need to email bursary", 
            "I need to call bursary",
            "I need to contact bursary",
            "I want to contact bursary",
            "I want to email bursary",
            "I want to call bursary",
            "cashier contact",
            "cashier email"
        ],

        # Bursary Late Payment
        "**Late Payment Penalties**\
            \nStudents will cease to enjoy all rights and privileges of a student of APU, after 7 days from the payment due date.\
            \nBesides, late charges will be applied to the student.\
            \nYou are advised to check APSpace for outstanding payments and settle the payments at least 3 working days earlier.\
            \nFor more details, please check the APU Student Handbook, https://apiit.atlassian.net/wiki/spaces/AA/pages/1199570953/Student+Handbook.":[
                "late payment",
                "late charges",
                "late penalties",
                "late penalty",
                "late pay",
                "late charge",
                "late payments",
        ],
        
        # Bursary location
        "The Bursary Office is located at Level 3 Spine, APU Campus. ":[
            "Where is cahier",
            "where cashier",
            "where is bursary",
            'where bursary',
            "where to pay",
            "how to go cashier",
            "how to go bursary",
            "where to pay cheque",
            "cashier counter",
            "payment counter"
        ],  

        ######Logistics & Operations - APU Campus Connect Lounge
        "APU Campus Connect Lounge will serve the purposes for Arrival and Departure for all APU Shuttle Buses. \nIt is located at Level 1M near main entrance, accessible via the glass elevator. \n**Operational Hours:** Monday – Friday: 8.00am – 10.00pm.":[
            "Purpose Connect Lounge",
            "purpose APU Shuttle Bus",
            "purpose Bus Shuttle ",
            "Purpose APU Connect Lounge",
            "APU Connect Lounge purpose?",
            "Campus Connect Lounge purpose?",
            "Connect Lounge purpose?",
            "Shuttle Bus purpose?",
            "APU Shuttle Bus purpose?",
            "APU Bus Lounge purpose?",
            "Arrival Lounge purpose for APU bus?",
            "Departure Lounge purpose for APU bus?",
            "How do I access APU Connect Lounge?",
            "What is the purpose of Block E lounge?",
            "Where can I find the Level 1 lounge?",
            # "Cleanliness expectations for the lounge?",
            "How do APU Shuttle Buses operate?",
            "What is the purpose of APU Shuttle Buses?",
            "Provide info about Arrival and Departure for APU Shuttle Buses.",
            "How does APU Shuttle Bus service operate?",
            "What is the purpose of APU Shuttle Bus?",
            "Provide info about Arrival and Departure for APU Shuttle Bus.",
            "How does APU Campus Connect Lounge bus service operate?",
            "What is the purpose of APU Campus Connect Lounge Bus?",
            "Provide info about Arrival and Departure for APU Campus Connect Lounge Bus.",
            "Where's the departure lounge for APU bus?",
            "Where to wait for shuttle bus APU?",
            "How to access APU Connect Lounge?",
            "What is the location of APU Connect Lounge?",
            # "How do I use APU Connect Lounge responsibly?",
            # "What are users' responsibilities in the lounge?",
            # "Guidelines for responsible lounge use?",
            # "How to maintain cleanliness of APU Campus Lounge?",
            # "What's expected in terms of cleanliness in the lounge?",
            "How to responsibly use APU Campus Lounge?",
            "How is APU Connect Lounge accessed?",
            "What is the purpose of the lounge in Block E?",
            "Where is the Level 1 lounge located?",
            "What are the cleanliness expectations for the lounge?",
            "How are APU Shuttle Buses operated?",
            "What is the purpose of APU Shuttle Buses?",
            "Information about Arrival and Departure for APU Shuttle Buses.",
            "How is the APU Shuttle Bus service operated?",
            "What is the purpose of APU Shuttle Bus?",
            "Information about Arrival and Departure for APU Shuttle Bus.",
            "How is the APU Campus Connect Lounge Bus service operated?",
            "What is the purpose of APU Campus Connect Lounge Bus?",
            "Information about Arrival and Departure for APU Campus Connect Lounge Bus.",
            "Where's the departure lounge for APU bus?",
            "Where should the shuttle bus be waited for at APU?",
            "How is APU Connect Lounge accessed?",
            "What is the location of APU Connect Lounge?",
            "How should APU Connect Lounge be responsibly used?",
            "What are the responsibilities of users in the lounge?",
            "Guidelines for responsible use of the lounge?",
            "How is the cleanliness of APU Campus Lounge maintained?",
            "What's expected in terms of cleanliness in the lounge?",
            "How is APU Campus Lounge responsibly used?",
            "Tell me about the APU Shuttle Buses.",
            "How does the APU Shuttle Bus service work?",
            "What is the purpose of the APU Shuttle Buses?",
            "Can you provide information about Arrival and Departure for APU Shuttle Buses.",
            "Tell me about the APU Shuttle Bus.",
            "How does the APU Shuttle Buses service work?",
            "What is the purpose of the APU Shuttle Bus?",
            "Can you provide information about Arrival and Departure for the APU Shuttle Bus.",
            "Tell me about the APU Shuttle Buses.",
            "How does the APU Shuttle Bus service work?",
            "What is the purpose of the APU Shuttle Buses?",
            "Can you provide information about Arrival and Departure for APU Shuttle Buses.",
            "Tell me about the Bus Shuttle.",
            "How does the Bus Shuttle service work?",
            "What is the purpose of the Bus Shuttle?",
            "Can you provide information about Arrival and Departure for Bus Shuttle.",
        ],
        "**Operational Hours of APU Campus Connect Lounge:**\n Monday – Friday: 8.00am – 10.00pm":[
            "Open time APU Campus Connect Lounge",
            "Open time APU bus shuttle",
            "Close time APU Campus Connect Lounge",
            "Close time APU bus shuttle",
            "When does APU Campus Connect Lounge operate?",
            "What are the lounge's opening hours on weekdays?",
            "When does the lounge close on weekdays?",
            "Tell me the operational hours of APU Campus Connect Lounge.",
            "When is APU Campus Connect Lounge open on weekdays?",
            "What time does the lounge close on weekdays?",
            "What are the operating hours of APU Campus Lounge?",
            "Operating hours of APU Campus Connect Lounge?",
            "Apu campus connect lounge operational hours?",
            "When does APU Lounge operate?",
            "What are the lounge hours on weekdays?",
            "When does the lounge close?",
            "Tell me the hours of APU Connect Lounge.",
            "When is APU Lounge open on weekdays?",
            "What time does the lounge close?",
            "What are the operating hours of APU Campus Connect Lounge?",
            "Operating hours of APU Connect Lounge?",
            "Apu campus lounge operational hours?",
            "When is the APU Campus Connect Lounge operating?",
            "What are the lounge's opening hours on the weekdays?",
            "When does the lounge closes on weekdays?",
            "Tell me the operational hours for APU Campus Connect Lounge.",
            "When is APU Campus Connect Lounge opened on weekdays?",
            "What time does the lounge closes on weekdays?",
            "What are the operational hours for APU Campus Lounge?",
            "Operating hours for APU Campus Connect Lounge?",
            "Apu campus connect lounge operation hours?",
            "When does APU Connect Lounge open and close?",
            "Tell me about the operating schedule of APU Lounge.",
            "What are the hours of APU Campus Connect Lounge?",
            "When is APU Campus Lounge accessible on weekdays?",
            "Apu campus connect lounge hours?",
            "When does APU Shuttle Bus operate?",
            "What are the APU Shuttle Bus hours on weekdays?",
            "When does the Shuttle Bus close on weekdays?",
            "Tell me the operational hours of APU Shuttle Bus.",
            "When is APU Shuttle Bus open on weekdays?",
            "What time does the Shuttle Bus close on weekdays?",
            "What are the operating hours of APU Shuttle Bus?",
            "Operating hours of APU Shuttle Bus?",
            "Apu shuttle bus operational hours?",
            "When does Bus Shuttle operate?",
            "What are the Bus Shuttle hours on weekdays?",
            "When does the Bus Shuttle close on weekdays?",
            "Tell me the operational hours of Bus Shuttle.",
            "When is Bus Shuttle open on weekdays?",
            "What time does the Bus Shuttle close on weekdays?",
            "What are the operating hours of Bus Shuttle?",
            "Operating hours of Bus Shuttle?",
            "Bus shuttle operational hours?",
        ],
        ###### Logistics & Operations - RapidKL Bus & LRT
        "Rapid KL Bus Route Information: \n https://myrapid.com.my/bus-train/rapid-kl/bus/":[
            "Rapid KL Bus",
            "Bus KL",    
            "KL bus route",
            "Tell me about Rapid KL bus routes.",
            "What is the link for Rapid KL bus route information?",
            "How can I find Rapid KL bus routes?",
            "How do I find info on Rapid KL bus routes?",
            "Explore Rapid KL bus routes.",
            "Guide to Rapid KL bus routes.",
            "Where can I see Rapid KL bus routes?",
            "Where can I view Rapid KL bus routes?",
            "Show me Rapid KL bus routes.",
        ],
        "RapidKL Journey Planning: \n https://www.myrapid.com.my/pulse-journey-planner ":[
            "KL journey planner",
            "journey planner",
            "journey planner KL",
            "How do I plan my journey with RapidKL?",
            "How to plan a journey with RapidKL?",
            "Tell me about RapidKL journey planner.",
            "Tell me about RapidKL's journey planner.",
            "What's the link for RapidKL journey planning?",
            "Guide to plan my journey with RapidKL.",
            "Guide for planning my journey with RapidKL.",
            "Where can I access RapidKL's journey planner?",
            "Where can I find RapidKL journey planner?",
            "Help with planning my journey on RapidKL.",
            "Help me with RapidKL journey planning.",
        ],
        ###### Logistics & Operations - APU and APIIT Car Parking Rates
        "**Parking Zone A (APU)** *(Covered Parking)*:\nDaily Parking Rate: RM 5.60\n*(Pay via APCard)* \n\n**Parking Zone B (APU) and Zone G (APIIT)** *(Open Parking)* \nHourly Parking Rates *(Pay via APCard)* \n1st hour or part thereof: RM 1.82 \nEvery subsequent hour or part thereof: RM 1.06 \nMaximum charge per day: RM 5.00\n\n**TPM Carpark (MRANTI)**\nHourly Parking Rates *(Pay via Flexi Parking 2.0 Mobile App)*\n1st hour or part thereof: RM 3.18 \nEvery subsequent hour or part thereof: RM 1.06 \nMaximum charge per day: RM 7.42":[
            "APU parking",
            "APU parking fees",
            "APU park",
            "APU car",
            "APU motorcycle",
            "campus parking",
            "campus parking fees",
            "campus park",
            "campus car",
            "campus motorcycle",
            "university parking",
            "university parking fees",
            "university park",
            "university car",
            "university motorcycle",
            "college parking",
            "college parking fees",
            "college park",
            "college car",
            "college motorcycle",
            "school parking",
            "school parking fees",
            "school park",
            "school car",
            "school motorcycle",
            "Zone A and Zone B",
            "Compare Zone A and Zone B",
            "Distinguish between Zone A and Zone B",
            "Tell me the distinctions of Zone A and Zone B",
            "What sets Zone A apart from Zone B?",
            "Contrast Zone A and Zone B",
            "Explain the variations between Zone A and Zone B",
            "Outline the differences of Zone A and Zone B",
            "Elaborate on the disparities between Zone A and Zone B",
            "What characteristics differentiate Zone A and Zone B?",
            "Enumerate the dissimilarities between Zone A and Zone B",
            "Underground parking",
            "Covered parking",
            "Tell me about Parking Zone A.",
            "What is the category of Parking Zone A?",
            "How much is the daily parking rate for Zone A?",
            "Daily parking rate for Covered Parking Zone A.",
            "Parking Zone A: Covered Parking",
            "What is the daily parking rate for Covered Parking in Zone A?",
            "Parking Zone B and Zone G: Open Parking",
            "What are the hourly parking rates for Open Parking Zone B and Zone G?",
            "What is the maximum charge per day for Open Parking?",
            "How are parking rates calculated?",
            # "What should I ensure before entering and exiting the parking with an APCard?",
            "Is the daily parking rate applicable for Covered Parking?",
            "What type of parking rates does Open Space Parking (Zone B and Zone G) offer for students?",
            "How are parking fees transactions conducted?",
            "parking fee",
            "parking rate",
            "car park fee",
            'car park rate'
            # "Reminder:",
            # "How can I avoid being charged twice for parking fees?",
            # "Safety Notice of parking",
            # "Safety Notice",
            # "What responsibility does the management take for injuries or loss of property within the car park?"
        ],
        ###### Logistics & Operations - parking FAQ
        "In order to avoid \"Invalid Status\", it is very important to not tailgate the vehicle that is trying to enter or exit the premise. Do ensure that the barricade is fully lowered before attempting to enter/exit and ensure that the card reader shows a valid message before proceeding.":[
            "Invalid parking"
            "parking error"
            "How do I avoid getting 'Invalid Status' upon exit or entry to the parking?",
            "Prevent 'Invalid Status' during parking entry and exit",
            "What steps can I take to avoid 'Invalid Status' when entering or exiting parking?",
            "Avoiding 'Invalid Status' at parking entry and exit",
            "Tips for preventing 'Invalid Status' during parking access",
            "How to ensure a valid status during parking entry and exit?",
            "What causes 'Invalid Status' during parking, and how to avoid it?",
            "Procedures to sidestep 'Invalid Status' during parking access",
            "Ensuring a smooth entry and exit without 'Invalid Status' in parking",
            "How can I secure a valid status for parking entry and exit?",
            "Troubleshooting 'Invalid Status' during parking and prevention steps",
        ],
        ###### Logistics & Operations - parking FAQ
        "The charges incurred are for the number of days the vehicle has been parked in the parking area. Thus, the balance you have will not cover for the extra days involved due to insufficient balance.":[
            "I am not able to exit the parking. The reader shows 'Please Top Up' although I have sufficient balance for one-day entry. Why does this happen?",
            "Please Top Up",
            "Trouble exiting parking with 'Please Top Up' message",
            "Unable to leave parking despite having enough balance",
            "Parking exit issue with 'Please Top Up' display",
            "Experiencing problems exiting parking even with sufficient funds",
            "Facing challenges leaving parking due to 'Please Top Up' prompt",
            "Issue at parking exit, 'Please Top Up' message displayed incorrectly",
            "Encountering 'Please Top Up' error upon parking departure",
            "Troubleshoot 'Please Top Up' error during parking exit",
            "Insufficient balance error at parking exit, 'Please Top Up' displayed",
            "Parking exit dilemma: 'Please Top Up' despite having funds",
        ],
        ###### Logistics & Operations - parking FAQ
        "It means either the APCard is not active or there was an improper exit done by the driver before. An improper exit refers to exiting by tailgating too closely to the car in front, and as a result, failing to register the entry/exit on the reader.\n\nWhat should I do? \nPlease visit APU cashier counter and report your issue.":[
            "parking invalid status",
            "I am not able to enter/exit the parking. The reader shows “Invalid Status”. What does it mean and what should I do?",
            "Issue entering/exiting parking with 'Invalid Status' displayed",
            "Unable to access parking due to 'Invalid Status' message",
            "Parking entry/exit problem: 'Invalid Status' on the reader",
            "Encountering 'Invalid Status' when trying to enter/exit parking",
            "Trouble with parking access: 'Invalid Status' on the reader",
            "Getting 'Invalid Status' at parking entry/exit – what does it indicate?",
            "Parking reader shows 'Invalid Status' – need assistance",
            "Seeking help for 'Invalid Status' issue at parking entry/exit",
            "Understanding and resolving 'Invalid Status' during parking access",
            "Parking entry/exit trouble: 'Invalid Status' explanation and solution",
        ],

       # Parking location
        "You may find the entrance of **APU Covered Parking** (Zone A) near Block E, APU Campus. \
            \nThe **APU Open Space Parking** (Zone B) is located on the opposite of APU main entrance. \
            \nThe **APIIT Open Space Parking** (Zone G) is located next to the APPIT campus\
            \n\n*Hint: Send 'parking fee' to me, for parking rates information.*":[
                "Where parking",
                "how to find parking",
                "where is parking zone",
                "Where is zone A",
                "Where is Zone B",
                "Where is Zone G",
                "Where is APIIT parking",
                "Tell me about parking in Zone G at APIIT.",
                "Guide to parking in Zone G at APIIT.",
                "Parking location in Zone A at APIIT.",
                "Parking location in Zone B at APIIT.",
                "APU car location",
                "APU parking location",
                "APU motorcycle location",
                "APIIT car space",
                "APIIT car location",
                "APIIT parking location",
                "APIIT motorcycle location",
                "APIIT car space",
                "outdoor parking locstion",
                "indoor parking location",
                "parking location",
                "How to find Covered Parking at APU Campus?",
                "Tell me about the location of Zone A parking at APU.",
                "Guide to finding parking at APU near Block E.",
                "Where can I find Open Space Parking at APU Campus?",
                "What is the location of Zone B parking at APU?",
                "Where is Zone G located at APU Campus?",
                "Guide to parking in Zone G at APU.",
                "Where can I find parking at APIIT?",
                "Tell me about parking locations at APU Campus.",
                "Where is the APU car parking located?",
                "Where is the APU motorcycle parking located?",
                "Where can I find parking at APIIT for cars?",
                "Where is the APIIT motorcycle parking located?",
                "Where is the outdoor parking located at APU Campus?",
                "Where is the indoor parking located at APU Campus?",
                "Guide to parking locations at APU and APIIT.",
        ],
        
        # Where to wait bus
        "If you would like to take the shuttle service from APU to any location, please take the glass elevator to **APU Campus Connect Lounge** at **Level 1M**, near main entrance":[
            "Where to wait bus at APU",
            "wait bus at apu",
            "wait shuttle at apu",
            "take bus at APU",
            "take shuttle at APU",
            "bus depart at APU",
            "bus arrive at APU"
        ],

        "If you are taking the shuttle service from LRT to APU, please wait the vehicle at **Grab A** point, **Bukit Jalil LRT station**.":[
            "Where to wait bus at LRT",
            "wait bus at LRT",
            "wait shuttle at LRT",
            "take bus at LRT",
            "take shuttle at LRT",
            "bus depart at LRT",
            "bus arrive at LRT"
        ],

        "Effective **8 January 2023**, the shuttle service from Endah to APU is discontinued. \
            \nYou may take the free APU shuttle service from LRT Bukit Jalil or RapidKL T580 bus":[
                "Endah",
                "Endah Promenade",
                "Endah to APU"
        ],
    }

    # Bus schedule algorithm
    if [i for i in ["shuttle", "bus", "from","to", "trip", "go", "trips", "buses", "travel"] if i in str(inp).lower()]:
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
            print("added", added_set)
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
            
        qa[
            "**Travel Pass from/to APU & APIIT**\
                \nLRT : Free\
                \nAPU ⇄ APIIT : Free \
                \nMosque : Free \
                \nFortune Park : RM50\
                \nM Vertica : RM140 \
                \n\n*Please make payment at the Bursary Office, Level 3 APU Campus.\
                \nHint: You may ask me `bus schedule`.*"
            ] = [
                "Travel pass",
                "Travel pass to APU",
                "travel pass to apiit",
                "how much is bus",
                "pay bus",
                "pay shuttle",
                "how much to pay for shuttle",
                "payment bus",
                "payment shuttle",
                "bus fee",
                "bus fees"
            ]
        
    return qa
