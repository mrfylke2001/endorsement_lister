import urllib.request
import time

nation = input("Enter your nation: ")
userRequestURL = "https://www.nationstates.net/cgi-bin/api.cgi?nation=" + nation + "&q=region+endorsements"
userData = str(urllib.request.urlopen(userRequestURL).read())
userEndoList = (userData.split("<ENDORSEMENTS>"))[1].split("</ENDORSEMENTS>")[0]
userEndoArray = userEndoList.split(",")
region = (userData.split("<REGION>"))[1].split("</REGION>")[0].replace(" ", "_").lower()
print("Got region: " + region)

rRequestURL = "https://www.nationstates.net/cgi-bin/api.cgi?region=" + region + "&q=nations"
nationsData = str(urllib.request.urlopen(rRequestURL).read())
nationsList = (nationsData.split("<NATIONS>"))[1].split("</NATIONS>")[0]

nArray = nationsList.split(":")

nationsWA = []
unendorsed = []
for i in range(len(nArray)):
    print("Testing " + nArray[i])
    nRequestURL = "https://www.nationstates.net/cgi-bin/api.cgi?nation=" + nArray[i] + "&q=wa+endorsements"
    nData = str(urllib.request.urlopen(nRequestURL).read())
    nWAStatus = (nData.split("<UNSTATUS>"))[1].split("</UNSTATUS>")[0]
    if nWAStatus != "Non-member":
        print("  " + nArray[i] + " is a WA member.")
        nationsWA.append(nArray[i])
        nEndoList = (nData.split("<ENDORSEMENTS>"))[1].split("</ENDORSEMENTS>")[0]
        nEndoArray = nEndoList.split(",")
        if nation not in nEndoArray:
            print("  User has not endorsed " + nArray[i])
            unendorsed.append(nArray[i])
    time.sleep(0.7)

results = "<!DOCTYPE html><html><body><p>You have not endorsed:</p><ol>"

for x in unendorsed:
    results += f"<li><a href='https://nationstates.net/nation={x}' target='_blank'>{x}</a></li>"
results += "</ol><p>You have not been endorsed by:</p><ol>"

for x in nationsWA:
    if x not in userEndoArray:
        results += f"<li><a href='https://nationstates.net/nation={x}' target='_blank'>{x}</a></li>"
results += "</ol></body></html>"

with open("results.html", "w") as file:
    file.write(results)

print("================")
print("Complete")

#print("You have not endorsed:")
#for i in range(len(unendorsed)):
#    print("  " + unendorsed[i])

#print("================")
#print("You have not been endorsed by:")
#for i in range(len(nationsWA)):
#    if nationsWA[i] not in userEndoArray:
#        print("  " + nationsWA[i])

exiter = input()