def stateName(s):

    dict1={
        "Andaman and Nicobar Islands" : "AN",
        "Andhra Pradesh" :"AP",
        "Arunachal Pradesh"	:"AR",
        "Assam":	"AS",
        "Bihar" :"BR",
        "Chandigarh" : "CH",
        "Chhattisgarh"	:"CG",
        "Dadra and Nagar Haveli and Daman and Diu":	"DD",
        "Delhi"	:"DL",
        "Goa"	:"GA",
        "Gujarat"	:"GJ",
        "Haryana" : "HR",
        "Himachal Pradesh"	:"HP",
        "Jammu and Kashmir"	:"JK",
        "Jharkhand" :"JH",
        "Karnataka":	"KA",
        "Kerala" : "KL",
        "Ladakh"	:"LA",
        "Lakshadweep"	:"LD",
        "Madhya Pradesh"	:"MP",
        "Maharashtra":	"MH",
        "Manipur"	:"MN",
        "Meghalaya":	"ML",
        "Mizoram" : "MZ",
        "Nagaland" : "NL",
        "Odisha"	:"OD",
        "Puducherry"	:"PY",
        "Punjab"	:"PB",
        "Rajasthan" : "RJ",
        "Sikkim":	"SK",
        "Tamil Nadu"	:"TN",
        "Telangana State"	:"TS",
        "Tripura"	:"TR",
        "Uttar Pradesh"	:"UP",
        "Uttarakhand"	:"UK",
        "West Bengal"	:"WB"
    }

    new_dict = dict([(value, key) for key, value in dict1.items()])
    c=s[0:2]
    #print("State : "+new_dict[c]);
    if c in new_dict:
        return "State : " + new_dict[c]
    else:
        return "State : None"
    






