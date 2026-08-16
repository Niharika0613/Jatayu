"""
Programmatic database seed script for Jatayu Trekking Management Application - V2.
Clears the existing SQLite file to recreate the schema, then seeds:
- 1 Admin user (from config)
- 4 Staff users
- 3 Trekker users (for review seeding)
- 12 Travel agencies with varied pricing tiers
- 22 treks categorized by season with route profiles, Komoot itineraries, alerts, terrain, and Pilgrimages
- 12 regional food trails
- 5 restaurant partners
- 5 bookings (some marked as Completed)
- 4 verified user reviews with rating stars and trail conditions
"""

import sys
import os
from datetime import date, datetime
from werkzeug.security import generate_password_hash

# Ensure app can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import User, Trek, LocalFood, Restaurant, TravelAgency, Booking, Review


def seed():
    app = create_app("development")
    with app.app_context():
        # Drop all tables to cleanly wipe data despite database locks
        db.reflect()
        db.drop_all()
        db.create_all()
        print("[*] Cleared and recreated database tables programmatically.")

        # ── 1. Admin Account ──────────────────────────────────────────
        admin = User(
            role="admin",
            full_name=app.config["ADMIN_NAME"],
            email=app.config["ADMIN_EMAIL"],
            password_hash=generate_password_hash(app.config["ADMIN_PASSWORD"]),
            contact_number="9999999999",
            status="active",
            is_active=True,
        )
        db.session.add(admin)
        print(f"[+] Admin created: {app.config['ADMIN_EMAIL']}")

        # ── 2. Staff Accounts ──────────────────────────────────────────
        staff_list = [
            {"full_name": "Rajesh Negi", "email": "rajesh@jatayu.in", "password": "Staff@123", "contact_number": "9812345670", "specialization": "High Altitude Specialist, First Aid Certified", "experience_years": 8, "languages_spoken": "Garhwali, Hindi, English", "regions_expertise": "Garhwal Himalaya"},
            {"full_name": "Dorjee Sherpa", "email": "dorjee@jatayu.in", "password": "Staff@123", "contact_number": "9812345671", "specialization": "Glacial Crossing Expert, Avalanche Rescue Certified", "experience_years": 12, "languages_spoken": "Ladakhi, Bhutia, Hindi", "regions_expertise": "Ladakh, Sikkim"},
            {"full_name": "Imchen Ao", "email": "imchen@jatayu.in", "password": "Staff@123", "contact_number": "9812345672", "specialization": "Northeast Jungles & Survival Specialist", "experience_years": 6, "languages_spoken": "Ao Naga, Nagamese, English", "regions_expertise": "Northeast India"},
            {"full_name": "Shiva Gowda", "email": "shiva@jatayu.in", "password": "Staff@123", "contact_number": "9812345673", "specialization": "Western Ghats Botanist, Serpent Handler", "experience_years": 5, "languages_spoken": "Kannada, Tulu, English", "regions_expertise": "Western Ghats"},
        ]
        
        staff_id_map = {}
        for s in staff_list:
            user = User(
                role="staff",
                full_name=s["full_name"],
                email=s["email"],
                password_hash=generate_password_hash(s["password"]),
                contact_number=s["contact_number"],
                status="active",
                is_active=True,
                specialization=s["specialization"],
                experience_years=s["experience_years"],
                languages_spoken=s["languages_spoken"],
                regions_expertise=s["regions_expertise"]
            )
            db.session.add(user)
            db.session.flush() # Flush to get user.id
            staff_id_map[s["regions_expertise"]] = user.id
            print(f"[+] Staff created: {s['email']}")

        # ── 3. Trekker Accounts (For Seeding Reviews) ──────────────────
        trekkers = [
            {"full_name": "Amit Sharma", "email": "amit@gmail.com", "password": "Password@123", "contact_number": "9876543220", "experience_level": "Intermediate", "blood_group": "O+"},
            {"full_name": "Neha Verma", "email": "neha@gmail.com", "password": "Password@123", "contact_number": "9876543221", "experience_level": "Beginner", "blood_group": "A+"},
            {"full_name": "Rohan Das", "email": "rohan@gmail.com", "password": "Password@123", "contact_number": "9876543222", "experience_level": "Advanced", "blood_group": "AB+"},
        ]
        
        trekker_ids = []
        for t in trekkers:
            user = User(
                role="trekker",
                full_name=t["full_name"],
                email=t["email"],
                password_hash=generate_password_hash(t["password"]),
                contact_number=t["contact_number"],
                status="active",
                is_active=True,
                experience_level=t["experience_level"],
                blood_group=t["blood_group"]
            )
            db.session.add(user)
            db.session.flush()
            trekker_ids.append(user.id)
            print(f"[+] Trekker created: {t['email']}")

        # ── 4. Travel Agencies (Trekking Partners) ────────────────────
        agencies = [
            # Uttarakhand
            {"name": "Garhwal Peaks Adventure", "owner_name": "Sohan Singh", "contact_number": "9411122233", "email": "info@garhwalpeaks.in", "website": "garhwalpeaks.in", "base_city": "Dehradun", "state": "Uttarakhand", "regions_covered": "Garhwal Himalaya", "services": "transport,accommodation,full_package,guide", "certifications": "IMF certified", "year_founded": 2012, "pricing_tier": "budget", "package_starting_price_inr": 6500.0, "status": "approved", "is_verified": True, "avg_rating": 4.5},
            {"name": "Himalayan Nomad Trails", "owner_name": "Vikram Negi", "contact_number": "9411122234", "email": "contact@nomadtrails.in", "website": "nomadtrails.in", "base_city": "Rishikesh", "state": "Uttarakhand", "regions_covered": "Garhwal Himalaya", "services": "full_package,gear_rental,insurance", "certifications": "ATTA member", "year_founded": 2016, "pricing_tier": "mid", "package_starting_price_inr": 9000.0, "status": "approved", "is_verified": True, "avg_rating": 4.7},
            {"name": "Peak Vista Luxury Climbs", "owner_name": "Ananya Joshi", "contact_number": "9411122235", "email": "bookings@peakvista.in", "website": "peakvista.in", "base_city": "Mussoorie", "state": "Mussoorie", "regions_covered": "Garhwal Himalaya", "services": "full_package,accommodation,glamping,porter", "certifications": "IIPT certified", "year_founded": 2020, "pricing_tier": "premium", "package_starting_price_inr": 16000.0, "status": "approved", "is_verified": True, "avg_rating": 4.9},
            
            # Ladakh
            {"name": "Zanskar Frozen Expedition", "owner_name": "Tashi Wangchuk", "contact_number": "9596011122", "email": "tashi@zanskarfrozen.in", "website": "zanskarfrozen.in", "base_city": "Leh", "state": "Ladakh", "regions_covered": "Ladakh", "services": "transport,accommodation,full_package,guide,gear_rental", "certifications": "ALTOA member", "year_founded": 2010, "pricing_tier": "mid", "package_starting_price_inr": 22000.0, "status": "approved", "is_verified": True, "avg_rating": 4.6},
            {"name": "Leh High-Adventure Tours", "owner_name": "Rigzin Namgyal", "contact_number": "9596011123", "email": "rigzin@lehadventure.in", "website": "lehadventure.in", "base_city": "Leh", "state": "Ladakh", "regions_covered": "Ladakh", "services": "full_package,porter,oxygen_cylinders", "certifications": "IMF certified", "year_founded": 2014, "pricing_tier": "premium", "package_starting_price_inr": 35000.0, "status": "approved", "is_verified": True, "avg_rating": 4.8},
            
            # Himachal
            {"name": "Kullu Valley Trekking Co.", "owner_name": "Prem Thakur", "contact_number": "9816022233", "email": "prem@kullutrekking.in", "website": "kullutrekking.in", "base_city": "Manali", "state": "Himachal Pradesh", "regions_covered": "Kullu Valley", "services": "transport,accommodation,full_package,guide", "certifications": "HPTDC approved", "year_founded": 2011, "pricing_tier": "budget", "package_starting_price_inr": 5500.0, "status": "approved", "is_verified": True, "avg_rating": 4.4},
            {"name": "Spiti Edge Adventures", "owner_name": "Tenzin Bodh", "contact_number": "9816022234", "email": "tenzin@spitiedge.in", "website": "spitiedge.in", "base_city": "Kaza", "state": "Himachal Pradesh", "regions_covered": "Kullu Valley", "services": "full_package,gear_rental,accommodation", "certifications": "ATTA member", "year_founded": 2015, "pricing_tier": "mid", "package_starting_price_inr": 8500.0, "status": "approved", "is_verified": True, "avg_rating": 4.7},
            
            # Northeast / Sikkim / West Bengal
            {"name": "Northeast Wanderers", "owner_name": "Khrieleno Tep", "contact_number": "9854123067", "email": "nomads@northeastwanderers.in", "website": "northeastwanderers.in", "base_city": "Dimapur", "state": "Nagaland", "regions_covered": "Northeast India", "services": "transport,accommodation,full_package,guide", "certifications": "ATTA member", "year_founded": 2018, "pricing_tier": "budget", "package_starting_price_inr": 6500.0, "status": "approved", "is_verified": True, "avg_rating": 4.5},
            {"name": "Kanchenjunga Trails", "owner_name": "Phurba Sherpa", "contact_number": "9733055566", "email": "contact@kanchenjungatrails.com", "website": "kanchenjungatrails.com", "base_city": "Gangtok", "state": "Sikkim", "regions_covered": "Sikkim", "services": "full_package,accommodation,guide,porter", "certifications": "TAAS member", "year_founded": 2013, "pricing_tier": "mid", "package_starting_price_inr": 11000.0, "status": "approved", "is_verified": True, "avg_rating": 4.6},
            {"name": "Singalila Eco-Adventures", "owner_name": "Karma Lepcha", "contact_number": "9733055567", "email": "karma@singalilaeco.in", "website": "singalilaeco.in", "base_city": "Darjeeling", "state": "West Bengal", "regions_covered": "West Bengal", "services": "accommodation,guide,eco_tours", "certifications": "GTA registered", "year_founded": 2017, "pricing_tier": "budget", "package_starting_price_inr": 5000.0, "status": "approved", "is_verified": True, "avg_rating": 4.4},
            
            # Karnataka / Western Ghats
            {"name": "Western Ghats Escapes", "owner_name": "Karthik Hegde", "contact_number": "9900112233", "email": "karthik@ghatescapes.in", "website": "ghatescapes.in", "base_city": "Bangalore", "state": "Karnataka", "regions_covered": "Western Ghats", "services": "transport,accommodation,full_package,guide", "certifications": "Karnataka Tourism approved", "year_founded": 2019, "pricing_tier": "budget", "package_starting_price_inr": 3000.0, "status": "approved", "is_verified": True, "avg_rating": 4.5},
            {"name": "Coorg Wild Summit Guild", "owner_name": "Nanda Cariappa", "contact_number": "9900112234", "email": "nanda@coorgwild.in", "website": "coorgwild.in", "base_city": "Madikeri", "state": "Karnataka", "regions_covered": "Western Ghats", "services": "guide,accommodation,homestays", "certifications": "ATTA member", "year_founded": 2015, "pricing_tier": "mid", "package_starting_price_inr": 4800.0, "status": "approved", "is_verified": True, "avg_rating": 4.8},
            
            # Additional Seeding Partners
            {"name": "Devbhumi Pilgrimage Guides", "owner_name": "Ramesh Pandey", "contact_number": "9411122240", "email": "contact@devbhumiguides.in", "website": "devbhumiguides.in", "base_city": "Haridwar", "state": "Uttarakhand", "regions_covered": "Garhwal Himalaya", "services": "guide,accommodation,transport", "certifications": "IMF certified", "year_founded": 2017, "pricing_tier": "budget", "package_starting_price_inr": 5000.0, "status": "approved", "is_verified": True, "avg_rating": 4.6},
            {"name": "Ladakh Himalayan Sherpas", "owner_name": "Sonam Dorje", "contact_number": "9596011130", "email": "info@ladakhsherpas.com", "website": "ladakhsherpas.com", "base_city": "Leh", "state": "Ladakh", "regions_covered": "Ladakh", "services": "guide,full_package,porter,gear_rental", "certifications": "ALTOA member", "year_founded": 2018, "pricing_tier": "mid", "package_starting_price_inr": 18000.0, "status": "approved", "is_verified": True, "avg_rating": 4.7},
            {"name": "Sikkim Himalayan Sherpas", "owner_name": "Mingma Sherpa", "contact_number": "9733055580", "email": "contact@sikkimsherpas.com", "website": "sikkimsherpas.com", "base_city": "Gangtok", "state": "Sikkim", "regions_covered": "Sikkim", "services": "guide,full_package,porter", "certifications": "TAAS member", "year_founded": 2019, "pricing_tier": "premium", "package_starting_price_inr": 15000.0, "status": "approved", "is_verified": True, "avg_rating": 4.9},
            {"name": "Kinner Kailash Expedition Group", "owner_name": "Sanjeev Negi", "contact_number": "9816022244", "email": "info@kinnerkailash.in", "website": "kinnerkailash.in", "base_city": "Shimla", "state": "Himachal Pradesh", "regions_covered": "Kullu Valley", "services": "guide,accommodation,transport", "certifications": "HPTDC approved", "year_founded": 2016, "pricing_tier": "mid", "package_starting_price_inr": 7000.0, "status": "approved", "is_verified": True, "avg_rating": 4.5},
        ]
        
        for a in agencies:
            db.session.add(TravelAgency(**a))
        print(f"[+] Seeding {len(agencies)} travel agencies.")

        # ── 5. Seeding 22 Seasonal Treks (With Itineraries & Pilgrimages) ──
        treks = [
            # ❄️ WINTER TREKS (December - February)
            {
                "name": "Kedarkantha Trek",
                "cover_image": "/kedarkantha.png",
                "location": "Uttarkashi, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Easy",
                "duration_days": 6,
                "total_slots": 20,
                "available_slots": 20,
                "start_date": date(2026, 12, 1),
                "end_date": date(2026, 12, 6),
                "status": "Open",
                "category": "Snow",
                "max_altitude_m": 3810,
                "nearest_railhead": "Dehradun",
                "permit_required": False,
                "best_season": "December–February (Winter Snow)",
                "mythological_significance": "Lord Shiva is believed to have meditated at the summit of Kedarkantha. The name translates to the 'throat of Lord Shiva', linked deeply to the Kedarnath mythos.",
                "cultural_notes": "The local Rawat community resides in wooden homes in Sankri. Local cuisine includes Kafuli (spinach curry) and Jhangora Kheer.",
                "local_tribe_culture": "Rawat and Jaunsari communities",
                "festivals_enroute": "Makar Sankranti (Khichdi Festival) in January",
                "description": "Widely known as India's ultimate winter snow trek. Offers spectacular snow clearings, deodar pine forests, and a beautiful 360-degree Himalayan view from the summit peak.",
                "hidden_places": "Hargad Peak clearing and the offbeat Someshwar Mahadev wooden temple in Jakhol village.",
                "price_inr": 7500.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1860,
                "elevation_profile": "0:1950,2:2300,4:2800,6:3200,8:3810",
                "safety_alerts": "Heavy snow and sub-zero temperatures (-10°C). Carry high-quality microspikes, gaiters, and 4-layer warm clothing. Stay updated on weather advisories.",
                "terrain_breakdown": "Snow:50,Forest:30,Rocky:20",
                "itinerary": "Day 1:Drive from Dehradun to Sankri base camp:180km:1950m|Day 2:Sankri to Juda ka Talab campsite:4km:2700m|Day 3:Juda ka Talab to Kedarkantha Base Camp:4km:3200m|Day 4:Kedarkantha Base to Summit & back to Hargaon:9km:3810m|Day 5:Hargaon to Sankri base camp:4km:1950m|Day 6:Sankri to Dehradun drive:180km:640m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },
            {
                "name": "Chadar Frozen River Trek",
                "cover_image": "/chadar.jpg",
                "location": "Zanskar Gorge, Ladakh",
                "state": "Ladakh",
                "region": "Ladakh",
                "difficulty": "Hard",
                "duration_days": 9,
                "total_slots": 10,
                "available_slots": 10,
                "start_date": date(2026, 1, 15),
                "end_date": date(2026, 1, 23),
                "status": "Open",
                "category": "Snow",
                "max_altitude_m": 3390,
                "nearest_railhead": "Jammu Tawi (Fly to Leh)",
                "permit_required": True,
                "permit_info": "ALTOA Wildlife Permit and Medical fitness certificate from Leh Sonam Norboo Hospital required.",
                "best_season": "January–February (Peak Freeze)",
                "mythological_significance": "The gorge of Zanskar is considered a natural sacred barrier. Ancient myths tell of local Buddhist monks who walked the frozen river during winter to maintain trade links between remote monasteries.",
                "cultural_notes": "A region deeply rooted in Tibetan Buddhism. Trekkers drink butter tea (Gur Gur Chai) and eat Thukpa with the locals.",
                "local_tribe_culture": "Zanskari Buddhists and Bhotia communities",
                "festivals_enroute": "Spituk Gustor Festival in Leh (January mask dance)",
                "description": "An extraordinary journey walking over the frozen Zanskar river. The temperature drops below -20°C, offering a landscape of vertical cliffs and giant frozen waterfalls.",
                "hidden_places": "The hidden caves of Nerak village and the massive 80-foot completely frozen waterfall at Nerak.",
                "price_inr": 28000.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 240,
                "elevation_profile": "0:3150,5:3180,10:3220,15:3280,20:3390",
                "safety_alerts": "Extreme sub-zero climate (up to -25°C). The ice layer (Chadar) can crack or form slush. Waterproof trekking boots and gumboots are mandatory. Carry thermos flask.",
                "terrain_breakdown": "Ice:90,Rocky:10",
                "itinerary": "Day 1:Fly to Leh & acclimatize:0km:3500m|Day 2:Medical check-up in Leh:0km:3500m|Day 3:Drive to Shingra Koma & walk to Tsomo Paldar:3km:3150m|Day 4:Tsomo Paldar to Tibb Cave:15km:3200m|Day 5:Tibb Cave to Nerak Waterfall camp:12km:3390m|Day 6:Nerak back to Tibb Cave:12km:3200m|Day 7:Tibb Cave to Gyalpo & drive to Leh:15km:3500m|Day 8:Buffer day in Leh:0km:3500m|Day 9:Departure from Leh:0km:3500m",
                "staff_id": staff_id_map.get("Ladakh")
            },
            {
                "name": "Brahmatal Trek",
                "cover_image": "/brahmatal.png",
                "location": "Chamoli, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Moderate",
                "duration_days": 6,
                "total_slots": 15,
                "available_slots": 15,
                "start_date": date(2026, 1, 5),
                "end_date": date(2026, 1, 10),
                "status": "Open",
                "category": "Snow",
                "max_altitude_m": 3400,
                "nearest_railhead": "Kathgodam",
                "permit_required": False,
                "best_season": "December–February (Snow trails)",
                "mythological_significance": "Legend says that Lord Brahma chose the shores of the alpine Brahmatal lake to meditate and perform penance, hence its sacred name.",
                "cultural_notes": "Trek starts from Lohajung. The local culture features traditional folk dances like Jhora and Choliya during winter celebrations.",
                "local_tribe_culture": "Kumaoni and Garhwali communities",
                "festivals_enroute": "Basant Panchami in February",
                "description": "A classic winter trek walking through ancient oak and rhododendron forests covered in white snow. Offers stellar views of Mt. Trishul and Mt. Nanda Ghunti.",
                "hidden_places": "Bekaltal, a pristine smaller glacial lake en route surrounded by oak trees that rarely freezes completely.",
                "price_inr": 8000.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1100,
                "elevation_profile": "0:2300,2:2650,4:3100,5:3400",
                "safety_alerts": "Avoid stepping on thin frozen ice layers at Bekaltal or Brahmatal lake shores. High winds near Tilbudi ridge. Keep hydrated.",
                "terrain_breakdown": "Forest:40,Rocky:30,Snow:30",
                "itinerary": "Day 1:Drive Kathgodam to Lohajung base:220km:2300m|Day 2:Lohajung to Bekaltal campsite:6km:2900m|Day 3:Bekaltal to Brahmatal campsite:7km:3100m|Day 4:Brahmatal to Summit & Tilbudi:8km:3400m|Day 5:Tilbudi back to Lohajung:8km:2300m|Day 6:Lohajung drive to Kathgodam:220km:550m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },
            {
                "name": "Dayara Bugyal Trek",
                "cover_image": "/dayara.png",
                "location": "Uttarkashi, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Easy",
                "duration_days": 5,
                "total_slots": 22,
                "available_slots": 22,
                "start_date": date(2026, 2, 10),
                "end_date": date(2026, 2, 14),
                "status": "Open",
                "category": "General",
                "max_altitude_m": 3700,
                "nearest_railhead": "Dehradun",
                "permit_required": False,
                "best_season": "December–February (Snow meadows) / May-June (Lush Green)",
                "mythological_significance": "Bugyals are believed to be the playground of local fairies and mountain deities. Cattle shepherds offer milk to the meadow spirits.",
                "cultural_notes": "Raithal village is famous for sustainable wooden homestays. Shepherds move their cattle here during summer.",
                "local_tribe_culture": "Garhwali farmers and Gujjar nomads",
                "festivals_enroute": "Butter Festival (Anduri) held in August",
                "description": "Among the most expansive high-altitude meadows in India. In winter, these vast green slopes turn into pristine snow slopes ideal for skiing.",
                "hidden_places": "Barnala Lake, a small holy water body en route, and the viewpoint of Bakaria Top.",
                "price_inr": 6800.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1450,
                "elevation_profile": "0:2250,2:2700,4:3200,5:3700",
                "safety_alerts": "Sunny but cold winds. UV exposure is high on open meadows. Use sun protection.",
                "terrain_breakdown": "Grassland:50,Forest:40,Rocky:10",
                "itinerary": "Day 1:Drive Dehradun to Raithal:180km:2250m|Day 2:Raithal to Gui campsite:5km:2900m|Day 3:Gui to Chilapada camp:3km:3200m|Day 4:Chilapada to Dayara Top & back to Gui:8km:3700m|Day 5:Gui to Raithal & drive to Dehradun:5km:640m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },

            # 🌧️ MONSOON TREKS (June - September)
            {
                "name": "Valley of Flowers",
                "cover_image": "/flowers.png",
                "location": "Chamoli District, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Easy",
                "duration_days": 6,
                "total_slots": 25,
                "available_slots": 25,
                "start_date": date(2026, 7, 15),
                "end_date": date(2026, 7, 20),
                "status": "Open",
                "category": "Wildlife",
                "max_altitude_m": 4389,
                "nearest_railhead": "Rishikesh",
                "permit_required": True,
                "permit_info": "National Park entry fee collected at Ghangaria forest checkpost. Carry ID proof.",
                "best_season": "July–September (Monsoon Bloom)",
                "mythological_significance": "In the Ramayana, it is believed Hanuman retrieved the Sanjeevani Buti (life-saving herb) from this valley. Hemkund Sahib, a sacred Sikh shrine, lies adjacent.",
                "cultural_notes": "Trekkers stay in Ghangaria. Pilgrims hike to Hemkund Sahib to pray and bathe in the freezing glacial lake.",
                "local_tribe_culture": "Bhotia and Garhwali communities",
                "festivals_enroute": "Hemkund Yatra pilgrimage season (July–August)",
                "description": "A UNESCO World Heritage site home to over 500 species of wild alpine flowers. The valley blooms during the monsoon rains, transforming into a sea of colors.",
                "hidden_places": "The grave of Margaret Legge, a British botanist who fell here in 1939, located in a quiet corner of the valley.",
                "price_inr": 9200.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 2561,
                "elevation_profile": "0:1828,4:2900,8:3500,10:4389",
                "safety_alerts": "Heavy rains and high landslide risk in Alaknanda gorge. Carrying high-quality rain gear, waterproof bags, and hiking poles is crucial.",
                "terrain_breakdown": "Meadow:60,Rocky:30,Forest:10",
                "itinerary": "Day 1:Drive Rishikesh to Govindghat:290km:1828m|Day 2:Govindghat to Ghangaria village:14km:2900m|Day 3:Ghangaria to Valley of Flowers & back:8km:3500m|Day 4:Ghangaria to Hemkund Sahib & back:10km:4389m|Day 5:Ghangaria back to Govindghat:14km:1828m|Day 6:Govindghat drive to Rishikesh:290km:340m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },
            {
                "name": "Hampta Pass Trek",
                "cover_image": "/hampta.png",
                "location": "Kullu Valley, Himachal Pradesh",
                "state": "Himachal Pradesh",
                "region": "Kullu Valley",
                "difficulty": "Moderate",
                "duration_days": 5,
                "total_slots": 18,
                "available_slots": 18,
                "start_date": date(2026, 7, 1),
                "end_date": date(2026, 7, 5),
                "status": "Open",
                "category": "General",
                "max_altitude_m": 4270,
                "nearest_railhead": "Chandigarh",
                "permit_required": False,
                "best_season": "June–September (Monsoon crossing)",
                "cultural_notes": "A fascinating cultural shift: you cross from the lush Hindu valley of Kullu into the stark, Buddhist desert landscape of Lahaul & Spiti.",
                "local_tribe_culture": "Lahauli Buddhists and Kullu shepherds",
                "festivals_enroute": "Ladarcha Summer Fair in Spiti (July)",
                "description": "One of India's most dramatic landscape crossings. Green pine forests of Manali suddenly transition into the barren moonscape of Spiti.",
                "hidden_places": "The glacial campsite of Shea Goru and the crystal-clear waters of the Chandra Tal lake.",
                "price_inr": 7800.0,
                "route_type": "One-way",
                "elevation_gain_m": 1370,
                "elevation_profile": "0:2900,3:3400,6:4270,9:3350",
                "safety_alerts": "Glacial river crossings can be deep and swift. Cross early in the morning. Spiti region is dry and remote; carry cash.",
                "terrain_breakdown": "Rocky:50,Snow:30,Forest:20",
                "itinerary": "Day 1:Drive Manali to Jobra & hike to Chika:2km:3100m|Day 2:Chika to Balu ka Gera camp:8km:3600m|Day 3:Balu ka Gera to Hampta Pass & Shea Goru:7km:4270m|Day 4:Shea Goru to Chatru & drive to Chandratal:7km:4250m|Day 5:Chatru drive back to Manali:80km:2050m",
                "staff_id": staff_id_map.get("Kullu Valley")
            },
            {
                "name": "Dzukou Valley Trek",
                "cover_image": "/dzukou.png",
                "location": "Viswema, Nagaland",
                "state": "Nagaland",
                "region": "Northeast India",
                "difficulty": "Moderate",
                "duration_days": 4,
                "total_slots": 12,
                "available_slots": 12,
                "start_date": date(2026, 8, 10),
                "end_date": date(2026, 8, 13),
                "status": "Open",
                "category": "Northeast",
                "max_altitude_m": 2452,
                "nearest_railhead": "Dimapur",
                "permit_required": True,
                "permit_info": "Inner Line Permit (ILP) mandatory for non-Nagaland residents. Apply online at nagalandilp.in.",
                "best_season": "June–September (Dzukou Lily blooms)",
                "mythological_significance": "Dzukou means 'cold water' in the Angami Naga language. Naga lore tells of spirits who inhabit the pristine bamboo forests.",
                "cultural_notes": "Homestays near Viswema provide a glimpse of Naga life. Local dishes include smoked pork with bamboo shoots and Galho.",
                "local_tribe_culture": "Angami and Chakhesang Naga tribes",
                "festivals_enroute": "Hornbill Festival (December, Kohima)",
                "description": "Famed for its unique rolling meadows of dwarf bamboo and the rare Dzukou Lily that blooms only here during the monsoon.",
                "hidden_places": "The natural rock caves at the bottom of the valley, and the cold water streams flowing beneath the valley floor.",
                "price_inr": 9500.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 852,
                "elevation_profile": "0:1600,2:2200,4:2452,6:2452",
                "safety_alerts": "Trail starts with a steep, muddy staircase climb at Viswema. Plastic water bottles are strictly banned in the valley. Carry reusable containers.",
                "terrain_breakdown": "Grassland:70,Forest:20,Rocky:10",
                "itinerary": "Day 1:Drive Kohima to Viswema & hike to Dzukou Valley:9km:2452m|Day 2:Explore Dzukou Valley & caves:8km:2452m|Day 3:Dzukou to Jakhama exit & drive to Kohima:11km:1440m|Day 4:Departure from Kohima:0km:1440m",
                "staff_id": staff_id_map.get("Northeast India")
            },

            # ☀️ SUMMER TREKS (March - May)
            {
                "name": "Sandakphu Trek",
                "cover_image": "/sandakphu.jpg",
                "location": "Darjeeling, West Bengal",
                "state": "West Bengal",
                "region": "West Bengal",
                "difficulty": "Moderate",
                "duration_days": 6,
                "total_slots": 15,
                "available_slots": 15,
                "start_date": date(2026, 4, 5),
                "end_date": date(2026, 4, 10),
                "status": "Open",
                "category": "General",
                "max_altitude_m": 3636,
                "nearest_railhead": "New Jalpaiguri (NJP)",
                "permit_required": True,
                "permit_info": "Singalila National Park permit obtained at Maneybhanjan base checkpost.",
                "best_season": "March–May (Rhododendron blooms) / October-November",
                "mythological_significance": "Sandakphu is the peak of the poison plants, referring to the aconite plants that grow here. The Sleeping Buddha range seen from here is considered highly sacred.",
                "cultural_notes": "Passes through the Indo-Nepal border villages. The local people are Nepalese and Sherpas, sharing rich Buddhist traditions.",
                "local_tribe_culture": "Nepalese, Lepcha, and Sherpa communities",
                "festivals_enroute": "Buddha Jayanti in May (monastery mask dances)",
                "description": "Offers views of the 'Sleeping Buddha' formation—a massive mountain range containing four of the five highest peaks in the world (Everest, Kanchenjunga, Lhotse, Makalu).",
                "hidden_places": "The tiny Buddhist monastery in Tumling and the black water lake at Kalipokhri.",
                "price_inr": 9000.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1486,
                "elevation_profile": "0:2150,5:2600,10:3100,15:3636",
                "safety_alerts": "High wind chill factors on Singalila Ridge. Border checks: keep multiple photocopies of ID/passport for Indo-Nepal border checkposts.",
                "terrain_breakdown": "Forest:50,Rocky:40,Grassland:10",
                "itinerary": "Day 1:Drive NJP to Manebhanjan & hike to Tumling:11km:2900m|Day 2:Tumling to Kalipokhri village:13km:3180m|Day 3:Tumling to Sandakphu Summit:6km:3636m|Day 4:Sandakphu to Phalut ridge hike:21km:3600m|Day 5:Phalut to Gorkhey village:15km:2400m|Day 6:Gorkhey to Srikhola & drive to NJP:6km:100m",
                "staff_id": staff_id_map.get("West Bengal")
            },
            {
                "name": "Goechala Trek",
                "cover_image": "/goechala.png",
                "location": "Yuksom, Sikkim",
                "state": "Sikkim",
                "region": "Sikkim",
                "difficulty": "Hard",
                "duration_days": 10,
                "total_slots": 8,
                "available_slots": 8,
                "start_date": date(2026, 4, 20),
                "end_date": date(2026, 4, 30),
                "status": "Open",
                "category": "General",
                "max_altitude_m": 4600,
                "nearest_railhead": "New Jalpaiguri (NJP)",
                "permit_required": True,
                "permit_info": "Kanchenjunga National Park permit required. Arrange through a verified Sikkim agency.",
                "best_season": "April–May (Red Rhododendron trails) / October-November",
                "mythological_significance": "Mt. Kanchenjunga is worshiped as the protective deity of Sikkim. Goechala means 'the lock gate of Goecha', the pass to Kanchenjunga.",
                "cultural_notes": "Trek starts from Yuksom, the ancient capital of Sikkim. Monasteries like Dubdi enroute are rich with ancient manuscripts.",
                "local_tribe_culture": "Bhutia, Lepcha, and Limbu communities",
                "festivals_enroute": "Saga Dawa in June (holy Buddhist festival)",
                "description": "A legendary high-altitude trek. Gets you closer to the massive south face of Mt. Kanchenjunga, walking through dense forests and glacial moraines.",
                "hidden_places": "The holy Samiti Lake, whose crystal-clear waters reflect the peaks of Mt. Pandim.",
                "price_inr": 16500.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 2820,
                "elevation_profile": "0:1780,4:2300,8:2900,12:3500,16:4000,20:4600",
                "safety_alerts": "Very high altitude trek (4,600m). Acclimatization is key. Carry Diamox if recommended. Strict eco-rules in Kanchenjunga National Park.",
                "terrain_breakdown": "Rocky:60,Forest:20,Snow:20",
                "itinerary": "Day 1:Drive NJP to Yuksom base:150km:1780m|Day 2:Yuksom to Sachen campsite:8km:2200m|Day 3:Yuksom to Tshoka village:7km:2900m|Day 4:Tshoka to Dzongri clearing:9km:4030m|Day 5:Dzongri rest & acclimatization:4km:4030m|Day 6:Dzongri to Thansing campsite:8km:3930m|Day 7:Thansing to Lamuney campsite:4km:4150m|Day 8:Lamuney to Goechala Viewpoint & back to Kokchurang:14km:4600m|Day 9:Kokchurang back to Tshoka:16km:2900m|Day 10:Tshoka to Yuksom & drive to NJP:15km:100m",
                "staff_id": staff_id_map.get("Sikkim")
            },
            {
                "name": "Kuari Pass Trek",
                "cover_image": "/kuari.png",
                "location": "Joshimath, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Easy",
                "duration_days": 6,
                "total_slots": 20,
                "available_slots": 20,
                "start_date": date(2026, 5, 10),
                "end_date": date(2026, 5, 15),
                "status": "Open",
                "category": "General",
                "max_altitude_m": 3876,
                "nearest_railhead": "Rishikesh",
                "permit_required": False,
                "best_season": "April–June (Green meadows) / Winter snow",
                "mythological_significance": "The trail is named the 'Lord Curzon Trail' after the British Viceroy who crossed it. Joshimath at the base houses the ancient Adi Shankaracharya temple.",
                "cultural_notes": "Garhwali villages like Kharchi showcase local farming traditions. The culture revolves around sheep rearing and temple fairs.",
                "local_tribe_culture": "Garhwali and Bhotiya communities",
                "festivals_enroute": "Harela Festival in July (crop-sowing celebrations)",
                "description": "Perfect for beginners. Offers views of India's most celebrated peaks: Mt. Nanda Devi, Dronagiri, Hathi Parvat, and Trishul.",
                "hidden_places": "Chitrakantha oak forests, which are completely untouched by tourism, and Gorson Bugyal meadows.",
                "price_inr": 7200.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1876,
                "elevation_profile": "0:2000,3:2500,6:3200,9:3876",
                "safety_alerts": "Mild weather, but sudden rain showers can occur. UV rays are strong at Gorson Bugyal.",
                "terrain_breakdown": "Meadow:50,Forest:40,Rocky:10",
                "itinerary": "Day 1:Drive Rishikesh to Joshimath:250km:1875m|Day 2:Joshimath to Dhak & hike to Guling camp:6km:2900m|Day 3:Guling to Khullara campsite:5km:3200m|Day 4:Khullara to Kuari Pass & back to Tali:11km:3876m|Day 5:Tali to Auli meadows & drive to Joshimath:8km:1875m|Day 6:Joshimath drive back to Rishikesh:250km:340m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },

            # 🍂 AUTUMN & OFFBEAT CULTURAL TREKS (September - November)
            {
                "name": "Roopkund Mystery Lake",
                "cover_image": "/roopkund.jpg",
                "location": "Chamoli, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Hard",
                "duration_days": 8,
                "total_slots": 15,
                "available_slots": 15,
                "start_date": date(2026, 9, 10),
                "end_date": date(2026, 9, 18),
                "status": "Open",
                "category": "Snow",
                "max_altitude_m": 5029,
                "nearest_railhead": "Kathgodam",
                "permit_required": True,
                "permit_info": "Forest permit required from Tharali Forest Division. Medical certificate mandatory.",
                "best_season": "September–October (Lake is visible and not frozen)",
                "mythological_significance": "Local legend says the skeletons at Roopkund belong to King Jasdhaval of Kanauj and his entourage on a pilgrimage to Nanda Devi, struck by a divine hailstorm as punishment.",
                "cultural_notes": "The Nanda Devi Raj Jat Yatra, held once every 12 years, passes through Roopkund. Locals sing folk songs dedicated to Goddess Nanda.",
                "local_tribe_culture": "Garhwali and Bhotiya shepherds",
                "festivals_enroute": "Nanda Devi Raj Jat Yatra (every 12 years)",
                "description": "The Mystery Lake trek. Skeletons dating back to the 9th century lie scattered at the edge of this glacial lake at 5,029m.",
                "hidden_places": "Junargali Summit Ridge, a steep climb above the lake offering views of Trisul and Nanda Ghunti.",
                "price_inr": 14000.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 2729,
                "elevation_profile": "0:2300,3:2900,6:3600,9:4300,12:5029",
                "safety_alerts": "EXTREME ALTITUDE (5,029m) and freezing winds. Risk of altitude sickness (AMS). Keep a slow pace. Skeletons must not be touched or moved.",
                "terrain_breakdown": "Rocky:50,Snow:40,Forest:10",
                "itinerary": "Day 1:Drive Kathgodam to Lohajung:220km:2300m|Day 2:Lohajung to Didna village:8km:2450m|Day 3:Didna to Ali Bugyal meadows:6km:3400m|Day 4:Ali Bugyal to Patar Nachuni:5km:3800m|Day 5:Patar Nachuni to Bhagwabasa cave camp:6km:4300m|Day 6:Bhagwabasa to Roopkund Lake & back to Bedni Bugyal:12km:5029m|Day 7:Bedni Bugyal to Wan & drive to Lohajung:15km:2300m|Day 8:Wan to Lohajung & drive to Kathgodam:220km:550m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },
            {
                "name": "Kumara Parvatha Trek",
                "cover_image": "/kumar.png",
                "location": "Pushpagiri, Coorg, Karnataka",
                "state": "Karnataka",
                "region": "Western Ghats",
                "difficulty": "Hard",
                "duration_days": 2,
                "total_slots": 30,
                "available_slots": 30,
                "start_date": date(2026, 10, 5),
                "end_date": date(2026, 10, 6),
                "status": "Open",
                "category": "Pilgrimage",
                "max_altitude_m": 1712,
                "nearest_railhead": "Mysore",
                "permit_required": True,
                "permit_info": "Forest entry fee paid at the Pushpagiri Forest checkpoint near Bhattara Mane.",
                "best_season": "October–February (Post-Monsoon green)",
                "mythological_significance": "Kumara Parvatha means 'Hill of Kumara (Karthikeya)'. Lord Subrahmanya is said to have meditated here. Kukke Subramanya temple lies at the base.",
                "cultural_notes": "A biodiverse forest hike. Trekkers eat simple meals served on banana leaves at Bhattara Mane (Bhatta's house), a legacy homestay en route.",
                "local_tribe_culture": "Kodava and Gowda communities",
                "festivals_enroute": "Subramanya Shashti in November/December",
                "description": "Karnataka's toughest trek. Leads through dense shola forests, open grasslands, and steep volcanic rock paths to the summit peak.",
                "hidden_places": "Shesha Parvatha, the adjacent peak shaped like a multi-hooded cobra, which serves as a natural viewpoint cliff.",
                "price_inr": 3500.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1562,
                "elevation_profile": "0:150,2:400,5:900,8:1400,10:1712",
                "safety_alerts": "Highly strenuous trail with direct sun exposure on volcanic rocks. Carry at least 3-4 liters of water. Leeches are common in the forest zone after rain.",
                "terrain_breakdown": "Forest:40,Rocky:50,Grassland:10",
                "itinerary": "Day 1:Subramanya temple to Bhattara Mane campsite:7km:900m|Day 2:Bhattara Mane to Summit & back to Subramanya:14km:1712m",
                "staff_id": staff_id_map.get("Western Ghats")
            },
            {
                "name": "Phulara Ridge Trek",
                "cover_image": "/phulara.png",
                "location": "Sankri, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Moderate",
                "duration_days": 6,
                "total_slots": 16,
                "available_slots": 16,
                "start_date": date(2026, 9, 20),
                "end_date": date(2026, 9, 25),
                "status": "Open",
                "category": "General",
                "max_altitude_m": 3690,
                "nearest_railhead": "Dehradun",
                "permit_required": False,
                "best_season": "September–November (Clear skies & ridge walks)",
                "mythological_significance": "Local villages hold weekly assemblies to pray to Someshwar (Shiva) to protect the meadows and cattle from wild leopards.",
                "cultural_notes": "Passing through remote villages, you see women wearing traditional 'Hansa' silver necklaces and cooking over mud hearths.",
                "local_tribe_culture": "Rawat and Jaunsari communities",
                "festivals_enroute": "Makar Sankranti (local fairs in Sankri)",
                "description": "One of India's few ridge treks. You walk along a thin mountain ridge for hours with valleys falling away on both sides.",
                "hidden_places": "Pushtara Bugyal, a massive meadow at the end of the ridge walk that is rarely visited by other groups.",
                "price_inr": 8200.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1740,
                "elevation_profile": "0:1950,2:2400,4:2900,6:3690",
                "safety_alerts": "Ridge walk features steep drops on both sides. Avoid walking in high wind storms. Keep close to the guide.",
                "terrain_breakdown": "Grassland:40,Forest:40,Rocky:20",
                "itinerary": "Day 1:Drive Dehradun to Sankri:180km:1950m|Day 2:Sankri to Sikolta camp:5km:2850m|Day 3:Sikolta to Bhoj Gadi camp:4km:3400m|Day 4:Bhoj Gadi to Ridge Summit & Pushtara:6km:3690m|Day 5:Pushtara to Taluka & drive to Sankri:9km:1950m|Day 6:Sankri drive to Dehradun:180km:640m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },
            {
                "name": "Ranthan Kharak Trek",
                "cover_image": "/ranthan.png",
                "location": "Bageshwar, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Kumaon Himalaya",
                "difficulty": "Moderate",
                "duration_days": 6,
                "total_slots": 14,
                "available_slots": 14,
                "start_date": date(2026, 10, 10),
                "end_date": date(2026, 10, 15),
                "status": "Open",
                "category": "General",
                "max_altitude_m": 3400,
                "nearest_railhead": "Kathgodam",
                "permit_required": False,
                "best_season": "September–November (Rhododendron autumn)",
                "mythological_significance": "Considered the secret walking path of Kumaon deities. Locals pray at tiny stone shrines built under massive oak trees.",
                "cultural_notes": "Rich in Kumaon woodcraft. Homes feature hand-carved window frames called Likhai, showcasing patterns of local flowers and birds.",
                "local_tribe_culture": "Kumaoni community",
                "festivals_enroute": "Harela Autumn Festival (October)",
                "description": "An offbeat forest trail passing through thick rhododendron and oak woodlands, opening up to vast high-altitude grasslands with solitude.",
                "hidden_places": "The ruins of ancient stone shelters en route, once used by Indo-Tibetan salt traders.",
                "price_inr": 9200.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 2200,
                "elevation_profile": "0:1200,3:2000,6:2800,9:3400",
                "safety_alerts": "Remote wilderness trail. Beware of wildlife (leopards/bears). Do not wander off the trail.",
                "terrain_breakdown": "Forest:60,Grassland:30,Rocky:10",
                "itinerary": "Day 1:Drive Kathgodam to Bageshwar:180km:1200m|Day 2:Bageshwar drive to trailhead & hike to camp 1:6km:2100m|Day 3:Camp 1 to Ranthan campsite:7km:2800m|Day 4:Ranthan to Kharak Meadows & back:8km:3400m|Day 5:Ranthan back to Bageshwar:13km:1200m|Day 6:Bageshwar drive to Kathgodam:180km:550m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },
            {
                "name": "Aancha Top Trek",
                "cover_image": "/aancha.png",
                "location": "Chamba, Himachal Pradesh",
                "state": "Himachal Pradesh",
                "region": "Kullu Valley",
                "difficulty": "Easy",
                "duration_days": 5,
                "total_slots": 20,
                "available_slots": 20,
                "start_date": date(2026, 10, 1),
                "end_date": date(2026, 10, 5),
                "status": "Open",
                "category": "General",
                "max_altitude_m": 3200,
                "nearest_railhead": "Pathankot",
                "permit_required": False,
                "best_season": "September–November (Clear autumn views)",
                "mythological_significance": "Aancha Top is associated with local shepherd deities. Gaddi shepherds build small stone towers (Goth) as offerings for safety.",
                "cultural_notes": "Gateway to the nomadic Gaddi culture. Shepherds wear traditional woven wool cords (Dora) around their waist and play wooden flutes.",
                "local_tribe_culture": "Gaddi shepherd community",
                "festivals_enroute": "Minjar Mela (celebrated in Chamba town nearby)",
                "description": "A beautiful, lesser-known meadow trek. Offers views of the Pir Panjal range and Chamba valley without any tourist crowd.",
                "hidden_places": "The seasonal Gaddi nomad camps at the base, where you can drink fresh sheep milk and hear ancient shepherd songs.",
                "price_inr": 6200.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 2200,
                "elevation_profile": "0:1000,2:1800,4:2600,5:3200",
                "safety_alerts": "Nights are cold. Keep warm. Shepherds graze sheep on the top; do not disturb the sheep dogs.",
                "terrain_breakdown": "Grassland:60,Forest:30,Rocky:10",
                "itinerary": "Day 1:Drive Pathankot to Chamba base:120km:1000m|Day 2:Chamba to Village homestay:5km:1800m|Day 3:Village to Aancha camp:6km:2600m|Day 4:Aancha camp to Summit & back to Chamba:9km:3200m|Day 5:Chamba drive to Pathankot:120km:330m",
                "staff_id": staff_id_map.get("Kullu Valley")
            },
            {
                "name": "Pin Bhaba Pass Trek",
                "cover_image": "/pinbhaba.png",
                "location": "Kafnu, Kinnaur, Himachal Pradesh",
                "state": "Himachal Pradesh",
                "region": "Kullu Valley",
                "difficulty": "Hard",
                "duration_days": 8,
                "total_slots": 12,
                "available_slots": 12,
                "start_date": date(2026, 9, 5),
                "end_date": date(2026, 9, 12),
                "status": "Open",
                "category": "General",
                "max_altitude_m": 4890,
                "nearest_railhead": "Shimla",
                "permit_required": True,
                "permit_info": "Kinnaur border area permit required. Arrange in advance at Shimla SDM office.",
                "best_season": "July–September (Monsoon / early Autumn)",
                "mythological_significance": "The pass is a bridge between the Hindu culture of Kinnaur and the Buddhist culture of Spiti. Pin valley is home to the ancient Kungri Monastery.",
                "cultural_notes": "Passing Mudh village, the local Spiti lifestyle revolves around pea farming and cold-desert survival techniques.",
                "local_tribe_culture": "Kinnauri and Spitian communities",
                "festivals_enroute": "Phagli Festival in Kinnaur (mask dance)",
                "description": "A challenging pass crossing. You walk from the green, forested Bhaba valley of Kinnaur, cross a high pass at 4,890m, and enter the dry, barren desert of Pin Valley in Spiti.",
                "hidden_places": "Mudh village, a beautiful whitewashed hamlet in Spiti with a small wooden gompa.",
                "price_inr": 15800.0,
                "route_type": "One-way",
                "elevation_gain_m": 2490,
                "elevation_profile": "0:2400,3:3100,6:3800,9:4890,12:3750",
                "safety_alerts": "Extremely steep loose scree climbs near Pin Bhaba pass. Extreme weather can block the pass. Acclimatize well at Kara camp.",
                "terrain_breakdown": "Rocky:60,Grassland:30,Forest:10",
                "itinerary": "Day 1:Drive Shimla to Kafnu:200km:2400m|Day 2:Kafnu to Mulling campsite:11km:3100m|Day 3:Mulling to Kara campsite:6km:3550m|Day 4:Kara to Pushtirang camp:5km:4100m|Day 5:Acclimatization day at Pushtirang:0km:4100m|Day 6:Pushtirang to Pin Bhaba Pass & Mangrungse:12km:4890m|Day 7:Mangrungse to Mudh village Spiti:16km:3750m|Day 8:Mudh drive back to Manali:200km:2050m",
                "staff_id": staff_id_map.get("Kullu Valley")
            },

            # 🛕 SACRED PILGRIMAGES & YATRA EXPEDITIONS (New 6 additions)
            {
                "name": "Kedarnath Dham Yatra",
                "cover_image": "/kedarnath.jpg",
                "location": "Gaurikund, Garhwal, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Hard",
                "duration_days": 4,
                "total_slots": 30,
                "available_slots": 30,
                "start_date": date(2026, 5, 1),
                "end_date": date(2026, 5, 4),
                "status": "Open",
                "category": "Pilgrimage",
                "max_altitude_m": 3584,
                "nearest_railhead": "Rishikesh / Haridwar",
                "permit_required": True,
                "permit_info": "Mandatory biometric tourist registration via Uttarakhand Tourism Portal (registration.andaman.gov.in/tourism).",
                "best_season": "May–June (Summer) / September-November (Autumn)",
                "mythological_significance": "One of the 12 Jyotirlingas. Pandavas sought Lord Shiva's blessings here for penance after the Mahabharata war. The temple is said to be originally built by the Pandavas.",
                "cultural_notes": "Deeply spiritual atmosphere. Evening Aarti chanting Vedic shlokas echoes through the snow peaks.",
                "local_tribe_culture": "Garhwali Pandits and local Pahadi hoteliers",
                "festivals_enroute": "Badri-Kedar Utsav in June",
                "description": "A sacred steep climb from Gaurikund base camp to the holy Kedarnath temple, flanked by Mandakini river gorge and majestic snow peaks.",
                "hidden_places": "Bhairav Temple, a short 1km steep climb above Kedarnath offering a complete view of the valley, and Chorabari Lake (Gandhi Sarovar).",
                "price_inr": 8500.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1634,
                "elevation_profile": "0:1950,4:2300,8:2750,12:3100,16:3584",
                "safety_alerts": "High altitude climb. Weather changes rapidly; carrying heavy woolens, raincoats, and hiking poles is highly advised. Medical registration mandatory.",
                "terrain_breakdown": "Rocky:70,Paved:20,Forest:10",
                "itinerary": "Day 1:Drive Haridwar to Guptkashi:200km:1319m|Day 2:Drive to Gaurikund & trek to Kedarnath Temple:16km:3584m|Day 3:Morning Darshan, visit Bhairav Temple & trek back to Gaurikund & drive to Guptkashi:16km:1319m|Day 4:Drive back to Haridwar/Rishikesh:200km:340m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },
            {
                "name": "Hemkund Sahib & Ghangaria Yatra",
                "cover_image": "/hemkund.png",
                "location": "Govindghat, Chamoli, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Moderate",
                "duration_days": 5,
                "total_slots": 25,
                "available_slots": 25,
                "start_date": date(2026, 6, 1),
                "end_date": date(2026, 6, 5),
                "status": "Open",
                "category": "Pilgrimage",
                "max_altitude_m": 4329,
                "nearest_railhead": "Rishikesh",
                "permit_required": True,
                "permit_info": "Tourist entry pass required. Register at Rishikesh or online on official UTDB portal.",
                "best_season": "June–September (Monsoon / Summer Yatra)",
                "mythological_significance": "Guru Gobind Singh, the tenth Sikh Guru, is believed to have meditated in a previous life on the banks of this lake surrounded by seven snow peaks.",
                "cultural_notes": "Sikh pilgrims perform selfless service (Kar Seva) enroute. Langar meals are served warm at Ghangaria and Hemkund Sahib Gurudwara.",
                "local_tribe_culture": "Sikh pilgrims and Bhotia traders",
                "festivals_enroute": "Opening ceremony of Hemkund Sahib in late May",
                "description": "High-altitude pilgrimage leading to a sacred crystal-clear lake and the highest Gurudwara in the world, adjacent to the Valley of Flowers.",
                "hidden_places": "The Laxman Temple located next to the Gurudwara, representing the ancient link to Lakshmana's meditation.",
                "price_inr": 8800.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 2501,
                "elevation_profile": "0:1828,4:2300,9:2900,12:3500,14:4329",
                "safety_alerts": "Hemkund Sahib is located at a very high altitude of 4,329m. Steep climb. Oxygen levels are thin. Avoid staying at the top after 2 PM.",
                "terrain_breakdown": "Rocky:60,Meadow:20,Paved:20",
                "itinerary": "Day 1:Drive Rishikesh to Govindghat:290km:1828m|Day 2:Govindghat to Ghangaria village:14km:2900m|Day 3:Ghangaria to Hemkund Sahib & back:12km:4329m|Day 4:Ghangaria back to Govindghat:14km:1828m|Day 5:Govindghat drive to Rishikesh:290km:340m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },
            {
                "name": "Tungnath & Chandrashila Peak",
                "cover_image": "/tungnath.jpg",
                "location": "Chopta, Chamoli, Uttarakhand",
                "state": "Uttarakhand",
                "region": "Garhwal Himalaya",
                "difficulty": "Easy",
                "duration_days": 3,
                "total_slots": 30,
                "available_slots": 30,
                "start_date": date(2026, 10, 10),
                "end_date": date(2026, 10, 12),
                "status": "Open",
                "category": "Pilgrimage",
                "max_altitude_m": 3690,
                "nearest_railhead": "Rishikesh",
                "permit_required": False,
                "best_season": "April–November (Chopta Spring / Autumn)",
                "mythological_significance": "Tungnath is the highest Shiva temple in the world (3,680m), one of the Panch Kedars. Pandavas built it to appease Shiva. Chandrashila means 'Moon Rock', where Moon God Chandra meditated.",
                "cultural_notes": "Quiet Himalayan villages. Priests from Maku village perform daily rituals at the temple during the summer season.",
                "local_tribe_culture": "Garhwali Brahmins and shepherds",
                "festivals_enroute": "Tungnath temple closing festival in November",
                "description": "A short and scenic trail winding through rhododendron forests of Chopta, climbing up to the ancient stone temple and the breathtaking Chandrashila peak.",
                "hidden_places": "The hidden Ravana Shila enroute, where local legend claims King Ravana performed intense penance to Shiva.",
                "price_inr": 4800.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1010,
                "elevation_profile": "0:2680,2:3100,4:3460,5:3690",
                "safety_alerts": "Chopta can get heavy snow in winter. Short but steep climb from Tungnath to Chandrashila peak. Beware of black ice.",
                "terrain_breakdown": "Rocky:40,Meadow:40,Forest:20",
                "itinerary": "Day 1:Drive Rishikesh to Chopta base camp:200km:2680m|Day 2:Trek Chopta to Tungnath & Chandrashila Peak, return to Chopta:10km:3690m|Day 3:Drive Chopta back to Rishikesh:200km:340m",
                "staff_id": staff_id_map.get("Garhwal Himalaya")
            },
            {
                "name": "Shrikhand Mahadev Yatra",
                "cover_image": "/shrikhand.png",
                "location": "Jaon, Kullu, Himachal Pradesh",
                "state": "Himachal Pradesh",
                "region": "Kullu Valley",
                "difficulty": "Hard",
                "duration_days": 6,
                "total_slots": 12,
                "available_slots": 12,
                "start_date": date(2026, 7, 10),
                "end_date": date(2026, 7, 15),
                "status": "Open",
                "category": "Pilgrimage",
                "max_altitude_m": 5227,
                "nearest_railhead": "Shimla",
                "permit_required": True,
                "permit_info": "Strict offline registration at Singhgad base. Mandatory physical checkup and climbing permission from Kullu administration.",
                "best_season": "July–August (Monsoon Yatra only)",
                "mythological_significance": "A natural 75-foot vertical rock monolith (Shivalinga) standing at 5,227m. Bhasmasura performed penance here to get the burning touch power from Shiva.",
                "cultural_notes": "A highly arduous pilgrimage. Trekkers are welcomed with traditional drums (Dhol-Damau) at village shrines.",
                "local_tribe_culture": "Himachali Pahadi community",
                "festivals_enroute": "Shrikhand Mahadev Trust Yatra season (July)",
                "description": "Among the toughest and most revered mountain pilgrimages in India, crossing high-altitude snowfields and vertical boulder walls.",
                "hidden_places": "Bhim Dwar, a spectacular high meadow surrounded by waterfalls, and the sacred glacial pond Nain Sarovar.",
                "price_inr": 18000.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 3377,
                "elevation_profile": "0:1850,5:2900,10:3800,15:4300,20:5227",
                "safety_alerts": "Toughest yatra in Himachal. Extreme altitude (5,227m) and glacier traverses. Medical clearance card and registration mandatory at Singhgad base.",
                "terrain_breakdown": "Rocky:70,Snow:20,Meadow:10",
                "itinerary": "Day 1:Drive Shimla to Jaon village:140km:1850m|Day 2:Trek Jaon to Singhgad & Thachru campsite:12km:3200m|Day 3:Thachru to Bhim Dwar camp:11km:3800m|Day 4:Bhim Dwar to Nain Sarovar & Shrikhand Mahadev Summit, return to Bhim Dwar:16km:5227m|Day 5:Bhim Dwar trek back to Jaon:23km:1850m|Day 6:Jaon drive back to Shimla:140km:2050m",
                "staff_id": staff_id_map.get("Kullu Valley")
            },
            {
                "name": "Kinner Kailash Parikrama",
                "cover_image": "/kinner.png",
                "location": "Tangling, Kinnaur, Himachal Pradesh",
                "state": "Himachal Pradesh",
                "region": "Kullu Valley",
                "difficulty": "Hard",
                "duration_days": 8,
                "total_slots": 10,
                "available_slots": 10,
                "start_date": date(2026, 8, 1),
                "end_date": date(2026, 8, 8),
                "status": "Open",
                "category": "Pilgrimage",
                "max_altitude_m": 4890,
                "nearest_railhead": "Shimla",
                "permit_required": True,
                "permit_info": "Kinnaur district administration permit required. Medical certificate mandatory.",
                "best_season": "August–September (Late Summer / Monsoon)",
                "mythological_significance": "A sacred parikrama (circumambulation) around the home of Lord Shiva in Kinnaur. The 79-foot high Kinner Kailash Shivling changes colors as the day progresses.",
                "cultural_notes": "A unique blend of Kinnauri Hinduism and Tibetan Buddhism. Local wood-carved temples line the path.",
                "local_tribe_culture": "Kinnauri tribal community",
                "festivals_enroute": "Kinner Kailash Yatra season (August)",
                "description": "An intense, high-altitude pilgrimage trek crossing glacial streams and the grueling Charang La pass at 5,200m.",
                "hidden_places": "Charang Village, the last remote village of Kinnaur, famous for its 11th-century Rangrik Rang Buddhist Monastery.",
                "price_inr": 16500.0,
                "route_type": "Loop",
                "elevation_gain_m": 2790,
                "elevation_profile": "0:2100,3:2800,6:3800,9:4890",
                "safety_alerts": "Steep vertical climbs over boulders. Avoid climbing in bad weather. High wind speeds.",
                "terrain_breakdown": "Rocky:60,Snow:30,Forest:10",
                "itinerary": "Day 1:Drive Shimla to Tangling village:220km:2100m|Day 2:Trek Tangling to Maling Khata campsite:8km:2900m|Day 3:Maling Khata to Cave Camp:5km:3800m|Day 4:Cave Camp to Kinner Kailash Shivling Peak & back:10km:4890m|Day 5:Trek back to Tangling:13km:2100m|Day 6:Tangling drive to Reckong Peo:30km:2290m|Day 7:Buffer day at Reckong Peo:0km:2290m|Day 8:Reckong Peo drive to Shimla:250km:2050m",
                "staff_id": staff_id_map.get("Kullu Valley")
            },
            {
                "name": "Amarnath Cave Yatra",
                "cover_image": "/amarnath.png",
                "location": "Baltal, Jammu & Kashmir",
                "state": "Jammu & Kashmir",
                "region": "Ladakh",
                "difficulty": "Hard",
                "duration_days": 5,
                "total_slots": 15,
                "available_slots": 15,
                "start_date": date(2026, 7, 5),
                "end_date": date(2026, 7, 9),
                "status": "Open",
                "category": "Pilgrimage",
                "max_altitude_m": 3888,
                "nearest_railhead": "Jammu Tawi",
                "permit_required": True,
                "permit_info": "Mandatory SASB (Shri Amarnathji Shrine Board) Yatra Permit, Compulsory Health Certificate (CHC), and RFID card.",
                "best_season": "July–August (Shravan Monsoon Yatra)",
                "mythological_significance": "The sacred cave where Lord Shiva narrated the Amar Katha (secrets of immortality) to Goddess Parvati. A natural ice lingam forms inside the cave.",
                "cultural_notes": "A massive national pilgrimage. Local Kashmiri porters and pony-wallas have assisted pilgrims for generations, showing deep communal harmony.",
                "local_tribe_culture": "Kashmiri and Balti Muslim communities (service providers)",
                "festivals_enroute": "Shravani Mela (July–August)",
                "description": "A high-security, high-altitude holy trail along deep gorges and glaciers to the sacred ice cave of Amarnath.",
                "hidden_places": "Sangam, the holy confluence where the Baltal and Pahalgam routes merge, flanked by glaciers.",
                "price_inr": 12500.0,
                "route_type": "Out-and-Back",
                "elevation_gain_m": 1145,
                "elevation_profile": "0:2743,3:3100,7:3400,11:3888",
                "safety_alerts": "Strict security guidelines. Mandatory RFID tags, medical certificate from designated doctors, and daily registration counts.",
                "terrain_breakdown": "Rocky:70,Ice:20,Meadow:10",
                "itinerary": "Day 1:Drive Srinagar to Baltal base camp:100km:2743m|Day 2:Acclimatization and security registration at Baltal:0km:2743m|Day 3:Trek Baltal to Holy Cave Temple & back to Baltal:28km:3888m|Day 4:Drive Baltal back to Srinagar:100km:1585m|Day 5:Departure from Srinagar:0km:1585m",
                "staff_id": staff_id_map.get("Ladakh")
            },
        ]
        
        seeded_treks = []
        for t in treks:
            trek_obj = Trek(**t)
            db.session.add(trek_obj)
            db.session.flush()
            seeded_treks.append(trek_obj)
        print(f"[+] Seeding {len(treks)} treks.")

        # ── 6. Seeding 12 Local Foods ──────────────────────────────────
        foods = [
            # Uttarakhand (Garhwal / Kumaon)
            {"name": "Siddu", "hindi_name": "सिड्डू", "region": "Kullu Valley", "state": "Himachal Pradesh", "category": "bread", "description": "Steamed wheat flatbread stuffed with poppy seeds and hemp paste, eaten warm with hot ghee.", "cultural_significance": "A winter high-calorie staple designed for keeping warm during snow crossings.", "best_eaten_at": "Manali local homestays", "season": "winter", "is_vegetarian": True, "key_ingredients": "Wheat, poppy seeds, ghee, hemp", "photo_url": "/siddu.jpg", "trek_region": "Kullu Valley"},
            {"name": "Kafuli", "hindi_name": "काफुली", "region": "Garhwal Himalaya", "state": "Uttarakhand", "category": "curry", "description": "Fenugreek and spinach gravy thickened with rice paste, cooked in an iron kadhai.", "cultural_significance": "Rich in iron, it is the primary organic energy meal for local farmers.", "best_eaten_at": "Lohajung dhabas", "season": "monsoon", "is_vegetarian": True, "key_ingredients": "Spinach, fenugreek, rice paste", "photo_url": "/kafuli.png", "trek_region": "Garhwal Himalaya"},
            {"name": "Chainsoo", "hindi_name": "चैंसू", "region": "Garhwal Himalaya", "state": "Uttarakhand", "category": "dal", "description": "Dry-roasted black gram dal slow-cooked on iron pots, giving it a rich charcoal flavor.", "cultural_significance": "High protein recovery meal served to trekkers after long hikes.", "best_eaten_at": "Joshimath local kitchen", "season": "year-round", "is_vegetarian": True, "key_ingredients": "Black gram (urad), spices, mustard oil", "photo_url": "/chainsoo.jpg", "trek_region": "Garhwal Himalaya"},
            {"name": "Bal Mithai", "hindi_name": "बाल मिठाई", "region": "Kumaon Himalaya", "state": "Uttarakhand", "category": "sweet", "description": "Brown chocolate-like fudge made from roasted khoya, coated in white sugar balls.", "cultural_significance": "The signature sweet of the Kumaon hills, brought as Prasad from Nanda Devi shrines.", "best_eaten_at": "Bageshwar local markets", "season": "year-round", "is_vegetarian": True, "key_ingredients": "Khoya, sugar balls", "photo_url": "/bal_mithai.png", "trek_region": "Kumaon Himalaya"},

            # Ladakh
            {"name": "Thukpa", "region": "Ladakh", "state": "Ladakh", "category": "soup", "description": "Noodle soup served with local herbs, vegetables, and yak meat/paneer.", "cultural_significance": "The ultimate survival soup for Ladakhi winters.", "best_eaten_at": "Leh market kitchens", "season": "winter", "is_vegetarian": False, "key_ingredients": "Handmade noodles, soup stock, vegetables", "photo_url": "/thukpa.jpg", "trek_region": "Ladakh"},
            {"name": "Gur Gur Chai", "region": "Ladakh", "state": "Ladakh", "category": "beverage", "description": "Salty butter tea made from yak butter, salt, and special tea leaves churned in wood cylinders.", "cultural_significance": "Crucial for preventing chapped lips and altitude dehydration in Leh.", "best_eaten_at": "Chadar base camps", "season": "winter", "is_vegetarian": True, "key_ingredients": "Yak butter, salt, tea leaves", "photo_url": "/gur_gur_chai.jpg", "trek_region": "Ladakh"},
            {"name": "Ladakhi Momo", "hindi_name": "मोमो", "region": "Ladakh", "state": "Ladakh", "category": "snack", "description": "Steamed or fried dumplings stuffed with seasoned vegetables or yak meat, served with fiery red chutney.", "cultural_significance": "A Tibetan-origin comfort food, momos are the lifeline snack at every Ladakhi roadside stall and base camp.", "best_eaten_at": "Leh Main Bazaar & Chilling village", "season": "year-round", "is_vegetarian": False, "key_ingredients": "Flour dough, minced meat/vegetables, onion, garlic, ginger", "photo_url": "/momo.jpg", "trek_region": "Ladakh"},

            # Himachal
            {"name": "Madra", "region": "Kullu Valley", "state": "Himachal Pradesh", "category": "curry", "description": "Slow-cooked chickpeas in a rich yogurt and spices gravy, seasoned with dried fruits.", "cultural_significance": "The main component of Himachali Dham, served during temple festivals.", "best_eaten_at": "Manali local homestays", "season": "summer", "is_vegetarian": True, "key_ingredients": "Kabuli chana, yogurt, raisins, cardamom", "photo_url": "/madra.png", "trek_region": "Kullu Valley"},
            {"name": "Tudkiya Bhath", "region": "Kullu Valley", "state": "Himachal Pradesh", "category": "rice", "description": "Spiced rice dish cooked with lentils, potatoes, yogurt, and local hill spices.", "cultural_significance": "A rich one-pot meal cooked during community gatherings.", "best_eaten_at": "Kafnu village kitchens", "season": "year-round", "is_vegetarian": True, "key_ingredients": "Rice, lentils, yogurt, potatoes", "photo_url": "/tudkiya_bhath.png", "trek_region": "Kullu Valley"},

            # Nagaland
            {"name": "Smoked Pork with Bamboo Shoot", "region": "Northeast India", "state": "Nagaland", "category": "curry", "description": "Dry smoked pork slow-boiled with fermented bamboo shoot and fiery Naga king chillies.", "cultural_significance": "The pride of Angami Naga feasts, showing ancestral smoking techniques.", "best_eaten_at": "Viswema village kitchens", "season": "monsoon", "is_vegetarian": False, "key_ingredients": "Pork, bamboo shoot, Raja Mircha", "trek_region": "Northeast India"},

            # West Bengal / Sikkim
            {"name": "Momo", "region": "West Bengal", "state": "West Bengal", "category": "bread", "description": "Steamed dumplings filled with local herbs, cabbage, or chicken, served with fiery red pepper chutney.", "cultural_significance": "A daily staple that represents the convergence of Tibetan and Nepalese heritage in Darjeeling.", "best_eaten_at": "Tumling tea stalls", "season": "year-round", "is_vegetarian": True, "key_ingredients": "Flour, cabbage, ginger, garlic", "photo_url": "/momo.jpg", "trek_region": "West Bengal"},
            {"name": "Gundruk", "hindi_name": "गुंड्रुक", "region": "West Bengal", "state": "West Bengal", "category": "curry", "description": "Fermented leafy green vegetables, sun-dried and cooked into a tangy soup or side dish. A beloved Himalayan staple.", "cultural_significance": "Representing traditional food preservation, Gundruk brings deep warmth and nutrition during cold mountain journeys.", "best_eaten_at": "Tumling and Kalipokhri homestays", "season": "year-round", "is_vegetarian": True, "key_ingredients": "Fermented mustard/radish leaves, garlic, tomatoes, chillies", "photo_url": "/gundruk.jpg", "trek_region": "West Bengal"},
            {"name": "Sel Roti", "hindi_name": "सेल रोटी", "region": "West Bengal", "state": "West Bengal", "category": "bread", "description": "Ring-shaped sweet fried rice bread, crispy on the outside and soft on the inside, cooked during festive occasions.", "cultural_significance": "A traditional delicacy symbolizing good fortune and celebration, often served with warm milk tea.", "best_eaten_at": "Manebhanjan trailhead kitchens", "season": "year-round", "is_vegetarian": True, "key_ingredients": "Rice flour, sugar, ghee, cardamom, cloves", "photo_url": "/sel_roti.jpg", "trek_region": "West Bengal"},

            # Karnataka (Western Ghats / Coorg)
            {"name": "Coorg Pandi Curry", "region": "Western Ghats", "state": "Karnataka", "category": "curry", "description": "Spicy pork curry cooked with black pepper and Kachampuli (the local sour vinegar).", "cultural_significance": "The signature dish of the Kodava warriors, served at every major festival.", "best_eaten_at": "Bhattara Mane homestay", "season": "year-round", "is_vegetarian": False, "key_ingredients": "Pork, Kachampuli vinegar, pepper, spices", "trek_region": "Western Ghats"},
            {"name": "Akki Roti", "region": "Western Ghats", "state": "Karnataka", "category": "bread", "description": "Flatbread made from rice flour, minced onions, dill leaves, and green chillies.", "cultural_significance": "A healthy breakfast staple of Karnataka farmers.", "best_eaten_at": "Subramanya trailhead dhabas", "season": "year-round", "is_vegetarian": True, "key_ingredients": "Rice flour, onion, dill leaves", "trek_region": "Western Ghats"},
        ]
        
        for f in foods:
            db.session.add(LocalFood(**f))
        print(f"[+] Seeding {len(foods)} local foods.")

        # ── 7. Seeding 5 Restaurants ──────────────────────────────────
        restaurants = [
            {"name": "Bhimtal Village Dhaba", "owner_name": "Ramesh Rawat", "contact_number": "9412345678", "village": "Sankri", "region": "Garhwal Himalaya", "state": "Uttarakhand", "distance_from_trailhead_km": 0.2, "type": "dhaba", "open_season": "October to June", "speciality": "Steamed wheat Siddu served with fresh bhang chutney", "description": "A small wooden dhaba run by the Rawat family serving trekkers heading to Kedarkantha.", "status": "approved", "is_verified": True, "avg_rating": 4.7, "total_reviews": 142},
            {"name": "Nanda Devi Homestay Kitchen", "owner_name": "Geeta Devi", "contact_number": "9412345679", "village": "Lohajung", "region": "Garhwal Himalaya", "state": "Uttarakhand", "distance_from_trailhead_km": 0.5, "type": "homestay_kitchen", "open_season": "Year-round", "speciality": "Kafuli, Chainsoo, and organic Mandua rotis", "description": "Authentic Kumaoni kitchen serving fresh hot food next to the Roopkund trailhead.", "status": "approved", "is_verified": True, "avg_rating": 4.8, "total_reviews": 98},
            {"name": "Viswema Naga Kitchen", "owner_name": "Kevi Angami", "contact_number": "9856012233", "village": "Viswema", "region": "Northeast India", "state": "Nagaland", "distance_from_trailhead_km": 1.2, "type": "restaurant", "open_season": "Year-round", "speciality": "Smoked pork, boiled Galho, and Axone chutney", "description": "Traditional Naga eatery run by Angami clan women.", "status": "approved", "is_verified": True, "avg_rating": 4.6, "total_reviews": 56},
            {"name": "Bhattara Mane homestay", "owner_name": "Narayana Bhat", "contact_number": "9900223344", "village": "Subramanya Base", "region": "Western Ghats", "state": "Karnataka", "distance_from_trailhead_km": 6.5, "type": "homestay_kitchen", "open_season": "October to May", "speciality": "Simple vegetarian rice, sambar, buttermilk, and pickle on banana leaf", "description": "The legendary rest-stop enroute to Kumara Parvatha. Every trekker stops here for food and water.", "status": "approved", "is_verified": True, "avg_rating": 4.9, "total_reviews": 320},
            {"name": "Chadar Ice Cafe", "owner_name": "Lobsang Gyatso", "contact_number": "9596099988", "village": "Chilling", "region": "Ladakh", "state": "Ladakh", "distance_from_trailhead_km": 0.1, "type": "dhaba", "open_season": "January to February", "speciality": "Hot Thukpa, Ginger lemon honey tea, and Maggi", "description": "A temp stone-walled shelter near the starting point of the Chadar frozen walk.", "status": "approved", "is_verified": True, "avg_rating": 4.5, "total_reviews": 84},
        ]
        
        for r in restaurants:
            db.session.add(Restaurant(**r))
        print(f"[+] Seeding {len(restaurants)} restaurants.")

        # Find specific treks for bookings & reviews
        kedarkantha_id = next(t.id for t in seeded_treks if "Kedarkantha" in t.name)
        chadar_id = next(t.id for t in seeded_treks if "Chadar" in t.name)
        roopkund_id = next(t.id for t in seeded_treks if "Roopkund" in t.name)
        kp_id = next(t.id for t in seeded_treks if "Kumara Parvatha" in t.name)

        # ── 8. Seeding Bookings (Completed & Active) ──────────────────
        bookings = [
            {"user_id": trekker_ids[0], "trek_id": kedarkantha_id, "status": "Completed", "payment_status": "Paid", "amount_paid": 6500.0, "payment_method": "Simulated"},
            {"user_id": trekker_ids[1], "trek_id": kedarkantha_id, "status": "Completed", "payment_status": "Paid", "amount_paid": 7500.0, "payment_method": "Simulated"},
            {"user_id": trekker_ids[2], "trek_id": chadar_id, "status": "Completed", "payment_status": "Paid", "amount_paid": 35000.0, "payment_method": "Simulated"},
            {"user_id": trekker_ids[0], "trek_id": roopkund_id, "status": "Completed", "payment_status": "Paid", "amount_paid": 14000.0, "payment_method": "Simulated"},
            {"user_id": trekker_ids[1], "trek_id": kp_id, "status": "Completed", "payment_status": "Paid", "amount_paid": 3500.0, "payment_method": "Simulated"},
        ]
        
        seeded_bookings = []
        for b in bookings:
            booking_obj = Booking(
                user_id=b["user_id"],
                trek_id=b["trek_id"],
                status=b["status"],
                payment_status=b["payment_status"],
                amount_paid=b["amount_paid"],
                payment_method=b["payment_method"],
                confirmed_at=datetime.utcnow()
            )
            db.session.add(booking_obj)
            db.session.flush()
            seeded_bookings.append(booking_obj)
        print(f"[+] Seeding {len(bookings)} bookings.")

        # ── 9. Seeding Verified User Reviews ──────────────────────────
        reviews = [
            {"booking_id": seeded_bookings[0].id, "user_id": trekker_ids[0], "trek_id": kedarkantha_id, "rating": 5, "comment": "Amazing winter views! The snowy trail was clear and the guide Negi was extremely knowledgeable. Loved the Siddu enroute!", "trail_condition": "Snowy"},
            {"booking_id": seeded_bookings[1].id, "user_id": trekker_ids[1], "trek_id": kedarkantha_id, "rating": 4, "comment": "Excellent experience for a beginner like me. A bit cold, but the deodar forest snow cover was breathtaking. Highly recommend!", "trail_condition": "Snowy"},
            {"booking_id": seeded_bookings[2].id, "user_id": trekker_ids[2], "trek_id": chadar_id, "rating": 5, "comment": "Walking on Zanskar ice gorge was a spiritual encounter. The Nerak frozen waterfall is out of this world. Physically demanding but worth every step.", "trail_condition": "Icy"},
            {"booking_id": seeded_bookings[3].id, "user_id": trekker_ids[0], "trek_id": roopkund_id, "rating": 4, "comment": "Tough climb, but the mystery skeletons at the edge of the lake were visible since it wasn't fully frozen. Thrilling experience!", "trail_condition": "Rocky"},
            {"booking_id": seeded_bookings[4].id, "user_id": trekker_ids[1], "trek_id": kp_id, "rating": 5, "comment": "Kumara Parvatha forest climb was intense. The views from Shesha Parvatha are absolutely mindblowing. Bhattara Mane food is simple and heavenly.", "trail_condition": "Muddy"},
        ]
        
        for r in reviews:
            db.session.add(Review(**r))
        print(f"[+] Seeding {len(reviews)} reviews.")

        # Commit all transactions
        db.session.commit()
        print("\n[OK] Seed complete.")
        print(f"    Admin login: {app.config['ADMIN_EMAIL']} / {app.config['ADMIN_PASSWORD']}")


if __name__ == "__main__":
    seed()
