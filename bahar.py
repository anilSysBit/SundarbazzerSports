from address.models import Province, District, Municipality

municipalities = {
    "Province No. 1": {
        "Jhapa": ["Bhadrapur", "Mechinagar", "Kankai", "Damak", "Ishworpur"],
        "Ilam": ["Ilam", "Suryodaya", "Fikkal", "Maheshpur", "Siddhithumka"],
        "Morang": ["Biratnagar", "Biratnagar Metropolitan", "Letang", "Rangeli", "Urlabari"],
        "Sunsari": ["Inaruwa", "Duhabi", "Madhyapur", "Prithvi Narayan", "Bishnupur"],
        "Panchthar": ["Phidim", "Bharatpur", "Fikkal", "Limbu"],
    },
    "Province No. 2": {
        "Saptari": ["Rajbiraj", "Barahkshetra", "Dhangadhimai", "Shambhunath", "Kanchanrup"],
        "Dhanusa": ["Janakpur", "Dhanushadham", "Mithila", "Brahmapuri", "Lakshminiya"],
        "Mahottari": ["Jaleshwor", "Harsahi", "Samsi", "Sakhuwa", "Baudhimai"],
        "Sarlahi": ["Malangawa", "Ichchhpur", "Bairiya", "Harlalka", "Ramnagar"],
    },
    "Bagmati Province": {
        "Kathmandu": ["Kathmandu Metropolitan", "Kirtipur", "Bhaktapur", "Lalitpur", "Madhyapur"],
        "Chitwan": ["Bharatpur", "Ratnanagar", "Madi", "Khairahani", "Rapti"],
        "Sindhuli": ["Sindhuli", "Kamalamai", "Dhanusha", "Bijaypur", "Sindhuli Bazaar"],
    },
    "Gandaki Province": {
        "Kaski": ["Pokhara", "Lekhnath", "Damauli", "Baglung", "Gorkha"],
        "Lamjung": ["Lamjung", "Beshisahar", "Jumla", "Tulsipur", "Bhatpou"],
    },
    "Lumbini Province": {
        "Rupandehi": ["Butwal", "Bhairahawa", "Lumbini", "Siddharthanagar", "Devdaha"],
        "Kapilvastu": ["Taulihawa", "Siddharthanagar", "Kauwapur", "Bhairahawa", "Rampur"],
    },
    "Karnali Province": {
        "Surkhet": ["Birendranagar", "Chhinchu", "Salyan", "Dang", "Rukum"],
        "Dailekh": ["Dailekh", "Kavre", "Salyan", "Chhatreshwari", "Narayan"],
    },
    "Sudurpashchim Province": {
        "Kailali": ["Dhangadhi", "Lamki", "Tikapur", "Chauharwa", "Siyari"],
        "Kanchanpur": ["Mahendranagar", "Bheemdatt", "Chaudhary", "Kailali", "Baijanath"],
    },
}

# Populate the database
for province_name, districts in municipalities.items():
    province, created = Province.objects.get_or_create(name=province_name)

    for district_name, municipality_list in districts.items():
        district, created = District.objects.get_or_create(name=district_name, province=province)

        for municipality_name in municipality_list:
            Municipality.objects.get_or_create(name=municipality_name, district=district)

print("Municipalities have been successfully added.")
