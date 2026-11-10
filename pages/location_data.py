import re

STATE_CITY_DATA = {
    "Andhra Pradesh": {
        "prefixes": ["51", "52", "53"],
        "cities": {
            "Visakhapatnam": ["530", "531"],
            "Vijayawada": ["520", "521"],
            "Guntur": ["522"],
            "Tirupati": ["517"],
            "Nellore": ["524"],
            "Kurnool": ["518"],
            "Kakinada": ["533"],
            "Rajahmundry": ["533"],
            "Kadapa": ["516"],
            "Anantapur": ["515"],
            "Eluru": ["534"],
            "Ongole": ["523"],
            "Chittoor": ["517"],
            "Srikakulam": ["532"],
            "Vizianagaram": ["535"],
            "Machilipatnam": ["521"],
            "Tenali": ["522"],
            "Proddatur": ["516"],
            "Nandyal": ["518"],
            "Bhimavaram": ["534"],
            "Other (Andhra Pradesh)": ["51", "52", "53"],
        }
    },
    "Telangana": {
        "prefixes": ["50"],
        "cities": {
            "Hyderabad": ["500", "501"],
            "Secunderabad": ["500"],
            "Warangal": ["506"],
            "Nizamabad": ["503"],
            "Karimnagar": ["505"],
            "Khammam": ["507"],
            "Ranga Reddy": ["500", "501"],
            "Medak": ["502"],
            "Mahabubnagar": ["509"],
            "Nalgonda": ["508"],
            "Adilabad": ["504"],
            "Ramagundam": ["505"],
            "Suryapet": ["508"],
            "Siddipet": ["502"],
            "Miryalaguda": ["508"],
            "Jagtial": ["505"],
            "Mancherial": ["504"],
            "Kothagudem": ["507"],
            "Nirmal": ["504"],
            "Kamareddy": ["503"],
            "Sangareddy": ["502"],
            "Wanaparthy": ["509"],
            "Gadwal": ["509"],
            "Other (Telangana)": ["50"],
        }
    },
    "Tamil Nadu": {
        "prefixes": ["60", "61", "62", "63", "64"],
        "cities": {
            "Chennai": ["600"],
            "Coimbatore": ["641"],
            "Madurai": ["625"],
            "Tiruchirappalli": ["620"],
            "Salem": ["636"],
            "Tirunelveli": ["627"],
            "Erode": ["638"],
            "Vellore": ["632"],
            "Thoothukudi": ["628"],
            "Dindigul": ["624"],
            "Thanjavur": ["613"],
            "Ranipet": ["632"],
            "Sivakasi": ["626"],
            "Karur": ["639"],
            "Ooty (Udhagamandalam)": ["643"],
            "Hosur": ["635"],
            "Kanchipuram": ["631"],
            "Tiruppur": ["641"],
            "Nagercoil": ["629"],
            "Cuddalore": ["607"],
            "Other (Tamil Nadu)": ["60", "61", "62", "63", "64"],
        }
    },
    "Karnataka": {
        "prefixes": ["56", "57", "58", "59"],
        "cities": {
            "Bengaluru": ["560", "562"],
            "Mysuru": ["570", "571"],
            "Hubballi-Dharwad": ["580"],
            "Mangaluru": ["575"],
            "Belagavi": ["590"],
            "Kalaburagi (Gulbarga)": ["585"],
            "Davanagere": ["577"],
            "Ballari": ["583"],
            "Vijayapura": ["586"],
            "Shivamogga": ["577"],
            "Tumakuru": ["572"],
            "Raichur": ["584"],
            "Bidar": ["585"],
            "Udupi": ["576"],
            "Hassan": ["573"],
            "Chikkamagaluru": ["577"],
            "Other (Karnataka)": ["56", "57", "58", "59"],
        }
    },
    "Kerala": {
        "prefixes": ["67", "68", "69"],
        "cities": {
            "Thiruvananthapuram": ["695"],
            "Kochi (Cochin)": ["682"],
            "Kozhikode": ["673"],
            "Kollam": ["691"],
            "Thrissur": ["680"],
            "Kannur": ["670"],
            "Alappuzha": ["688"],
            "Kottayam": ["686"],
            "Palakkad": ["678"],
            "Malappuram": ["676"],
            "Kasaragod": ["671"],
            "Pathanamthitta": ["689"],
            "Wayanad": ["673"],
            "Idukki": ["685"],
            "Other (Kerala)": ["67", "68", "69"],
        }
    },
    "Maharashtra": {
        "prefixes": ["40", "41", "42", "43", "44"],
        "cities": {
            "Mumbai": ["400"],
            "Pune": ["411", "412"],
            "Nagpur": ["440", "441"],
            "Thane": ["400"],
            "Nashik": ["422"],
            "Chhatrapati Sambhajinagar (Aurangabad)": ["431"],
            "Solapur": ["413"],
            "Amravati": ["444"],
            "Navi Mumbai": ["400", "410"],
            "Kolhapur": ["416"],
            "Akola": ["444"],
            "Jalgaon": ["425"],
            "Latur": ["413"],
            "Dhule": ["424"],
            "Ahmednagar": ["414"],
            "Chandrapur": ["442"],
            "Nanded": ["431"],
            "Sangli": ["416"],
            "Satara": ["415"],
            "Wardha": ["442"],
            "Other (Maharashtra)": ["40", "41", "42", "43", "44"],
        }
    },
    "Delhi (NCT)": {
        "prefixes": ["11"],
        "cities": {
            "New Delhi": ["110"],
            "Central Delhi": ["110"],
            "North Delhi": ["110"],
            "South Delhi": ["110"],
            "East Delhi": ["110"],
            "West Delhi": ["110"],
            "North East Delhi": ["110"],
            "North West Delhi": ["110"],
            "South East Delhi": ["110"],
            "South West Delhi": ["110"],
            "Shahdara": ["110"],
            "Other (Delhi)": ["11"],
        }
    },
    "Gujarat": {
        "prefixes": ["36", "37", "38", "39"],
        "cities": {
            "Ahmedabad": ["380", "382"],
            "Surat": ["395"],
            "Vadodara": ["390"],
            "Rajkot": ["360"],
            "Bhavnagar": ["364"],
            "Jamnagar": ["361"],
            "Junagadh": ["362"],
            "Gandhinagar": ["382"],
            "Anand": ["388"],
            "Navsari": ["396"],
            "Morbi": ["363"],
            "Nadiad": ["387"],
            "Bharuch": ["392"],
            "Mehsana": ["384"],
            "Bhuj": ["370"],
            "Valsad": ["396"],
            "Vapi": ["396"],
            "Other (Gujarat)": ["36", "37", "38", "39"],
        }
    },
    "Rajasthan": {
        "prefixes": ["30", "31", "32", "33", "34"],
        "cities": {
            "Jaipur": ["302"],
            "Jodhpur": ["342"],
            "Kota": ["324"],
            "Bikaner": ["334"],
            "Ajmer": ["305"],
            "Udaipur": ["313"],
            "Bhilwara": ["311"],
            "Alwar": ["301"],
            "Bharatpur": ["321"],
            "Sikar": ["332"],
            "Pali": ["306"],
            "Sri Ganganagar": ["335"],
            "Chittorgarh": ["312"],
            "Other (Rajasthan)": ["30", "31", "32", "33", "34"],
        }
    },
    "Uttar Pradesh": {
        "prefixes": ["20", "21", "22", "23", "24", "25", "26", "27", "28"],
        "cities": {
            "Lucknow": ["226"],
            "Kanpur": ["208"],
            "Varanasi": ["221"],
            "Agra": ["282"],
            "Prayagraj (Allahabad)": ["211"],
            "Meerut": ["250"],
            "Ghaziabad": ["201"],
            "Noida / Greater Noida": ["201"],
            "Bareilly": ["243"],
            "Aligarh": ["202"],
            "Moradabad": ["244"],
            "Gorakhpur": ["273"],
            "Ayodhya": ["224"],
            "Jhansi": ["284"],
            "Mathura": ["281"],
            "Muzaffarnagar": ["251"],
            "Other (Uttar Pradesh)": ["20", "21", "22", "23", "24", "25", "26", "27", "28"],
        }
    },
    "West Bengal": {
        "prefixes": ["70", "71", "72", "73", "74"],
        "cities": {
            "Kolkata": ["700"],
            "Howrah": ["711"],
            "Asansol": ["713"],
            "Siliguri": ["734"],
            "Durgapur": ["713"],
            "Bardhaman": ["713"],
            "Malda": ["732"],
            "Darjeeling": ["734"],
            "Kharagpur": ["721"],
            "Other (West Bengal)": ["70", "71", "72", "73", "74"],
        }
    },
    "Madhya Pradesh": {
        "prefixes": ["45", "46", "47", "48"],
        "cities": {
            "Indore": ["452"],
            "Bhopal": ["462"],
            "Jabalpur": ["482"],
            "Gwalior": ["474"],
            "Ujjain": ["456"],
            "Sagar": ["470"],
            "Rewa": ["486"],
            "Satna": ["485"],
            "Other (Madhya Pradesh)": ["45", "46", "47", "48"],
        }
    },
    "Punjab": {
        "prefixes": ["14", "15", "16"],
        "cities": {
            "Ludhiana": ["141"],
            "Amritsar": ["143"],
            "Jalandhar": ["144"],
            "Patiala": ["147"],
            "Bathinda": ["151"],
            "Mohali": ["160"],
            "Pathankot": ["145"],
            "Other (Punjab)": ["14", "15", "16"],
        }
    },
    "Haryana": {
        "prefixes": ["12", "13"],
        "cities": {
            "Gurugram (Gurgaon)": ["122"],
            "Faridabad": ["121"],
            "Panipat": ["132"],
            "Ambala": ["133", "134"],
            "Karnal": ["132"],
            "Rohtak": ["124"],
            "Hisar": ["125"],
            "Sonipat": ["131"],
            "Panchkula": ["134"],
            "Other (Haryana)": ["12", "13"],
        }
    },
    "Bihar": {
        "prefixes": ["80", "81", "82", "84", "85"],
        "cities": {
            "Patna": ["800"],
            "Gaya": ["823"],
            "Bhagalpur": ["812"],
            "Muzaffarpur": ["842"],
            "Purnia": ["854"],
            "Darbhanga": ["846"],
            "Other (Bihar)": ["80", "81", "82", "84", "85"],
        }
    },
    "Odisha": {
        "prefixes": ["75", "76", "77"],
        "cities": {
            "Bhubaneswar": ["751"],
            "Cuttack": ["753"],
            "Rourkela": ["769"],
            "Berhampur": ["760"],
            "Sambalpur": ["768"],
            "Puri": ["752"],
            "Other (Odisha)": ["75", "76", "77"],
        }
    },
    "Assam": {
        "prefixes": ["78"],
        "cities": {
            "Guwahati": ["781"],
            "Silchar": ["788"],
            "Dibrugarh": ["786"],
            "Jorhat": ["785"],
            "Tezpur": ["784"],
            "Other (Assam)": ["78"],
        }
    },
    "Jharkhand": {
        "prefixes": ["81", "82", "83"],
        "cities": {
            "Ranchi": ["834"],
            "Jamshedpur": ["831"],
            "Dhanbad": ["826"],
            "Bokaro": ["827"],
            "Hazaribagh": ["825"],
            "Other (Jharkhand)": ["81", "82", "83"],
        }
    },
    "Chhattisgarh": {
        "prefixes": ["49"],
        "cities": {
            "Raipur": ["492"],
            "Bhilai": ["490"],
            "Bilaspur": ["495"],
            "Korba": ["495"],
            "Durg": ["491"],
            "Other (Chhattisgarh)": ["49"],
        }
    },
    "Uttarakhand": {
        "prefixes": ["24", "26"],
        "cities": {
            "Dehradun": ["248"],
            "Haridwar": ["249"],
            "Roorkee": ["247"],
            "Haldwani": ["263"],
            "Pantnagar": ["263"],
            "Rishikesh": ["249"],
            "Other (Uttarakhand)": ["24", "26"],
        }
    },
    "Himachal Pradesh": {
        "prefixes": ["17"],
        "cities": {
            "Shimla": ["171"],
            "Dharamshala": ["176"],
            "Palampur": ["176"],
            "Solan": ["173"],
            "Other (Himachal Pradesh)": ["17"],
        }
    },
    "Jammu and Kashmir": {
        "prefixes": ["18", "19"],
        "cities": {
            "Srinagar": ["190"],
            "Jammu": ["180"],
            "Anantnag": ["192"],
            "Baramulla": ["193"],
            "Other (Jammu and Kashmir)": ["18", "19"],
        }
    },
    "Goa": {
        "prefixes": ["40"],
        "cities": {
            "Panaji": ["403"],
            "Margao": ["403"],
            "Vasco da Gama": ["403"],
            "Mapusa": ["403"],
            "Other (Goa)": ["40"],
        }
    },
    "Chandigarh": {
        "prefixes": ["16"],
        "cities": {
            "Chandigarh": ["160"]
        }
    },
    "Puducherry": {
        "prefixes": ["60"],
        "cities": {
            "Puducherry": ["605"],
            "Karaikal": ["609"],
            "Other (Puducherry)": ["60"]
        }
    },
    "Tripura": {
        "prefixes": ["79"],
        "cities": {
            "Agartala": ["799"],
            "Other (Tripura)": ["79"]
        }
    },
    "Meghalaya": {
        "prefixes": ["79"],
        "cities": {
            "Shillong": ["793"],
            "Tura": ["794"],
            "Other (Meghalaya)": ["79"]
        }
    },
    "Manipur": {
        "prefixes": ["79"],
        "cities": {
            "Imphal": ["795"],
            "Other (Manipur)": ["79"]
        }
    },
    "Nagaland": {
        "prefixes": ["79"],
        "cities": {
            "Kohima": ["797"],
            "Dimapur": ["797"],
            "Other (Nagaland)": ["79"]
        }
    },
    "Mizoram": {
        "prefixes": ["79"],
        "cities": {
            "Aizawl": ["796"],
            "Other (Mizoram)": ["79"]
        }
    },
    "Arunachal Pradesh": {
        "prefixes": ["79"],
        "cities": {
            "Itanagar": ["791"],
            "Other (Arunachal Pradesh)": ["79"]
        }
    },
    "Sikkim": {
        "prefixes": ["73"],
        "cities": {
            "Gangtok": ["737"],
            "Other (Sikkim)": ["73"]
        }
    },
    "Ladakh": {
        "prefixes": ["19"],
        "cities": {
            "Leh": ["194"],
            "Kargil": ["194"]
        }
    },
    "Andaman and Nicobar Islands": {
        "prefixes": ["74"],
        "cities": {
            "Port Blair": ["744"],
            "Other (Andaman and Nicobar)": ["74"]
        }
    },
    "Dadra and Nagar Haveli and Daman and Diu": {
        "prefixes": ["39", "36"],
        "cities": {
            "Daman": ["396"],
            "Silvassa": ["396"],
            "Diu": ["362"]
        }
    },
    "Lakshadweep": {
        "prefixes": ["68"],
        "cities": {
            "Kavaratti": ["682"]
        }
    },
    "Other / International": {
        "prefixes": [],
        "cities": {
            "Other / International City": []
        }
    }
}

