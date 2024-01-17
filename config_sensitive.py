import requests, datetime
from copy import deepcopy
from autocorrect import Speller

TOKEN = "MTE4NTQ5MTc1OTQ5Nzc1NjY5Mg.GmDf32.mk_Jiy6oWMa6v_u4aMk_asYr67hDJIfENoqKi8"
ID = ["1185519671873638501", "1185517094385745962"]
spell = Speller(lang='en')

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
            "Where APU",
            "where campus"
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

        # Library(How to reserve a book?)
        "1) Log in to 'My Library Account', https://library.apu.edu.my/ to access the library catalog.\n2) Search and locate the book that you wish to reserve.\
        \n3) Click on the `Place hold` button to reserve the book(s).\n4) Choose your `Pickup location` as APU  Library to collect the book(s).\
        \n5) The librarians or automated email will notify you that the book(s) are ready for collection. Pick up the reserved books within three working days after notification. Your library account shows your reservation data and status.": [
            "reserve book",
            "How do I reserve a book?",
            "How to reserve a book?",
            "Can I reserve a book online?",
            "Can you guide me on reserving a book at APU Library?",
            "How to use 'My Library Account' for reserving a book?",
            "What are the steps to follow to reserve a book at APU Library?",
            "What steps should I follow to hold a book in the library?",
            "What are the steps to reserve a book from the library?",
            "How can I reserve a book",
            "Explain the process of book reservation.",
            "How to pick up a reserved book from APU Library?",
            "How will I know when my reserved book is ready?",
            "How will I get notified about my book reservation?",
            "How do I reserve a book through the library website?",
            "What is the process for online book reservation?",
            "how to reserve book"
        ],

        # Library(Where do I return the borrowed book?)
        "You can either return the borrowed items through the book return kiosk or at the library counter. Refer to the Book Return Kiosk Guide if you are returning the items using the kiosk. \nAlternatively, you can follow the on-screen instructions displayed in the kiosk screen.": [
            "return book",
            "Where do I return the borrowed book?",
            "How do I return the book?",
            "How can I give back borrowed books?",
            "Do I return books at the counter or kiosk?",
            "How do I use the return kiosk?",
            "Where should I go to return the book I borrowed?",
            "Where is the book return kiosk located?",
            "Can I return the borrowed book at the library counter?",
            "Is there a guide I can refer to for using the book return kiosk?",
            "How do I use the book return kiosk to return my borrowed book?",
            "What is the process for returning a borrowed book?",
            "What is the procedure to return a book using the kiosk?",
            "What are the steps for returning books through the kiosk?",
            "Can you guide me on how to return a book at the library?",
            "What are the instructions for returning a book through the kiosk?",
            "What steps should I follow to return a borrowed book at the library?",
            "Where should I return a book after borrowing it?",
        ],

        # Library(How do I collect my library deposit?)
        "1) Login to APSpace.\n2) Go to `Collaboration & Information Resources` and select `e-Forms`. Your browser will open a new tab with the `Exit Application` form at the bottom.\
        \n3) Complete the form by providing the required details and wait for confirmation. You can check the status in the E-forms.\n4) Collect the library deposit from the cashier.": [
            "collect library deposit",
            "collect my library deposit",
            "How to get back my library deposit?",
            "library deposit",
            "How do I collect my library deposit?",
            "What are the steps to retrieve my library deposit?",
            "how to get back my library deposit?",
            "How to get library deposit back?",
            "claim library deposit",
            "How to claim library deposit?",
            "Method to retrieve library deposit?",
            "What is the process to collect my library deposit?",
            "How to collect my library deposit?",
            "I want to collect my library deposit",
            "How to retrieve library deposit?",
            "How to retrieve my library deposit?",
            "Steps to get library deposit back?",
            "Procedure for library deposit collection?",
            "Where and how can I collect my library deposit?",
            "How do I withdraw my library deposit?",
            "How can I reclaim my library deposit easily?",
            "Method to receive my library deposit",
            "How to retrieve my library deposit",
        ],
    
        # Library(Can I borrow FYP/theses/dissertation?)
        "The hard bound FYP / Theses / Dissertation belongs to the library's `Reference Collection`. Any materials belong to this category can only be used within the library and not available for borrowing. However, you may visit the APU’s Institutional Repository (APres) to access hundreds of selected copies of FYPs / Theses/ Dissertation.": [
            "borrow FYP",
            "borrow theses",
            "borrow disseratation",
            "Can I borrow FYP?",
            "Can I borrow theses?",
            "Can I borrow dissertation?",
            "Can I borrow FYP from the library?",
            "Can I borrow theses from the library?",
            "Can I borrow disseratation from the library?",
            "Is it possible to take home the library's FYP?",
            "Is it possible to take home the library's theses?",
            "Is it possible to take home the library's dissertation?",
            "Are the FYP available for borrowing?",
            "Are the theses available for borrowing?",
            "Are the dissertation available for borrowing?",
            "Can I take the FYP home?",
            "Can I take the theses home?",
            "Can I take the dissertation home?",
            "Can FYP be borrowed?",
            "Can theses be borrowed?",
            "Can dissertation be borrowed?",
            "Is it allowed to borrow FYP?",
            "Is it allowed to borrow theses?",
            "Is it allowed to borrow disseration?",
            "Are fyp available for borrowing?",
            "Are theses available for borrowing?",
            "Are dissertation available for borrowing?",
        ],
    
        # Library(How long can I borrow an item?)
        "General circulation (no colored labels attached) – 7 days\n3 days loan (yellow-colored label) – 3 days\nOvernight loan (red-colored label) – 1 day\
        \nStaff circulation (green colored label) – for academic staff only – 120 days (4 months)\nReferences, Current Periodicals, Bound Journals - Only to be used in the library as a reference\
        \nFinal year projects and Theses - Only to be used in the library as a reference\nCD ROMs / DVDs - can be borrowed with the same privileges as the book.\
        \nAPU Wacom Tablet – 1 day\nAPU Lightpad – 1 day": [
            "How long can borrow an item?",
            "How many days can I borrow an item?",
            "What is the loan period for an item?",
            "What is the borrowing period for items with a yellow-colored label?",
            "What is the borrowing period for items with a red-colored label?",
            "What is the borrowing period for items with a green-colored label?",
            "Is there a specific duration for borrowing reference materials in the library?",
            "What is the duration for borrowing an item?",
            "How long can I borrow an APU Lightpad?",
            "How long can I borrow an APU Wacom Tablet?",
            "Can I borrow references?",
            "Can I borrow current periodicals?",
            "Can I borrow bound journals?",
            "What is the borrowing time for final year projects?",
            "What is the borrowing time for theses?",
            "How long can academic staff borrow green-labeled items?",
            "What is the borrowing policy for CD ROMs / DVDs?",
            "What is the loan period for an item",
            "Can I borrow reference materials or journals?",
            "How long can I borrow a general circulation item?",
            "Can academic staff renew green-labeled items?",
            "Is there a time restriction for items with no colored label?",
        ],
    
        # Library(How do I pay my library fines?)
        "You need to come to the library counter and pay your fines by cash. Please ensure to login to your “My Library Account” to check your total outstanding fines and prepare the exact cash to make payment at the library counter.": [
            "pay my library fines",
            "How to pay library fines?",
            "How do I pay my library fines?",
            "Can I pay my library fines in cash?",
            "What is the procedure to pay my library fines?",
            "Where to pay my library fines",
            "Methods to pay library fines",
            "Can I use “My Library Account” to pay my fines online?",
            "How to check my library fines?",
            "Where do I need to go to pay my library fines?",
            "Can I pay my fines with a credit card, or is cash the only option?",
            "Can I pay my fines online, or is it only accepted at the library?",
        ],
    
        # Library(What should I do if I lost a book?)
        "Please report to us immediately once you realize the borrowed item(s)/book(s) is lost by providing the details of the lost item(s) / book(s) `(e.g., name of the item, book title, barcode, date that you borrow, etc.)`. If you fail to report to us, the fines will continue to accrue. Once reported, your library account will be suspended temporarily. The library will allow a grace period of two weeks for you to search for the book(s)/item(s).\
        \n\nYou will not be charged with fines for **two weeks**. If the item is not found after the grace period, we will contact you to discuss one of the following possible options (but not limited to) to resolve the issue.\
        \n`- Replace the lost book with a new copy of the same edition or the latest edition.`\n`- Pay the replacement costs, including the book price and overdue fines owing on the item.`\
        \n\nLibrary staff will fill out the `Missing / Lost Book` form. You will receive the discussion's final verdict via email to guide your future steps. After you clean your account based on the final decision, we will reinstate your library account.": [
            "lost a book",
            "What should I do if I lost a book?",
            "I lost a book",
            "I lost a book I borrowed from the library."
            "What if I lose a library book?",
            "What are my responsibilities if I lose a library book?",
            "What happens if I can't find a book I borrowed from the library?",
            "What do I do if I lose a library book?",
            "How can I report a lost library book?",
            "Will I get fine if I lost a book?",
            "Will fines continue if I don't report a lost book?",
            "How long is the grace period for finding a lost book?",
            "Will my account get suspended if I lost a book",
            "What are my options if I can't find the lost book?",
            "I can't find thr book I borrowed",
            "How do I report a lost item to the library?",
            "Is my account suspended for a lost library item?",
            "How long do I have to find a lost book without fines?",
            "Can I replace a lost book",
            "Options if I can't find the lost book?",
            "How do I report a lost item to the library?",
            "I accidentally lost a book",
            "What action I need to take if I lost a borrowed book?",
        ],

        # Library(Do I have to pay if damaged a book?)
        "Damaged items should be reported to the library immediately to prevent fines from continuing to accrue. The cost of a damaged book depends on the severity of the damage If a loaned item is severely damaged, the student will have to replace it or pay for it at its current market price.\
        \nFor minor damages, the cost of repairing the book would be **RM 12** for soft-cover books and **RM 15** for hardcover titles.": [
            "Do I have to pay if damaged a book?",
            "Do I have to pay for damaging a library book?",
            "What is the fee for damaging a library item?",
            "What should I do if I damage a library book?",
            "How much does it cost to repair a damaged soft-cover book?",
            "How much does it cost to repair a damaged hard-cover book?",
            "What is the cost of repairing a book if damaged",
            "Will I be fined if I don't report a damaged item?",
            "What happens if I damage a library book?",
            "Do I need to report if I damage a library book?",
            "Can I replace a damaged book instead of paying?",
            "Will I be fined for damaging a library book?",
            "Replace or pay for a damaged book?",
        ],

        # Library(How do I check the print collection availability in the Library?)
        "You can either use the OPAC (Online Public Access Catalogue) or the Worldcat Discovery to enter your search terms in the search field available on the library homepage.": [
            "How do I check the print collection availability in the Library?",
            "How to check print collection?",
            "check print collection availability in the Library",
            "print collection availability in the Library",
            "print collection in the library",
            "How do I check if a book is in the library?",
            "How do I know if a book there in the library?",
            "How do I find out if a book is available in the library?",
            "How can I quickly check if a book is in the library's collection?",
            "What is the process for verifying the availability of print collections in the library?",
            "Can you guide me on how to find out if a print collection is available in the library?",
            "Can you guide me on finding a book in the library?",
            "What steps should I follow to check if a print collection is available in the library?",
            "Steps to check print collection is available",
            "What is the method to check the availability of print collections in the library?",
            "Method to check the availability of print collections in the library?",
            "How can I check the availability of print materials in the library?",
            "Is there a way to find out which print collections are currently available at the library?",
            "What should I do to check if a book is available in the library?",
            "How can I find out if a book is in the library's print collection?",
        ],
    
        # Library(Does the library have any magazine collections?)
        "We do have selected print magazine collections displayed on shelves in the library near the staircase area.": [
            "Does the library have any magazine collections?",
            "Are there any magazines available in the library?",
            "Can I find magazines in the library?",
            "Can I find any magazine collections in the library?",
            "Does the library carry any print magazines?",
            "Is there a magazine section in the library?"
            "Are there magazine collections at the library?",
            "Can I access magazines at the library?",
            "Do you have a selection of magazines in the library?",
            "Are there print magazines on the library shelves?",
            "Where can I find magazines in the library?",
            "Is there a magazine section in the library?",
            "Are magazines part of the library's collections?",
            "Magazine collection in library",
            "Where to find magazine collection in library?",
            "Is there a place in the library where I can find magazines?",
            "Are there any printed magazines I can read at the library?"
            "Can I check out magazines from the library?",
            "Where can I locate printed magazines within the library premises?",
            "Are there any physical copies of magazines in the library's inventory?",
            "Is there a magazine corner in the library?",
            "Are there any magazine displays in the library?",
            "Magazine collection in library",
        ],
    
        # Library(Does the library have a fiction book collection?)
        "We do have access to some selected fiction books in print and also as e-books. You can check the availability through  **OPAC (print copy)** and **EBSCOHost (e-books)** as shown below:\
        \n\n__OPAC (Print copy)__\n1) Click `Advance Search`in OPAC and choose the **content** to **Fiction** (Print copy).\n2) Choose any of the titles from the result. Write down the call number and search the book on the shelf.\
        \n\n__EBSCOhost (E-books)__\n1) Click `eBooks` from the top menu and choose **eBook Collection (EBSCOhost).**\n2) Key in any keyword in the search box. You may also browse by category at the side.\
        \n3) Once you find the title you wish to read/view. Click on the title to view the details of the e-books. You may also directly click `'PDF Full Text', 'EPUB Full Text', or 'Full Download'`.": [
            "Does the library have a fiction book collection?",
            "Does the library have a section for fiction books?",
            "Can I find fiction books in the library?",
            "Can I find fiction books in the library's collection?",
            "Is there a fiction book collection available in the library?",
            "Is there a section for fiction books in the library?",
            "Is there a collection of fiction books in the library?",
            "Does the library offer fiction books for borrowing?",
            "Are there any fiction books I can borrow from the library?",
            "Can I access fiction books, either in print or as e-books, at the library?",
            "Do you have a selection of fiction books I can check out?",
            "Do you have any fiction books, either in print or digital format?",
            "Is there a fiction category in the library's inventory?",
            "Where can I find novels in the library?",
            "Are fiction books part of the library resources?",
            "Are fiction books part of the library collection?",
            "Can you guide me on how to locate fiction books in the library?",
            "Does the library carry fiction books?",
            "Are there fiction books in the library collection?",
            "Can I find a collection of fiction books in the library?",
            "fiction book collection in library",
        ],
    
        # Library(How to search for the previous final year project (FYP) that is available in the library?)
        "You can use the **OPAC (Online Public Access Catalogue)** to browse our collection of final year projects (FYP) and theses.\
        \n1) Click on “Advanced Search”.\n2) Key in any keyword and choose either Diploma Project, Undergraduate Theses, Master Theses or PhD Theses. Click the “Search” button\
        \n3) Click on the titles of the collection.\n4) Check the library location and take note of the call number to locate the FYP/Dissertation on the shelf.": [
            "How to search for the previous final year project (FYP) that is available in the library?",
            "How can I find past final year projects in the library's collection?",
            "What is the process for locating previous FYPs in the library?",
            "What is the process to find the final year projects (FYP) in the library?",
            "Can you guide me on searching for past FYPs in the library?",
            "Can you explain how to access the previous FYPs in the library?"
            "Is there a way to access previous final year projects at the library?",
            "How do I look for previous FYPs in the library's catalog?",
            "Can you help me find previous final year projects and theses?",
            "What steps should I take to discover past FYPs in the library?",
            "What steps should I follow to search for the past FYPs available in the library?",
            "How can I use the library resources to find previous FYPs?",
            "Is there a specific method for searching for FYPs in the library?",
            "Where can I find information on previous final year projects?",
            "Can you assist me in locating final year projects from previous years?",
            "Can you guide me on how to locate the previous FYPs in the library?",
            "Where can I find information on the projects completed by students in previous years?",
            "Is there a recommended method for searching and accessing past FYPs in the library?",
            "What steps should I follow to access final year projects and theses from previous years?",
            "What method should I use to find past FYPs in the library?",
            "What is the best way to search for the previous FYPs in the library?",
        ],
    
        # Library(How do I access the e-databases library resources off-campus?)
        "Visit the  APU E-databases from our library website. Click on the title of the e-database of your choice and key in your APKey to access the e-databases.": [
            "How do I access the e-databases library resources off-campus?",
            "How to access the e-databases library resources off-campus? ",
            "Access the e-databases library resources off-campus?",
            "E-database library resources"
            "What is the process for reaching APU E-databases when off-campus?",
            "How can I get to the e-databases on the library website from outside the campus?",
            "Is there a way to access library e-databases remotely?",
            "Can you guide me on reaching APU E-databases off-campus?",
            "What steps should I take to use library e-databases when not on campus?",
            "How do I connect to e-database resources from a location outside the campus?",
            "Is it possible to access library e-databases when I'm not on campus?",
            "What is the procedure for off-campus access to APU E-databases?",
            "Can you explain how to use e-databases from the library website off-campus?",
            "Is there a way to log in and explore e-databases remotely?",
            "How can I get to the e-databases library resources if I am not on campus?",
            "Steps to access the e-databases library resources when not on campus?",
            "Is there a way to log in to APU E-databases from a location outside the university?",
            "Can you explain the steps for accessing e-databases remotely?",
            "How can I connect to APU E-databases off-campus using my APKey?",
            "Is it possible to use library e-databases when I'm not physically on campus?",
            "What steps should I follow to use e-databases off-campus?",
            "How can I log in to the library website and access e-databases when I'm not at the university?",
        ],
    
        # Library(How do I view or search for e-journals and e-books? What about downloading or printing?)
        "E- journals/e-books are usually in `HTML, PDF, or ePUB format`. PDF and ePUB resources require PDF readers and Adobe Digital Edition software, respectively. Format availability is determined by publishers.The availability of the formats are determined by the publishers.\
        \n\nMost of the electronic materials we subscribed to are downloadable and printed, however publishers may limit the quantity of pages/content. Publishers have different restrictions.": [
            "How do I view or search for e-journals and e-books?",
            "How can I download or print e-journals",
            "How to search for e-journals?",
            "How to search for e-books?",
            "How can I download or print e-books ",
            "How can I access or find e-journals and e-books? And is it possible to download or print them?",
            "How do I find or view e-journals and e-books?",
            "Is it possible to access or search for e-journals and e-books?",
            "What steps should I take to view or search for e-journals and e-books?",
            "Can you explain the process for viewing and searching e-journals and e-books?",
            "What are the options for downloading or printing e-journals and e-books?", 
            "How can I access or find e-journals and e-books?",
            "Can you explain the process for viewing and searching e-journals and e-books?",
            "What are the steps to find and view e-journals and e-books",
            "Can I download or print e-journals and e-books?",
            "What is the procedure to search for and view e-journals and e-books?",
            "s it possible to download or print  e-journals and e-books?",
        ],
    
        # Library(How can I access online final year projects (FYP) or theses (APres)?)
        "Staff and students can access it through APres, __https://library.apu.edu.my/apres/__. They are required to login to access the full text content. The public view is currently limited up to the abstract of the content.": [
            "How can I access online final year projects (FYP) or theses (APres)?",
            "How to access online final year projects (FYP) or theses (APres)?",
            "Online final year projects (FYP) or theses (APres)",
            "What steps should I take to view final year projects and theses on APres?",
            "How do I access online FYPs or theses on APres?",
            "Guide me on reaching FYPs and theses through APres.",
            "What's the process for viewing FYPs and theses on APres?",
            "Where can I find and access FYPs and theses online?",
            "How do I log in to APres to view FYPs and theses?",
            "What's the link to access online FYPs and theses?",
            "Guide me on accessing FYPs and theses online through APres.",
            "How can I view full-text FYPs and theses on APres?",
            "What steps should I take to access FYPs and theses?",
            "Is there a quick way to reach online FYPs and theses on APres?",
            "Accessing FYPs and theses on APres: how?",
            "Steps to view online FYPs or theses?",
            "Quick guide to APres for FYPs and theses?",
            "How to log in and see FYPs on APres?",
            "Direct link to APres for FYPs and theses?",
            "Guide me to FYPs and theses on APres.",
            "Accessing APres for FYPs: what's the process?",
            "How to view FYPs and theses online?",
            "APres login for accessing FYPs and theses?",
        ],
    
        # Library(How to check Turnitin similarity report before the official module submission)
        "1) From your Moodle Dashboard, search \"Turnitin\".\n2) Click on the \"Try view similarity…\" link.\n3) Click on Enrol Me.\
        \n4) Click on the following link to open the submission portal.\n5) Click on Add Submission.\n\nOnce done, the status will be set to \"Queued\" wait a little while for your similarity report.": [
            "Access Turnitin",
            "How do I access Turnitin?",
            "How to access Turnitin?",
            "What is the process for entering Turnitin?",
            "How can I reach Turnitin's interface?",
            "Is there a way to log in to Turnitin?",
            "What steps should I take to access Turnitin?",
            "Can you guide me on entering Turnitin?",
            "How do I get to Turnitin?",
            "What's the procedure for logging into Turnitin?",
            "Is there a way to access Turnitin through Moodle?",
            "How can I reach Turnitin's features?",
            "What is the method for logging in to Turnitin via Moodle?",
            "What are the steps to access Turnitin?",
            "Can you guide me on how to use Turnitin?",
            "What’s the process for accessing Turnitin?",
            "How do I navigate to Turnitin?",
            "What is the method to use Turnitin?",
            "How can I log into Turnitin?",
            "How do I open Turnitin?",
            "How can I start using Turnitin?",
            "How to check Turnitin similarity report before the official module submission",
            "I want to check Turnitin similarity report",
            "How to preview Turnitin similarity report before submitting?",
            "Steps to check Turnitin report before official submission?",
            "How to check Turnitin similarity pre-submission?",
            "Steps for Turnitin preview before submission?",
            "How to view Turnitin report before submitting?",
            "Guide me on viewing Turnitin report before submission.",
            "How to check Turnitin similarity before module submission?",
            "Preview Turnitin similarity report",
            "Preview Turnitin report before submitting?",
            "Check Turnitin similarity report",
            "Steps to check Turnitin similarity report",
            "Steps for previewing Turnitin report before official submission?",
            "Can I check Turnitin similarity before submitting the module?",
            "Can I check Turnitin similarity before submitting?",
            "How can I preview the Turnitin similarity report prior to the module submission?",
            "Is there a way to view the Turnitin similarity report before the official submission of my module?",
            "What steps should I take to check the Turnitin similarity report before submitting my module officially?",
            "Can you guide me on accessing the Turnitin similarity report before the official module submission?",
            "How do I review the Turnitin similarity report before I officially submit my module?",
            "Is it possible to check the Turnitin similarity report in advance of the module submission?",
            "What are the steps to view the Turnitin similarity report prior to the official module submission?",
            "Can you guide me on how to access the Turnitin similarity report before submitting the official module?",
            "How can I review the Turnitin similarity report before the final module submission?",
            "What is the procedure to check the Turnitin similarity report before the official module is submitted?",
            "Could you explain how to inspect the Turnitin similarity report before the official module hand-in?",
        ],
    
        # Library(I want to remove/delete a paper from Turnitin. What should I do?)
        "Submit a paper deletion request via Library Helpdesk by providing the Turnitin submission ID of the paper you wish to be removed. The deletion is permanent and papers cannot be retrieved for any reason once it's deleted.": [
            "I want to remove a paper from Turnitin",
            "Remove a paper from Turnitin",
            "Delete a paper from Turnitin",
            "How do I delete a paper from Turnitin?",
            "How to delete a paper from Turnitin?",
            "Steps to remove a paper from Turnitin?"
            "Delete a paper from Turnitin: how?",
            "Guide me on removing a Turnitin paper.",
            "Can I delete a paper from Turnitin?",
            "Process for removing a paper from Turnitin?",
            "What is the procedure for Turnitin paper deletion?",
            "Is there a way to remove a paper from Turnitin?",
            "What should I do to delete a paper from Turnitin?",
            "Can you explain the process of removing a paper from Turnitin?",
            "How can I request the deletion of a paper from Turnitin?",
            "What steps should I follow to delete a paper from Turnitin?",
            "Guide me on removing a paper from Turnitin.",
            "Is it possible to delete a paper from Turnitin?",
            "How do I initiate the removal of a paper from Turnitin?",
            "What's the process for requesting the deletion of a paper from Turnitin?",
            "What steps should I take to delete a paper from Turnitin?",
            "How can I erase my paper from Turnitin?",
            "What is the procedure to remove a document from Turnitin?",
            "I need to delete a submission from Turnitin. How do I go about it?",
            "Can you guide me on how to remove a paper from Turnitin?",
            "What is the method to delete a paper from Turnitin?",
            "How do I go about removing a paper from Turnitin?",
            "What should I do if I want to delete a paper from Turnitin?",
            "What is the process for deleting a paper from Turnitin?",
            "Can you tell me how to delete a paper from Turnitin?",
        ],
    
        # Library(How to download Turnitin assignment with feedback comments?)
        "1) Navigate to the specific assignment and open up the graded paper in the document viewer.\n2) Click on the assignment submitted to open the Turnitin page.\
        \n3) You must select the view you wish to see in your download. If you wish to see your grades and feedback in the downloaded file, ensure you click the text comment button to view the feedback.\n4) Click on the download button.\
        \n\nYour assignment will likely be downloaded into your downloads folder (this is dependent on your browser settings but the default is normally the downloads folder). Open your downloaded file and scroll to the end of the document to find your feedback comments and matches.\
        \n\nIf you select Digital receipt – this is a copy of the submission receipt, which students also received by email.\nIf you select Originally submitted – this is the exact file that you uploaded without any additions.": [
            "How to download Turnitin assignment with feedback comments?",
            "Method to download Turnitin assignment",
            "Download Turnitin assignment",
            "How to download Turnitin assignment with feedback?",
            "Steps for getting Turnitin assignment with feedback?",
            "Download Turnitin assignment with grades and comments."
            "How can I download Turnitin assignment with feedback?",
            "Steps for accessing Turnitin assignment and feedback download?",
            "What is the process for Turnitin assignment download with feedback?",
            "How to get Turnitin feedback?",
            "Steps to download Turnitin feedback?",
            "Downloading Turnitin assignment feedback?",
            "Procedure for Turnitin feedback download?",
            "Guide to download Turnitin comments?",
            "How to access Turnitin feedback?",
            "Turnitin assignment feedback download?",
            "Retrieving feedback from Turnitin?",
            "Turnitin feedback download steps?",
            "Getting feedback from Turnitin?",
        ],
    
        # Library(How can I find my Turntin Submission ID?)
        "To ensure your paper deletion request is fulfilled successfully, **Turnitin ID or Submission ID** must be provided along with your request. Turnitin Support Team will not process any deletion request without IDs.\
        \nEach work you submit to Turnitin will generate an automated Digital Receipt (refer to the image below) which contains all the necessary information about the submission you made including the ID.This will be sent to your official APU email and you can check for the ID by retrieving your Digital Receipt from your email.": [
            "How can I find my Turntin Submission ID?",
            "What's the process for locating my Turnitin Submission ID?",
            "How can I find the ID for my Turnitin submission?",
            "Is there a way to retrieve my Turnitin Submission ID?",
            "What steps should I take to get my Turnitin ID or Submission ID?",
            "Can you guide me on locating my Turnitin Submission ID?",
            "Can you guide me on how to retrieve my Submission ID for Turnitin?",
            "How do I check for my Turnitin Submission ID?",
            "What is the procedure for finding the ID for my Turnitin submission?",
            "Is it possible to get my Turnitin ID or Submission ID from a previous submission?",
            "How to obtain the ID for my Turnitin submission?",
            "Guide me on retrieving my Turnitin Submission ID from the Digital Receipt.",
            "What is the method to locate my Turnitin Submission ID?",
            "What steps should I follow to find my Turnitin Submission ID?",
            "Where can I find the Submission ID for my Turnitin assignment?",
            "How do I get my Submission ID from Turnitin?",
            "How to find my Turnitin Submission ID?",
            "Steps to get my Turnitin ID?",     
            "How to retrieve Turnitin Submission ID?",
            "How to get my Turnitin Submission ID?",
        ],
    
        # Library(How long does the paper deletion request takes?)
        "By default, all Turnitin deletion requests are treated as urgent. Generally, it takes from 24 hours to 2 weeks for the Turnitin Support Team to fulfill your deletion request depending on the request queue.\
        \nAs the support team are based in the UK, US, India & Australia, the time difference between them and Malaysia is also a contributing factor in determining the speed of response. Therefore, it is highly recommended for you to send your deletion request at least 3 weeks prior to your submission deadline.": [
            "How long does the paper deletion request takes?",
            "Deletion request duration?",
            "Time needed for paper deletion request",
            "Turnitin deletion request duration?",
            "Timeframe for Turnitin deletion requests?",
            "Expected time for Turnitin deletion requests?",
            "Turnitin response time for deletion requests?",
            "Turnitin deletion request time estimate?",
            "How much time for Turnitin deletion?",
            "How much time does the paper deletion request takes?",
            "How long for Turnitin to process deletion requests?",
            "How long does it usually take for Turnitin to process deletion requests?",
            "What is the typical duration for Turnitin to fulfill a deletion request?",
            "Can you provide an estimate on the time it takes for Turnitin to process deletion requests?",
            "What's the expected timeframe for Turnitin to handle a paper deletion request?",
            "How much time does it usually take for Turnitin to complete a deletion request?",
            "What is the average processing time for Turnitin paper deletion requests?",
            "What is the expected time frame for a paper deletion request?",
            "Can you tell me the duration for a paper deletion request to be processed?",
            "How much time does it usually take for a paper deletion request to be completed?",
            "What is the typical wait time for a paper deletion request?",
        ],
    
        # Library(How can I reserve a discussion room in the Library?)
        "Library discussion rooms can be booked manually at the library counter on a first-come-first-served basis. Reservations can be made by following the steps below.\
        \n\n1) Proceed to the library counter on the day that you want to use.\n2) Check the availability of room from the staff on duty.\
        \n3) Confirm the booking.\n4) Pass the student/staff ID to the staff on duty before entering the room.\n5) Collect the ID after leaving the room.": [
            "How can I reserve a discussion room in the Library",
            "Reserve a disccusion room in the Library",
            "Reserve a disccusion room",
            "Steps to reserve a room for discussions?",
            "Can I book a discussion room at the Library",
            "Guide me on booking a discussion room in the Library.",
            "What is the process for booking a discussion room in the Library?",
            "What is the process to book a discussion room in the Library?",
            "Can you guide me on reserving a discussion room in the Library?",
            "What steps should I follow to reserve a discussion room in the Library?"
            "How can I reserve a room for discussions at the Library?",
            "Guide me on reserving a discussion room in the Library.",
            "Is there a way to book a room for discussions in the Library?",
            "What steps should I take to secure a discussion room in the Library?",
            "Can you explain how to reserve a discussion room at the Library?",
            "How do I book a discussion room at the Library?",
            "What is the procedure for reserving a room for discussions in the Library?",
            "Is it possible to reserve a room for discussions at the Library?",
            "Guide me on the process of securing a discussion room in the Library.",
            "Can I book a room for discussions in the Library?",
            "Guide me on reserving a discussion room at the Library.",
            "How to book a discussion room at the Library?",
            "Procedure for reserving a room for discussions in the Library?",
            "Is it possible to reserve a discussion room at the Library?",
            "Guide me on securing a discussion room in the Library.",
            "Could you tell me how to secure a discussion room in the Library?",
        ],
    
        # Library(I have a problem with library facilities/services. Where should I report to?)
        "You may raise a helpdesk request from our Library Helpdesk, and we will assist you as soon as possible.\nhttps://apiit.atlassian.net/servicedesk/customer/portal/14.": [
            "I have a problem with library facilities",
            "Report library facilities issues",
            "Report library services issues",
            "Where do I report problems with library services?",
            "Where to report library facility issues?",
            "How to report issues with library services?",
            "Where to seek help for library problems?",
            "How to report problems with library services?",
            "Where to report library facility concerns?",
            "What to do if I have library service issues?",
            "Where to report library issues?",
            "Who to contact for library problems?",
            "Where to raise library concerns?",
            "Who handles library service issues?",
            "Where to report library service problems?",
            "Where to submit library complaints?",
            "Who to notify about library issues?",
            "Where to report problems with the library?",
            "Who to reach out to for library difficulties?",
            "Where to voice library service complaints?",
            "Who to inform about library troubles?",
            "Where to lodge library service issues?",
            "Who to alert about library problems?",
            "Where to communicate library concerns?",
            "Who to advise about library issues?",
            "I am experiencing issues with the library facilities/services. Who can I contact for help?",
            "There is a problem with the library services. Could you guide me on where to report this?",
            "I need to report an issue with the library facilities",
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
            "Where is cashier",
            "where cashier",
            "where is bursary",
            'where bursary',
            "where to pay",
            "how to go cashier",
            "how to go bursary",
            "where to pay cheque",
            "cashier counter",
            "payment counter",
            "bursary location", 
            "cashier location"
        ],  

        ######Logistics & Operations - APU Campus Connect Lounge
        "APU Campus Connect Lounge will serve the purposes for Arrival and Departure for all APU Shuttle Buses. \nIt is located at Level 1M near main entrance, accessible via the glass elevator. \n**Operational Hours:** Monday – Friday: 8.00am – 10.00pm.":[
            "Connect Lounge",
            "Campus Connect Lounge purpose?",
            "How do I access APU Connect Lounge?",
            "What is the purpose of Block E lounge?",
            "Where can I find the Level 1 lounge?",
            "How does APU Shuttle Bus service operate?",
            "What is the purpose of APU Shuttle Bus?",
            "Provide info about Arrival and Departure for APU Shuttle Bus.",
            "How does APU Campus Connect Lounge bus service operate?",
            "Where's the departure lounge for APU bus?",
            "Where to wait for shuttle bus APU?",
            "How to access APU Connect Lounge?",
            "What is the location of APU Connect Lounge?",
            "How is APU Connect Lounge accessed?",
            "What is the purpose of the lounge in Block E?",
            "Where is the Level 1 lounge located?",
            "How are APU Shuttle Buses operated?",
            "How is the APU Shuttle Bus service operated?",
            "What is the purpose of APU Shuttle Bus?",
            "How is APU Connect Lounge accessed?",
            "What is the location of APU Connect Lounge?",
            "Tell me about the APU Shuttle Buses.",
            "Tell me about the APU Shuttle Bus.",
            "How does the APU Shuttle Buses service work?",
            "What is the purpose of the APU Shuttle Bus?",
            "How does the Bus Shuttle service work?",
            "Can you provide information about Arrival and Departure for Bus Shuttle.",
        ],        
    }

    # General payment details
    if [i for i in ["fee", "pay", "paid", "bank"] if i in str(inp).lower()]:
        print("bank alg")
        add_qa = {
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
        }
        qa.update(add_qa)

    # Operation hour
    if [i for i in ["operat", "hour", "time", "open", "close"] if i in str(inp).lower()]:
        print("operation hour alg")
        add_qa = {
            "**Operational Hours of APU Campus Connect Lounge:**\n Monday – Friday: 8.00am – 10.00pm":[
                "Open time APU Campus Connect Lounge",
                "Close time APU Campus Connect Lounge",
                "When does APU Campus Connect Lounge operate?",
                "What are the lounge's opening hours",
                "When does the lounge close",
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
                "What time does the lounge closes on weekdays?",
                "What are the operational hours for APU Campus Lounge?",
                "Operating hours for APU Campus Connect Lounge?",
                "Apu campus connect lounge operation hours?",
                "When does APU Connect Lounge open and close?",
                "Tell me about the operating schedule of APU Lounge.",
                "What are the hours of APU Campus Connect Lounge?",
                "When is APU Campus Lounge accessible on weekdays?",
                "Apu campus connect lounge hours?",
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
        }
        qa.update(add_qa)

    # Contacts algorithm
    if [i for i in ["contact", "call", "phone", "email"] if i in str(inp).lower()]:
        print("contacts alg")
        add_qa = {
            # Library(contact)
            "Library Email: __library@apu.edu.my__\nYou may also call __+603 8992 5207__ (Library Counter) and __+603 8992 5209__ (Reference Desk)": [
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

            # Bursary Contact
            "Bursary Email: __bursary@apu.edu.my__\nYou may also call __+603 8992 5228__":[
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

            # TechCentre Contact
            "IT Helpdesk Email: __assist@apu.edu.my__\nYou may also call __+603 8992 5050__":[
                "How to contact techcentre",
                "What is the contacts of techcentre",
                "What is the email of techcentre",
                "How should I contact techcentre",
                "How to email techcentre",
                "How to call techcentre",
                "email techcentre",
                "call techcentre",
                "contact techcentre",
                "talk to techcentre",
                "I need to email techcentre", 
                "I need to call techcentre",
                "I need to contact techcentre",
                "I want to contact it helpdesk",
                "I want to email it helpdesk",
                "I want to call it helpdesk",
                "it helpdesk contact",
                "it helpdesk email"
            ],

            # Admin Contact
            "Admin Email: __admin@apu.edu.my__\nYou may also call __+603 8992 5250__":[
                "How to contact admin",
                "What is the contacts of admin",
                "What is the email of admin",
                "How should I contact admin",
                "How to email admin",
                "How to call admin",
                "email admin",
                "call admin",
                "contact admin",
                "talk to admin",
                "I need to email admin",
                "I need to call admin",
                "I need to contact admin",
                "I want to contact admin",
                "I want to email admin",
                "I want to call admin",
            ]
        }
        qa.update(add_qa)

    # References algorithm
    if [i for i in ["apa", "reference", "references", "referencing", "citation", "citations", "style", "text"] if i in str(inp).lower()]:
        print("citation alg")
        add_qa = {
            # Library(Which referencing style is used in APU?)
            "At APU, we use `APA referencing style` in our academic writing. \
            \nAPA referencing style is a set of guidelines that helps the writers properly present their works precisely and properly. It contains comprehensive guidelines and specific formatting for all kinds of resources, described in the 7th Edition Publication Manual of the American Psychological Association. \
            \nFor more information on creating a correct reference list, see **APA's Style and Grammar Guidelines (References)** and the library's **Quick APA Referencing Guide**. Workshops on APA referencing are available.\
            \nhttps://apastyle.apa.org/style-grammar-guidelines/references\
            \nhttps://dif7uuh3zqcps.cloudfront.net/wp-content/uploads/sites/91/2021/07/12102004/Quick-APA-Referencing-Guide-2021.pdf.": [
                "meaning of referencing?",
                "apu referencing",
                "What is referencing",
                "What is include in referencing",
                "What is the purpose of referencing?",
                "What are the two main components of referencing?",
                "Can you explain the difference between citation (in-text referencing) and reference list (end-text referencing)?",
                "What is the difference between in-text referencing and end-text referencing?",
                "Why is it necessary to include both citation and reference list in academic writing?",
                "Why is referencing used in academic writing?",
                "Which referencing style is used in APU?",
                "What referencing style does APU use?",
                "What referencing style is use in APU?",
                "What is the preferred referencing style for academic writing at APU?",
                "What resources does APU provide for learning the APA referencing style?",
                "Guides of APU referencing",
                "What referencing style does APU use?",
                "Where can I learn APA referencing at APU?",
                "What APA guides does APU library provide?",
                "What is the standard referencing style at APU?",
                "What are the recommended APA guides at APU?",
                "Where can I find APA Style Guidelines?",
                "Does APU recommend any specific APA guides for referencing?",
                "APA style",
                "What is APA?",
                "What is APA style?",
                "Why use APA style?",
                "What does APA style format?",
                "What is APA referencing style?",
                "Definition of APA referencing style",
                "What is the purpose of the APA referencing style?",
                "Can you describe the APA referencing style?",
                "How does APA style help in writing?",
            ],
        
            # Library(What is the format of APA in-text citation?)
            "There are two different formats of in-text citation, `parenthetical and narrative`. Both formats require two elements: `Author's name and Year of publication`\
            \nParenthetical citations are the more commonly seen form of in-text citations for academic work. Both required reference elements are presented at the end of the sentence in parentheses. E.g. (Belafonte, 2008).\
            \nIn narrative citations, the author's name will be separated from the date. The date must appear immediately after the author's name but in parenthesis. E.g. Belafonte (2008).": [
                "format of APA in-text citation"
                "What is the format of APA in-text citation?",
                "APA in-text citation format",
                "format of APA in-text citation",
                "How many format of APA in-text citation are there?",
                "What are the two different formats of in-text citation?",
                "What are the two formats of in-text citation in APA style?",
                "What is parenthetical citation?",
                "What is narrative citation?",
                "Can you provide an example of a parenthetical citation?",
                "Can you provide an example of a narrative citation?"
                "How does a narrative citation differ from a parenthetical citation?",
                "Explain the difference between parenthetical and narrative citations in APA?",
            ],
        
            # Library(How to write the APA reference list?)
            "1) Begin the reference list on a new page after the text.\n2) Place the section label `References` in bold at the top of the page, centered.\
            \n3) Double-space the reference list, both within and between references. Do not add extra lines between references.\n4) Order references alphabetically, usually by the first letter of the first author's last name.\
            \n5) Include the authors' first and middle initials (if they have them). Do not write out first or middle names.\n6)Write author names in the inverted format so that the last name comes first, followed by a comma and the initials. Place a period and a space after each initial.\
            \n7) Apply a hanging indent for all references using the paragraph-formatting function of your word processing program: The first line is flush left, and all subsequent lines are indented 0.5 inches.\
            \nYou may refer https://library.apiit.edu.my/apa-referencing/": [
                "How to write the APA reference list?",
                "Ways to write APA reference list",
                "How are author names ordered in APA?",
                "How is the References section formatted in APA?",
                "How are references ordered in APA?",
                "How should the authors names be written in an APA reference list?",
                "How is spacing applied in APA references?",
                "What is the indentation style in APA references?",
                "What is the author name format in APA references?",
                "How to format the References section in APA?",
                "What is the APA style for reference indentation?",
                "How to apply spacing in APA references?",
                "Where to start the reference list in APA?",
                "What is the order of references in APA?",
            ],
        
            # Library(How to write an end-text referencing using APA Style?)
            "APA referencing style required four basic information: WHO: Author's name,WHEN: Date of publication,WHAT: Title of work and WHERE: Source data\
            \nFor more information how to write an end-text referencing using APA style,please go to this link: https://apiit.atlassian.net/wiki/spaces/LIB/pages/1968767097/How+to+write+an+end-text+referencing+using+APA+Style\
            \n\n__Important notes__\n-Primary title should be written in italic.\n-For the journal article, the journal title should be written in Italic while the article title will be written in a normal text.\nResources that are available online, please use the DOI or URL as their source of data.": [
                "How to write an end-text referencing using APA Style?",
                "end-text referencing using APA Style",
                "Ways to write an end-text referencing using APA Style",
                "What are the four components needed for APA referencing?",
                "How should the primary title be presented in APA end-text referencing?",
                "Where can I find more details on writing end-text referencing in APA style?",
                "How should online resources be cited in APA",
                "Which title is italicized in a journal article citation, and which one is in normal text?",
                "How should the primary title be presented in APA end-text referencing?",
                "How to cite online resources in APA style?",
            ],
        }
        qa.update(add_qa)

    # Car Park algorithm
    if [i for i in ["car", "park", "parking", "zone"] if i in str(inp).lower()]:
        print("parking alg")
        add_park = {
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
                    ###### Academic Administration - Student Handbook 
        "You may download the handbock through the link \n <https://apiit.atlassian.net/wiki/x/CQCARw>":[
            "APU Student Handbook",
            "Campus Handbook",
            "University Guidebook",
            "APU Regulations",
            "Student Policies Guide",
            "APIIT Student Handbook", 
            "Institute Handbook",
            "APIIT Rules Book",
            "Engineering Student Supplementary Document",
            "Student Reference Guide",
            "Engineering Handbook"
        ],

        ##### Academic Administration (General) - New Class Code Structure
        "This new structure was rolled out in early 2021 \n Bellow are the structure\n\n\
        ```yaml Cluster ``` ___ ```css ModuleCode-ClassType ``` ___ ```diff ClassStartDate```\n\
        ```yaml APP ```___```css CT042-3-1-IDB-LAB-1 ```___```diff 2020-06-14 ``` ":[
            "New Class Code Structure",
            "Class Code Structure",
            "example Class Code",
            "What is the new class code structure?",
            "Tell me about the class code format.",
            "What does the class code APP stand for?",
            "Explain the structure Cluster ___ ModuleCode-ClassType ___ ClassStartDate.",
            "What information does the class code APP___CT042-3-1-IDB-LAB-1___2020-06-14 convey?",
            "Guide to understanding the new class code structure.",
            "What is the significance of each component in the class code?",
            "How can I interpret the Cluster, ModuleCode, ClassType, and ClassStartDate in the class code?",
            "Tell me about the class code APP___CT042-3-1-IDB-LAB-1___2020-06-14.",
            "What does CT042 represent in the class code?",
            "How is the ClassType determined in the class code?",
            "When does the class with the code APP___CT042-3-1-IDB-LAB-1 start?",
        ],

        "Benefits for Lecturers\n\
        1. Automatic Class Code Detection in Attendix (no manual selection required)\n\
        2. Different Class Code for LAB and Tutorial (no manual selection required)\n\
        3. Future report to understand how many class codes have been taught during the year(LAB-16). ":[
            "Benefits for Lecturers with New Class Code Structure",
            "Benefits for Teachers with New Class Code Structure",
            "What are the benefits for lecturers with the new class code structure?",
            "How does the new class code structure benefit lecturers?",
            "Tell me about the advantages of the new class code structure for lecturers.",
            "Explain the automatic class code detection in Attendix for lecturers.",
            "How does the new class code structure eliminate the need for manual code selection in Attendix?",
            "What is the significance of having different class codes for LAB and Tutorial?",
            "How does the new class code structure eliminate the manual selection requirement for LAB and Tutorial codes?",
            "Can you elaborate on the future reporting feature for lecturers using class codes (LAB-16)?",
            "How does the new class code structure facilitate future reporting for lecturers?",
            "Guide to understanding the benefits of the new class code structure for lecturers.",
            "Tell me about the automatic detection feature in Attendix related to class codes.",
            "How does the new structure enhance the reporting capabilities for lecturers?",
            "What advantages does the new class code structure bring to lecturers regarding attendance tracking?",
        ],

        "Benefits for Academic Administration\n\
        1. Automatic Class Code Generation.\n\
        2. Automatic Class Creation in SIS (no more event list). \n\
        3. Automatic Student Enrollment to the Classes.\n\
        4. Automatic Intake Grouping of the Students.  \n\
        5. Sending Notification to Students.":[
            "advantage new class code structure for for academic admin",
            "What are the benefits for academic administration with the new class code structure?",
            "How does the new class code structure benefit academic administration?",
            "Tell me about the advantages of the new class code structure for academic administration.",
            "Explain the process of automatic class code generation.",
            "How does the new class code structure eliminate the need for manual code generation in academic administration?",
            "Describe the automatic class creation feature in SIS for academic administration.",
            "How does the new class code structure eliminate the use of the event list for academic administration?",
            "Explain the automatic student enrollment process in classes for academic administration.",
            "What is the significance of automatic intake grouping of students with the new class code structure?",
            "How does the new class code structure facilitate automatic intake grouping of students for academic administration?",
            "Tell me about the process of sending notifications to students with the new class code structure.",
            "How does the new class code structure streamline the notification process for academic administration?",
            "Guide to understanding the benefits of the new class code structure for academic administration.",
            "What advantages does the new class code structure bring to academic administration in terms of efficiency?",
            "Can you elaborate on how automatic processes improve administrative tasks with the new class code structure?",
        ],

        "**Why cluster code has been added to the class code?**\n\
        'Because the same module being taught at the exact start date can carry the same lecture, tutorial, or lab class number. As so, the cluster is at the beginning of the code to ensure there are no duplicate codes created in GIMS.' ":[
            "Reason for Adding Cluster Code to Class Code",
            "Why was the cluster code added to the class code?",
            "What is the purpose of including the cluster code in the class code?",
            "Can you explain why the cluster code is part of the class code?",
            "Tell me about the reason behind adding the cluster code to the class code.",
            "Why is the cluster code placed at the beginning of the class code?",
            "What problem does the cluster code solve in GIMS?",
            "How does adding the cluster code prevent duplicate codes in GIMS?",
            "Guide to understanding the rationale behind including the cluster code in the class code.",
            "How does the presence of the cluster code ensure unique class codes in GIMS?",
            "What role does the cluster code play in avoiding code duplications for the same module?",
            "Explaining the importance of the cluster code in ensuring unique class codes in GIMS.",
        ],

        "**Why haven't we added the intakes to the class code?**\n\
         1. Merging intakes / separating intakes until week 3 or 4:\n\ ```As we are aware the numbers of the students may change in a class and therefore the classes may need separating or merging meaning the above class code may need to change on week 3 or 4 to \n APP___CT042-3-1-IDB-LAB-1___2020-06-14___CT \n APP___CT042-3-1-IDB-LAB-1___2020-06-14___SE  \n But sometimes the class codes are used across different systems  and the first requirements of the class codes are to be unique (Moodle, APSpace, Appendix, Feedback and etc) it had to have some level of stability.``` \n\n\
        2. The class codes needed to be short: \n\ ``` Some modules are general like MPU or IMT modules which are offered across the schools. These modules may have lecturers with around 30 to 40 intakes in a class the length of the class code would be out of hand. See example below\n Intakes: UC2F2102BM, APD1F2103CE.... \n Module Code: MPU3173-MLY3(FS)-L-2 ```":[
            "Reason for Not Adding Intakes to Class Code",
            "Why haven't intakes been added to the class code?",
            "What is the rationale behind excluding intakes from the class code?",
            "Can you explain the decision to not include intakes in the class code?",
            "Tell me about the reasons for avoiding the addition of intakes to the class code.",
            "How does the potential merging or separating of intakes impact the decision?",
            "Why is it important for class codes to remain stable across different systems?",
            "How does stability play a role in the uniqueness of class codes for various systems?",
            "Guide to understanding the considerations for keeping class codes short.",
            "What challenges arise with longer class codes, especially for general modules with multiple intakes?",
            "How do general modules with numerous intakes affect the length of class codes?",
        ],
        "**Please click the link to view the operation:\n <https://apiit.atlassian.net/wiki/spaces/AA/pages/1626997180/New+Class+Code+Structure#How-Can-Lecturers-Take-Attendance-Easily-without-Knowing-the-Cohorts%3F> ":[
            "Taking Attendance Easily without Knowing Cohorts",
            "How can lecturers take attendance without knowing the cohorts?",
            "What is the process for lecturers to easily take attendance without being aware of the cohorts?",
            "Why is it easy for lecturers to manage attendance with unique and system-generated class codes?",
            "Guide to understanding the role of class codes in simplifying attendance for lecturers.",
            "How does the attendance platform utilize unique class codes to assist lecturers?",
            "How does the uniqueness of class codes contribute to the efficiency of attendance tracking?",
        ],
        }
        qa.update(add_park)

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
                \nMosque *(Friday only)*: Free \
                \nFortune Park : RM50/month\
                \nM Vertica : RM140/month \
                \n\n*For paid travel pass, please make payment at the Bursary Office, Level 3 APU Campus.\
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
        add_qa = {
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
        }
        qa.update(add_qa)
        
    return qa