INDIAN_STATES = list(STATE_CITY_DATA.keys())


def validate_location(state, city, pincode, field_prefix="Organization"):
    """
    Validates state, city, and pincode consistency.
    - state must be a valid known state.
    - city must be an available city for that state.
    - pincode must be valid 6 digits (if not Other / International) and relate to the city/state.
    Returns (is_valid: bool, error_message: str or None)
    """
    if not state:
        return False, f"Please select a {field_prefix} State."

    if state not in STATE_CITY_DATA:
        return False, f"Invalid {field_prefix} State: {state}."

    if not city:
        return False, f"{field_prefix} City is required."

    # For Other / International, skip Indian pincode checking
    if state == "Other / International":
        if not pincode:
            return False, f"{field_prefix} Postal Code is required."
        return True, None

    # Check that city belongs to the selected state
    cities_in_state = STATE_CITY_DATA[state]["cities"]
    matching_city = None
    for c in cities_in_state:
        if c.lower() == city.strip().lower():
            matching_city = c
            break

    if not matching_city:
        return False, f"City '{city}' is not available in {state}. Please select a valid city under {state}."

    # Validate PIN code format (strictly 6 numeric digits)
    if not pincode:
        return False, f"{field_prefix} PIN Code is required."
    
    clean_pin = str(pincode).strip()
    if not re.match(r'^\d{6}$', clean_pin):
        return False, f"{field_prefix} PIN Code must be exactly 6 numeric digits."

    # Validate that PIN code matches the city prefixes
    city_prefixes = cities_in_state[matching_city]
    state_prefixes = STATE_CITY_DATA[state]["prefixes"]

    if city_prefixes:
        if not any(clean_pin.startswith(pfx) for pfx in city_prefixes):
            expected = ", ".join(city_prefixes)
            return False, f"PIN Code {clean_pin} does not relate to {matching_city}, {state} (expected to start with {expected})."
    elif state_prefixes:
        if not any(clean_pin.startswith(pfx) for pfx in state_prefixes):
            expected = ", ".join(state_prefixes)
            return False, f"PIN Code {clean_pin} does not relate to {state} (expected to start with {expected})."

    return True, None
