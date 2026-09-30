import os
from decimal import Decimal
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, Review
from atelier.models import CeramicShape, GlazeOption


def get_best_image(*filenames):
    """Auto-detects which file exists on disk (handles spaces, underscores, case, picX)"""
    media_dir = os.path.join(settings.MEDIA_ROOT, "products")
    for name in filenames:
        if not name:
            continue
        if os.path.exists(os.path.join(media_dir, name)):
            return f"products/{name}"
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, name)):
            return name
        norm_name = name.replace(" ", "").replace("_", "").lower()
        if os.path.exists(media_dir):
            for existing in os.listdir(media_dir):
                if existing.replace(" ", "").replace("_", "").lower() == norm_name:
                    return f"products/{existing}"
    return f"products/{filenames[0]}"


class Command(BaseCommand):
    help = "Populate the ceramic shop with aesthetic catalog products, customizer glazes, shapes and reviews"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Beginning seed process for Atelier Terra..."))

        # 1. Create Superuser & Demo User
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_superuser("admin", "admin@atelierterra.com", "admin123")
            admin_user.first_name = "Artisan"
            admin_user.last_name = "Curator"
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser 'admin' with password 'admin123'"))

        if not User.objects.filter(username="elena").exists():
            elena = User.objects.create_user("elena", "elena@example.com", "pottery123")
            elena.first_name = "Elena"
            elena.last_name = "Vance"
            elena.save()
            if hasattr(elena, 'profile'):
                elena.profile.phone = "+1 (555) 234-8901"
                elena.profile.street_address = "42 Willow Street, Apt 3B"
                elena.profile.city = "Portland"
                elena.profile.state = "OR"
                elena.profile.postal_code = "97201"
                elena.profile.save()
            self.stdout.write(self.style.SUCCESS("Created demo user 'elena' (password: pottery123)"))

        # 2. Categories
        cat_data = [
            {
                "name": "Ambient Lighting",
                "slug": "ambient-lighting",
                "description": "Architectural pleated paper shades, ceramic bases, and soft 2700K warm incandescent lighting to transform any quiet corner.",
                "icon": "fa-solid fa-lightbulb",
                "order": 1,
            },
            {
                "name": "Artisanal Vases",
                "slug": "artisanal-vases",
                "description": "Sculptural stoneware vases, fluted amphoras, and delicate bud vases designed for single wild stems and dried florals.",
                "icon": "fa-solid fa-wine-bottle",
                "order": 2,
            },
            {
                "name": "Desk & Corner Decor",
                "slug": "desk-decor",
                "description": "Tactile ceramic organizers, pencil cups, incense arches, and decorative dishes for serene, uncluttered workspaces.",
                "icon": "fa-solid fa-feather",
                "order": 3,
            },
            {
                "name": "Wallmates & Fiber Art",
                "slug": "wallmates-fiber-art",
                "description": "Hand-loomed organic linen tapestries, terracotta wall reliefs, and ceramic bead hangings that bring warmth to exposed brick and plaster walls.",
                "icon": "fa-solid fa-rug",
                "order": 4,
            },
            {
                "name": "Ceramics & Tableware",
                "slug": "ceramics-tableware",
                "description": "Hand-pinched matcha bowls, organic morning mugs, and stoneware serving dishes crafted from high-fire natural clay.",
                "icon": "fa-solid fa-mug-saucer",
                "order": 5,
            },
        ]

        categories = {}
        for c in cat_data:
            cat_obj, created = Category.objects.update_or_create(
                slug=c["slug"],
                defaults={
                    "name": c["name"],
                    "description": c["description"],
                    "icon": c["icon"],
                    "order": c["order"],
                }
            )
            categories[c["slug"]] = cat_obj
            self.stdout.write(f"Category '{cat_obj.name}' ready.")

        # 3. Products
        products_data = [
            # 1. The Hero Lamp from user photo
            {
                "category": categories["ambient-lighting"],
                "name": "The Pleated Solstice Table Lamp",
                "slug": "pleated-solstice-table-lamp",
                "tagline": "Hand-pleated paper shade on powder-coated architectural iron tripod",
                "description": (
                    "As captured in our morning atelier studio: a gentle confluence of Japanese origami precision and Scandinavian minimalism. "
                    "The Solstice lamp features a sharp, sunburst-pleated conical shade that softens illumination into a rich, golden 2700K ambient glow. "
                    "Mounted upon a clean, bent-wire architectural iron tripod with a tactile fabric braided cord. "
                    "Ideal for light oak work desks, bedside alcoves, and reading nooks."
                ),
                "story": (
                    "Inspired by the soft, diffused morning light filtered through Kyoto shoji screens. Each shade is hand-folded from heavy-weight "
                    "mulberry paper and treated with a water-resistant matte sealant. The stand is hand-welded from solid architectural steel wire."
                ),
                "price": Decimal("145.00"),
                "compare_at_price": Decimal("180.00"),
                "stock": 18,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": True,
                "nook_layer_type": "lamp",
                "image": "products/pleated_solstice_lamp.jpg",
                "material": "Architectural Iron, Heavy Mulberry Pleated Shade, Ceramic Collar",
                "dimensions": "15.5\"H x 11.2\"W x 11.2\"Base",
                "weight": "1.4 kg",
                "firing_temperature": "Metal / Paper Assembly (Ceramic Collar Cone 10)",
                "care_instructions": "Dust gently with a soft dry brush. Keep away from splashing water. E26/E27 warm LED bulb included.",
                "badge": "Signature Hero Piece"
            },
            # 2. Bud vase from photo
            {
                "category": categories["artisanal-vases"],
                "name": "Aura Fluted Bud Vase with Botanical Sprig",
                "slug": "aura-fluted-bud-vase",
                "tagline": "Petite speckled stoneware vessel for single wildflower stems",
                "description": (
                    "Designed to sit quietly alongside your workspace essentials. Cast in creamy stoneware with fine mineral speckling "
                    "and a softly flared lip. Perfect for holding fresh baby's breath, a jasmine sprig, or wild garden cuttings."
                ),
                "story": "Wheel-thrown in small batches of 20 pieces. Left unglazed on the bottom to expose the raw, sandy grain of Oregon clay.",
                "price": Decimal("48.00"),
                "compare_at_price": Decimal("58.00"),
                "stock": 25,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": True,
                "nook_layer_type": "vase",
                "image": "products/bud_vase.jpg",
                "material": "High-fire Oregon Stoneware, Food-safe Satin Glaze",
                "dimensions": "5.5\"H x 3.8\"Diameter",
                "weight": "0.45 kg",
                "firing_temperature": "Cone 10 (1280°C / 2336°F)",
                "care_instructions": "Hand wash with mild soap and warm water. Dishwasher safe on gentle cycle.",
                "badge": "Featured in Studio"
            },
            # 3. Desk Pen Cup from photo
            {
                "category": categories["desk-decor"],
                "name": "Cylindrical Oatmeal Ceramic Pen Holder",
                "slug": "cylindrical-oatmeal-pen-holder",
                "tagline": "Substantial stoneware vessel for writing tools and brushes",
                "description": (
                    "A weighted, grounded cylinder to house your favorite writing pencils, calligraphy pens, and pottery modeling tools. "
                    "Features a silky smooth matte oatmeal glaze over a warm clay body, equipped with a cork-padded bottom to protect desk surfaces."
                ),
                "story": "Created to eliminate visual clutter from the creative workspace while honoring the physical weight of pottery.",
                "price": Decimal("38.00"),
                "compare_at_price": None,
                "stock": 30,
                "is_featured": True,
                "is_bestseller": False,
                "is_nook_hero": True,
                "nook_layer_type": "cup",
                "image": "products/desk_cup.jpg",
                "material": "Stoneware Clay, Satin Oatmeal Glaze, Natural Cork Base",
                "dimensions": "4.8\"H x 3.5\"Diameter",
                "weight": "0.55 kg",
                "firing_temperature": "Cone 6 (1220°C / 2228°F)",
                "care_instructions": "Wipe clean with a damp microfiber cloth.",
                "badge": "Essential Deskware"
            },
            # 4. Wallmate Tapestry
            {
                "category": categories["wallmates-fiber-art"],
                "name": "Handwoven Botanical Tapestry Wallmate",
                "slug": "handwoven-botanical-tapestry-wallmate",
                "tagline": "Organic raw wool, linen cord, and high-fired terracotta discs",
                "description": (
                    "Woven by hand on traditional wooden floor looms using unbleached organic linen, raw merino wool fringe, "
                    "and interspersed with kiln-fired terracotta ceramic medallions. Creates an immediate focal point on exposed brick or painted plaster."
                ),
                "story": "Collaboratively crafted with generational textile weavers in Oaxaca, integrating our studio's custom fired terracotta buttons.",
                "price": Decimal("85.00"),
                "compare_at_price": Decimal("110.00"),
                "stock": 12,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": True,
                "nook_layer_type": "wallmate",
                "image": "products/wallmate_tapestry.jpg",
                "material": "Raw Organic Linen, Merino Wool, Hand-turned Oak Rod, Terracotta Discs",
                "dimensions": "28\"H x 14\"W (plus hanging cord)",
                "weight": "0.85 kg",
                "firing_temperature": "Ceramic elements Cone 10 (1280°C)",
                "care_instructions": "Shake gently outdoors to release dust. Spot clean fabric with cool damp cloth if necessary.",
                "badge": "Handmade Wallmate"
            },
            # 5. Donut Vase
            {
                "category": categories["artisanal-vases"],
                "name": "Wabi-Sabi Sandstone Donut Vase",
                "slug": "wabi-sabi-sandstone-donut-vase",
                "tagline": "Sculptural hollow-ring silhouette with tactile sand glaze",
                "description": (
                    "A striking circular geometry that frames light and negative space. The textured sandstone finish invites touch, "
                    "making it as much an architectural sculpture as a functional vessel for eucalyptus stems or pampas grass."
                ),
                "story": "Hand-built using coil and pinch techniques, celebrating natural organic asymmetry and clay texture.",
                "price": Decimal("74.00"),
                "compare_at_price": Decimal("90.00"),
                "stock": 14,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": False,
                "image": "products/donut_vase.jpg",
                "material": "Coarse Sandstone Stoneware, Textured Natural Sand Glaze",
                "dimensions": "9.2\"H x 8.5\"W x 2.8\"D",
                "weight": "1.3 kg",
                "firing_temperature": "Cone 10 Reduction Firing",
                "care_instructions": "Rinse interior with warm water. Exterior is water-safe.",
                "badge": "Sculptural Form"
            },
            # 6. Moon Jar
            {
                "category": categories["artisanal-vases"],
                "name": "Arcadia Moon Jar in Speckled Oatmeal",
                "slug": "arcadia-moon-jar-speckled-oatmeal",
                "tagline": "Voluminous sphere inspired by classic Korean Joseon pottery",
                "description": (
                    "A homage to historic moon jars with an understated modern profile. Thrown in two hemispheres joined at the waist, "
                    "resulting in an unhurried, organic fullness that brings serenity to any mantelpiece or credenza."
                ),
                "story": "Fired in a wood-burning anagama kiln for 48 hours, leaving subtle kiss marks of natural ash upon the clay belly.",
                "price": Decimal("110.00"),
                "compare_at_price": None,
                "stock": 8,
                "is_featured": True,
                "is_bestseller": False,
                "is_nook_hero": False,
                "image": "products/moon_jar.jpg",
                "material": "Stoneware Clay, Iron-speckled White Satin Glaze",
                "dimensions": "10.5\"H x 10\"Diameter",
                "weight": "2.1 kg",
                "firing_temperature": "Cone 10 (1280°C / 2336°F)",
                "care_instructions": "Hand wash only. Watertight interior for lush floral bouquets.",
                "badge": "Limited Kiln Run"
            },
            # 7. Fluted Amphora
            {
                "category": categories["artisanal-vases"],
                "name": "Sculptural Ribbed Amphora Vase",
                "slug": "sculptural-ribbed-amphora-vase",
                "tagline": "Earthy terracotta vessel with vertical carved fluting",
                "description": (
                    "Classic Mediterranean proportions reimagined with Scandinavian restraint. The surface is carved by hand while leather-hard, "
                    "creating rhythmic vertical grooves that catch the light throughout the day."
                ),
                "story": "Created using rich iron terracotta clay sourced directly from riverbed deposits in the Pacific Northwest.",
                "price": Decimal("95.00"),
                "compare_at_price": Decimal("115.00"),
                "stock": 16,
                "is_featured": False,
                "is_bestseller": True,
                "is_nook_hero": False,
                "image": "products/fluted_amphora.jpg",
                "material": "Red Terracotta Clay, Matte Iron Wash",
                "dimensions": "12.0\"H x 7.2\"Diameter",
                "weight": "1.7 kg",
                "firing_temperature": "Cone 8 (1240°C)",
                "care_instructions": "Hand wipe with dry or lightly moistened cloth.",
                "badge": "Carved by Hand"
            },
            # 8. Mushroom Lamp
            {
                "category": categories["ambient-lighting"],
                "name": "Kumo Ceramic Mushroom Lamp",
                "slug": "kumo-ceramic-mushroom-lamp",
                "tagline": "Hand-turned stoneware dome shade with warm diffused downlight",
                "description": (
                    "An enchanting silhouette that evokes peaceful woodland flora. The entire dome shade is hand-thrown ceramic, "
                    "channeling light downward in an intimate pool of golden radiance that warms bedside tables and coffee nooks."
                ),
                "story": "Designed for ritual unwinding in the evening. Integrated rotary brass dimmer switch on cord.",
                "price": Decimal("120.00"),
                "compare_at_price": Decimal("140.00"),
                "stock": 10,
                "is_featured": True,
                "is_bestseller": False,
                "is_nook_hero": True,
                "nook_layer_type": "lamp",
                "image": "products/mushroom_lamp.jpg",
                "material": "Glazed Stoneware Dome, Heavy Ceramic Base, Solid Brass Hardware",
                "dimensions": "11\"H x 9.5\"Shade Diameter",
                "weight": "2.2 kg",
                "firing_temperature": "Cone 10 (1280°C)",
                "care_instructions": "Unplug before cleaning. Wipe ceramic surfaces with dry lint-free cloth.",
                "badge": "Best for Bedroom"
            },
            # 9. Incense Arch
            {
                "category": categories["desk-decor"],
                "name": "Zenith Stoneware Incense Arch",
                "slug": "zenith-stoneware-incense-arch",
                "tagline": "Architectural bridge burner with raw clay catch tray",
                "description": (
                    "Turn your fragrance ritual into an aesthetic ceremony. The suspended arch suspends a single Japanese incense stick "
                    "over an elongated terracotta tray, catching delicate ash with effortless grace."
                ),
                "story": "Engineered for standard bamboo and coreless dhoop incense sticks. Made with heat-resistant refractory grog clay.",
                "price": Decimal("42.00"),
                "compare_at_price": None,
                "stock": 22,
                "is_featured": False,
                "is_bestseller": False,
                "is_nook_hero": True,
                "nook_layer_type": "cup",
                "image": "products/incense_arch.jpg",
                "material": "Grog Stoneware, Unglazed Terracotta Bed",
                "dimensions": "6.2\"L x 2.4\"W x 3.5\"H",
                "weight": "0.38 kg",
                "firing_temperature": "Cone 10 (1280°C)",
                "care_instructions": "Empty ash into garden or bin. Wash tray with warm soapy water periodically.",
                "badge": "Daily Ritual"
            },
            # 10. Matcha Bowl
            {
                "category": categories["ceramics-tableware"],
                "name": "Hand-pinched Wabi-Sabi Matcha Bowl",
                "slug": "hand-pinched-wabi-sabi-matcha-bowl",
                "tagline": "Organic rim chawan with mossy celadon glaze pool",
                "description": (
                    "Formed slowly by thumb and fingers to create comfortable thumb-rests and a satisfying tactile heft in both hands. "
                    "The interior wells feature a pooling crackled celadon glaze that turns vibrant green under whisked matcha."
                ),
                "story": "Created following traditional Japanese Kurinuki and pinch pottery philosophies.",
                "price": Decimal("52.00"),
                "compare_at_price": Decimal("65.00"),
                "stock": 18,
                "is_featured": False,
                "is_bestseller": True,
                "is_nook_hero": True,
                "nook_layer_type": "bowl",
                "image": "products/matcha_bowl.jpg",
                "material": "Stoneware Clay, Crackle Celadon Glaze",
                "dimensions": "4.9\"Diameter x 3.1\"H",
                "weight": "0.42 kg",
                "firing_temperature": "Cone 10 (1280°C)",
                "care_instructions": "Hand rinse with warm water immediately after use. Do not microwave.",
                "badge": "Tea Ceremony"
            },
            # 11. Fluted Mug
            {
                "category": categories["ceramics-tableware"],
                "name": "Fluted Ceramic Mug with Sand Glaze",
                "slug": "fluted-ceramic-mug-sand-glaze",
                "tagline": "Ergonomic two-finger pulled handle with rhythmic ridges",
                "description": (
                    "Your companion for slow morning brew and pour-over coffee. The ribbed exterior offers tactile traction and heat dissipation, "
                    "while the pulled handle balances the mug effortlessly in hand."
                ),
                "story": "Holds 12 fl oz comfortably. Food-safe, lead-free glaze formulated from natural feldspar and wood ash.",
                "price": Decimal("34.00"),
                "compare_at_price": None,
                "stock": 35,
                "is_featured": False,
                "is_bestseller": False,
                "is_nook_hero": True,
                "nook_layer_type": "cup",
                "image": "products/fluted_mug.jpg",
                "material": "Stoneware Clay, Cream Sand Satin Glaze",
                "dimensions": "3.8\"H x 3.4\"Diameter (12 oz capacity)",
                "weight": "0.38 kg",
                "firing_temperature": "Cone 10 (1280°C)",
                "care_instructions": "Microwave and dishwasher safe.",
                "badge": "Everyday Warmth"
            },

            # --- Extra 13 Products from Collection (Auto-Detecting User Filenames) ---
            # 1. Wallmate (Disc Tapestry)
            {
                "category": categories["wallmates-fiber-art"],
                "name": "Terracotta Solstice Disc Wallmate",
                "slug": "terracotta-solstice-disc-wallmate",
                "tagline": "Minimalist clay spheres suspended on raw organic linen cord",
                "description": "A serene meditation in geometry and negative space. Hand-rolled terracotta ceramic discs suspended from a solid turned oak dowel with organic unbleached linen threads.",
                "story": "Each terracotta disc is burnished by hand with river stones before firing to give a soft, buttery matte sheen.",
                "price": Decimal("65.00"),
                "compare_at_price": Decimal("80.00"),
                "stock": 14,
                "is_featured": True,
                "is_bestseller": False,
                "is_nook_hero": True,
                "nook_layer_type": "wallmate",
                "image": get_best_image("wallmate_disc.jpg", "pic1.jpg", "pic 1.jpg", "wallmate_tapestry.jpg"),
                "material": "High-fired Terracotta, Natural Oak Dowel, Organic Linen Cord",
                "dimensions": "24\"H x 12\"W",
                "weight": "0.65 kg",
                "firing_temperature": "Cone 6 (1220°C)",
                "care_instructions": "Dust gently with dry cloth. For indoor use.",
                "badge": "New Arrival"
            },
            # 2. Tripod Lamp
            {
                "category": categories["ambient-lighting"],
                "name": "Nordic Pleated Desk Lamp with Tripod Base",
                "slug": "nordic-pleated-desk-lamp-tripod",
                "tagline": "Architectural white tripod lamp with pleated origami shade",
                "description": "Clean Scandinavian lines combined with cozy 2700K incandescent warmth. The white wire tripod base provides balanced stability without visual weight.",
                "story": "Handcrafted to create the ultimate reading and writing sanctuary beside your ceramic collection.",
                "price": Decimal("135.00"),
                "compare_at_price": Decimal("165.00"),
                "stock": 20,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": True,
                "nook_layer_type": "lamp",
                "image": get_best_image("tripod_lamp.jpg", "pic2.jpg", "pic 2.jpg", "pleated_solstice_lamp.jpg"),
                "material": "Architectural White Steel, Pleated Mulberry Paper, Brass Fittings",
                "dimensions": "15.0\"H x 11.0\"W",
                "weight": "1.35 kg",
                "firing_temperature": "Fabricated Steel & Ceramic E27 Socket",
                "care_instructions": "Clean shade with feather duster. Unplug before bulb change.",
                "badge": "Atelier Favorite"
            },
            # 3. Botanical Foliage Vase
            {
                "category": categories["artisanal-vases"],
                "name": "Verdant Foliage Hand-Painted Ceramic Vase",
                "slug": "verdant-foliage-hand-painted-vase",
                "tagline": "Botanical monstera & palm brushwork on crackled stoneware",
                "description": "Bring lush botanical energy indoors. Substantial vase featuring rich emerald and forest green leaves meticulously painted by hand over textured porcelain slip.",
                "story": "Painted individually with traditional cobalt and iron underglazes before a 1280°C kiln firing.",
                "price": Decimal("115.00"),
                "compare_at_price": Decimal("140.00"),
                "stock": 10,
                "is_featured": True,
                "is_bestseller": False,
                "is_nook_hero": False,
                "image": get_best_image("botanical_vase.jpg", "pic13.jpg", "pic 13.jpg", "pic3.jpg", "pic 3.jpg"),
                "material": "Stoneware Clay, Botanical Underglazes, Clear Satin Glaze",
                "dimensions": "14.5\"H x 7.5\"Diameter",
                "weight": "2.4 kg",
                "firing_temperature": "Cone 10 (1280°C)",
                "care_instructions": "Watertight interior. Hand wash gently.",
                "badge": "Hand-Painted"
            },
            # 4. Interlocking Heart Vase
            {
                "category": categories["artisanal-vases"],
                "name": "Harmonia Interlocking Heart Ceramic Vase",
                "slug": "harmonia-interlocking-heart-vase",
                "tagline": "Sculptural matte white heart cutout duo for dried botanical stems",
                "description": "A graceful symbolic study in union and sculptural form. The hollow heart aperture frames light beautifully while supporting tall plumes of fluffy pampas grass.",
                "story": "Cast in premium matte unglazed bisque porcelain with a soft-touch stone texture.",
                "price": Decimal("89.00"),
                "compare_at_price": Decimal("110.00"),
                "stock": 16,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": False,
                "image": get_best_image("heart_vase.jpg", "pic12.jpg", "pic 12.jpg", "pic4.jpg", "pic 4.jpg"),
                "material": "Fine Bisque Porcelain, Soft Matte Tactile Finish",
                "dimensions": "10.2\"H x 8.0\"W x 3.2\"D",
                "weight": "1.2 kg",
                "firing_temperature": "Cone 9 (1260°C)",
                "care_instructions": "Wipe with a damp sponge. Best paired with dried or faux botanicals.",
                "badge": "Sculptural Art"
            },
            # 5. Calla Petal Vase
            {
                "category": categories["artisanal-vases"],
                "name": "Calla Petal Sculptural Ceramic Pitcher Vase",
                "slug": "calla-petal-sculptural-pitcher-vase",
                "tagline": "Dramatic organic petal flare mouth with integrated loop handle",
                "description": "Modeled after the graceful unfolding of a blooming calla lily flower. The swooping organic lip cradles long cut stems while the integrated handle adds classical charm.",
                "story": "Hand-carved and pulled from a single block of porcelain clay by master ceramic artisans.",
                "price": Decimal("98.00"),
                "compare_at_price": Decimal("125.00"),
                "stock": 12,
                "is_featured": False,
                "is_bestseller": True,
                "is_nook_hero": False,
                "image": get_best_image("calla_lily_vase.jpg", "pic5.jpg", "pic 5.jpg", "pic10.jpg"),
                "material": "High-fired Fine Porcelain, Gloss White Glaze",
                "dimensions": "13.0\"H x 7.8\"W x 6.5\"D",
                "weight": "1.6 kg",
                "firing_temperature": "Cone 10 (1280°C)",
                "care_instructions": "Hand wash with warm soapy water. 100% watertight.",
                "badge": "Collector's Piece"
            },
            # 6. Shelf Decor Ensemble
            {
                "category": categories["desk-decor"],
                "name": "Nordic Kinfolk Minimalist Shelf Decor Ensemble",
                "slug": "nordic-kinfolk-shelf-decor-ensemble",
                "tagline": "Harmonious 8-piece ceramic curation: arches, knot, torso & fluted vessels",
                "description": "Everything needed to style an entire bookcase, credenza, or mantle. Includes textured ceramic knot, classical bust figurine, arch vase, footed bowl, and candlesticks.",
                "story": "Curated in-house to bring the timeless Scandinavian warmth and tranquility of slow living into your home.",
                "price": Decimal("165.00"),
                "compare_at_price": Decimal("210.00"),
                "stock": 8,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": False,
                "image": get_best_image("kinfolk_shelf.jpg", "pic9.jpg", "pic 9.jpg", "pic6.jpg", "pic 6.jpg"),
                "material": "Natural Sandstone Ceramic, Matte Sand Glaze, Unfinished Clay",
                "dimensions": "Varies by piece (4\" to 10\" Height)",
                "weight": "3.8 kg (Set)",
                "firing_temperature": "Cone 8 to 10",
                "care_instructions": "Dust with dry soft cloth. Individual pieces can be rearranged freely.",
                "badge": "Curated Set"
            },
            # 7. Double Loop Vase
            {
                "category": categories["artisanal-vases"],
                "name": "Serpentine Double-Loop Sandstone Vase",
                "slug": "serpentine-double-loop-sandstone-vase",
                "tagline": "Organic dual-neck curving arch sculpture with rough sand grain",
                "description": "An eye-catching topological wonder. Two intertwining loop necks provide twin receptacles for dried lotus seed heads, fluffy grasses, and wild stems.",
                "story": "Hand-built in the atelier through continuous coil wrapping and slab sculpting techniques.",
                "price": Decimal("88.00"),
                "compare_at_price": Decimal("105.00"),
                "stock": 15,
                "is_featured": False,
                "is_bestseller": False,
                "is_nook_hero": False,
                "image": get_best_image("double_loop_vase.jpg", "pic7.jpg", "pic 7.jpg"),
                "material": "Textured Grog Clay, Sand Dune Matte Finish",
                "dimensions": "11.2\"H x 8.4\"W x 3.6\"D",
                "weight": "1.45 kg",
                "firing_temperature": "Cone 10 (1280°C)",
                "care_instructions": "Wipe with soft lint-free cloth. Safe for water and botanicals.",
                "badge": "Architectural Form"
            },
            # 8. Pastel Swan Sculpture
            {
                "category": categories["desk-decor"],
                "name": "Pastel Luster Ceramic Swan & Swirl Sculpture",
                "slug": "pastel-luster-ceramic-swan-sculpture",
                "tagline": "Hand-pinched iridescent swirl figurines in blush pink and mint glaze",
                "description": "Delicate curves and iridescent luster finish capture light and serenity. Features fluid abstract avian and infinity ribbons that evoke grace.",
                "story": "Glazed with double-dipped low-fire opalescent luster finishes in an artisan studio.",
                "price": Decimal("55.00"),
                "compare_at_price": Decimal("70.00"),
                "stock": 18,
                "is_featured": False,
                "is_bestseller": False,
                "is_nook_hero": False,
                "image": get_best_image("pastel_swan.jpg", "pic8.jpg", "pic 8.jpg"),
                "material": "White Ceramic Earthenware, Pearlescent Pastel Glaze",
                "dimensions": "7.5\"H x 5.2\"W x 3.0\"D",
                "weight": "0.75 kg",
                "firing_temperature": "Cone 04 Luster Firing (1060°C)",
                "care_instructions": "Gently wipe with microfiber cloth. Keep out of harsh direct sunlight.",
                "badge": "Artisan Sculpture"
            },
            # 9. Tender Embrace Trio
            {
                "category": categories["desk-decor"],
                "name": "Tender Embrace Ceramic Silhouette & Candlestick Trio",
                "slug": "tender-embrace-silhouette-candlestick-trio",
                "tagline": "Family silhouette with cutout heart, arch vase & twisted candlesticks",
                "description": "A heartfelt focal arrangement representing unity and love. Includes an abstract parent-and-child statue with heart, arch vessel, and winding candle holders.",
                "story": "Sculpted by hand to honor meaningful human connection and peaceful evening candlelight.",
                "price": Decimal("105.00"),
                "compare_at_price": Decimal("130.00"),
                "stock": 11,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": False,
                "image": get_best_image("tender_embrace.jpg", "pic6.jpg", "pic 6.jpg", "pic9.jpg", "pic 9.jpg"),
                "material": "Fine Earthenware Clay, Satin Sage & Peach Slip",
                "dimensions": "Statue: 8.2\"H, Holders: 9.0\"H",
                "weight": "1.8 kg (Set)",
                "firing_temperature": "Cone 6 (1220°C)",
                "care_instructions": "Wax drops can be removed by freezing for 15 minutes and gently popping off.",
                "badge": "Heartfelt Gift"
            },
            # 10. Lotus Candle & Tray Set
            {
                "category": categories["desk-decor"],
                "name": "Lotus Bloom Candle Bowl & Ribbed Vase Coffee Table Set",
                "slug": "lotus-bloom-candle-bowl-tray-set",
                "tagline": "Fluted matte ceramic vase and lotus flower candle vessel on oval tray",
                "description": "Designed for cozy coffee tables and restful living spaces. Includes a scalloped lotus-petal wax bowl, fluted cylindrical flower vase, and matching pill-shaped tray.",
                "story": "Infused with natural soy wax and clean cotton wicks for 45 hours of soothing candlelight.",
                "price": Decimal("78.00"),
                "compare_at_price": Decimal("95.00"),
                "stock": 20,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": False,
                "image": get_best_image("lotus_tray.jpg", "pic10.jpg", "pic 10.jpg", "pic5.jpg"),
                "material": "Stoneware Ceramic, Soy Wax Candle, Natural Fiber Wick",
                "dimensions": "Tray: 11\"L x 5.5\"W, Vase: 6.5\"H",
                "weight": "1.5 kg",
                "firing_temperature": "Cone 8 (1240°C)",
                "care_instructions": "Refillable candle bowl. Trim wick to 1/4 inch before each lighting.",
                "badge": "Cozy Living"
            },
            # 11. Spiral & Donut Vase Trio
            {
                "category": categories["artisanal-vases"],
                "name": "Trilogy Spiral & Donut Earth Vase Ensemble",
                "slug": "trilogy-spiral-donut-earth-vase-ensemble",
                "tagline": "Mocha, ivory and espresso hollow circle ceramic vases with globe candles",
                "description": "Geometric tranquility in warm earth tones. Three graduating donut and spiral ceramic sculptures accompanied by pair of matching stoneware tea light spheres.",
                "story": "Inspired by planetary orbits and Zen rock gardens, bringing organic grounding to any room.",
                "price": Decimal("118.00"),
                "compare_at_price": Decimal("145.00"),
                "stock": 14,
                "is_featured": False,
                "is_bestseller": True,
                "is_nook_hero": False,
                "image": get_best_image("donut_spiral_trio.jpg", "pic4.jpg", "pic 4.jpg", "pic11.jpg", "pic 11.jpg"),
                "material": "Stoneware Ceramic, Sand Matte Earth Glazes",
                "dimensions": "Large Vase: 10\"H, Medium: 7.5\"H, Small: 5.5\"H",
                "weight": "2.6 kg (Ensemble)",
                "firing_temperature": "Cone 10 (1280°C)",
                "care_instructions": "Dust regularly with soft dry brush.",
                "badge": "Trio Ensemble"
            },
            # 12. Ocean Glaze Dining Set
            {
                "category": categories["ceramics-tableware"],
                "name": "Emerald Tide Artisanal Ceramic Dining Set (16-Piece)",
                "slug": "emerald-tide-ceramic-dining-set",
                "tagline": "Hand-painted ocean watercolor glaze stoneware with gold rim accent",
                "description": "Transform every gathering into an unforgettable feast. Features swirling turquoise and deep sea-green hand-painted scalloped washes, rimmed in 14k gold luster.",
                "story": "Individually brush-glazed by hand so that no two dining plates have the exact same ocean pattern.",
                "price": Decimal("220.00"),
                "compare_at_price": Decimal("275.00"),
                "stock": 6,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": False,
                "image": get_best_image("emerald_dining_set.jpg", "pic2.jpg", "pic 2.jpg", "pic12.jpg", "pic 12.jpg"),
                "material": "High-fire Porcelain-Stoneware, Reactive Ocean Glaze, Gold Rim",
                "dimensions": "Plates: 10.5\" & 8.5\", Bowls: 6.5\" Diameter",
                "weight": "8.5 kg (Complete Set)",
                "firing_temperature": "Cone 10 High Fire (1280°C)",
                "care_instructions": "Hand washing recommended to preserve gold luster rims.",
                "badge": "Banquet Set"
            },
            # 13. Reading Planter
            {
                "category": categories["desk-decor"],
                "name": "The Literary Sprout Rocking Chair Planter",
                "slug": "literary-sprout-rocking-chair-planter",
                "tagline": "Adorable smiling ceramic character reading a book on rocking chair",
                "description": "The most heartwarming addition to any plant parent's desk or windowsill! This whimsical ceramic friend happily reads a little book while sitting on a miniature wooden rocking chair.",
                "story": "Created to bring an instant smile to your face during busy study or work hours. Includes drainage hole.",
                "price": Decimal("42.00"),
                "compare_at_price": Decimal("52.00"),
                "stock": 25,
                "is_featured": True,
                "is_bestseller": True,
                "is_nook_hero": True,
                "nook_layer_type": "cup",
                "image": get_best_image("reading_planter.jpg", "pic1.jpg", "pic 1.jpg", "pic13.jpg", "pic 13.jpg"),
                "material": "Terracotta Ceramic, Natural Walnut Wood Rocker",
                "dimensions": "5.5\"H x 4.2\"W x 4.0\"D",
                "weight": "0.5 kg",
                "firing_temperature": "Cone 6 (1220°C)",
                "care_instructions": "Includes bottom drainage hole and plastic nursery liner.",
                "badge": "Cutest Bestseller"
            },
        ]

        for p in products_data:
            prod_obj, created = Product.objects.update_or_create(
                slug=p["slug"],
                defaults=p
            )
            self.stdout.write(f"Product '{prod_obj.name}' ready.")

            # Add Reviews for key products
            if p["slug"] == "pleated-solstice-table-lamp":
                Review.objects.get_or_create(
                    product=prod_obj,
                    name="Clara M.",
                    title="The most soothing light in my study",
                    defaults={
                        "rating": 5,
                        "comment": "The pleated paper shade casts the warmest, softest glow across my exposed brick desk. The wire tripod stand is sturdy yet looks weightless. It feels like an authentic artisan piece from Kyoto or Copenhagen.",
                        "verified_purchase": True,
                        "is_approved": True,
                    }
                )
                Review.objects.get_or_create(
                    product=prod_obj,
                    name="Henrik S.",
                    title="Exquisite craft & packaging",
                    defaults={
                        "rating": 5,
                        "comment": "Arrived securely packaged in biodegradable pine wrap. The fabric cord and ceramic collar show remarkable attention to detail. Worth every penny.",
                        "verified_purchase": True,
                        "is_approved": True,
                    }
                )
            elif p["slug"] == "aura-fluted-bud-vase":
                Review.objects.get_or_create(
                    product=prod_obj,
                    name="Maya K.",
                    title="The sweetest little desk vase",
                    defaults={
                        "rating": 5,
                        "comment": "Sits right next to my Solstice lamp with a single branch of olive leaves. The mineral speckling in the glaze gives it so much depth and warmth.",
                        "verified_purchase": True,
                        "is_approved": True,
                    }
                )

        # 4. Atelier Customizer Shapes
        shapes_data = [
            {
                "name": "The Pleated Solstice Table Lamp",
                "slug": "custom-pleated-solstice-lamp",
                "category_label": "Ambient Lighting",
                "description": "Hand-pleated conical shade paired with custom-glazed ceramic collar and architectural wire tripod stand.",
                "base_price": Decimal("145.00"),
                "dimensions": "15.5\"H x 11.2\"W",
                "shape_code": "pleated_lamp",
                "order": 1,
            },
            {
                "name": "Sculptural Fluted Amphora Vase",
                "slug": "custom-fluted-amphora-vase",
                "category_label": "Artisanal Vase",
                "description": "Dramatic ribbed curves with hand-turned neck and organic handles, finished in your bespoke glaze formulation.",
                "base_price": Decimal("95.00"),
                "dimensions": "12.0\"H x 7.2\"W",
                "shape_code": "fluted_vase",
                "order": 2,
            },
            {
                "name": "Wabi-Sabi Donut Moon Flask",
                "slug": "custom-donut-moon-flask",
                "category_label": "Artisanal Vase",
                "description": "Hollow-ring sculptural vessel celebrating negative space and tactile ceramic textures.",
                "base_price": Decimal("74.00"),
                "dimensions": "9.2\"H x 8.5\"W",
                "shape_code": "donut_flask",
                "order": 3,
            },
            {
                "name": "Minimalist Desk Tool Vessel",
                "slug": "custom-desk-tool-vessel",
                "category_label": "Desk Decor",
                "description": "Weighted cylindrical organizer for pens, brushes, or dried stems with cork-dampened base.",
                "base_price": Decimal("38.00"),
                "dimensions": "4.8\"H x 3.5\"W",
                "shape_code": "desk_cup",
                "order": 4,
            },
            {
                "name": "Organic Hand-Pinched Tea Chawan",
                "slug": "custom-tea-chawan",
                "category_label": "Ceramics & Tableware",
                "description": "Tactile ceremonial tea bowl with unique pinch marks, custom fired in our high-temperature kiln.",
                "base_price": Decimal("52.00"),
                "dimensions": "4.9\"D x 3.1\"H",
                "shape_code": "tea_bowl",
                "order": 5,
            },
        ]

        for s in shapes_data:
            shape_obj, created = CeramicShape.objects.update_or_create(
                slug=s["slug"],
                defaults=s
            )
            self.stdout.write(f"Atelier Shape '{shape_obj.name}' ready.")

        # 5. Atelier Glazes
        glazes_data = [
            {
                "name": "Speckled Oatmeal",
                "hex_color": "#F2EDE4",
                "accent_color": "#DFD5C6",
                "texture_type": "speckled",
                "description": "Silky satin cream infused with volcanic basalt flecks and unhurried warmth.",
                "price_modifier": Decimal("0.00"),
                "badge": "Signature Glaze",
            },
            {
                "name": "Raw Fired Terracotta",
                "hex_color": "#C4704F",
                "accent_color": "#A65636",
                "texture_type": "terracotta_raw",
                "description": "Unfiltered natural red clay with iron-rich warmth and authentic porous tactile feel.",
                "price_modifier": Decimal("0.00"),
                "badge": "Earthy Heritage",
            },
            {
                "name": "Sage Celadon Mist",
                "hex_color": "#8F9F8B",
                "accent_color": "#73846F",
                "texture_type": "satin_matte",
                "description": "Subtle botanical green with soft celadon micro-crystalline pools.",
                "price_modifier": Decimal("6.00"),
                "badge": "Artisan Choice",
            },
            {
                "name": "Warm Biscuit Sandstone",
                "hex_color": "#D9C4A5",
                "accent_color": "#BFA886",
                "texture_type": "speckled",
                "description": "Toasted golden undertones mimicking dune sandstones and calm morning shores.",
                "price_modifier": Decimal("0.00"),
                "badge": "",
            },
            {
                "name": "Matte Alabaster Cream",
                "hex_color": "#FAF7F0",
                "accent_color": "#E8E2D3",
                "texture_type": "satin_matte",
                "description": "Pure chalky satin white with zero glare, reflecting soft window daylight.",
                "price_modifier": Decimal("4.00"),
                "badge": "Clean Japandi",
            },
            {
                "name": "Midnight Basalt",
                "hex_color": "#383431",
                "accent_color": "#242220",
                "texture_type": "speckled",
                "description": "Deep moody charcoal stoneware with tiny sparkling feldspar crystals.",
                "price_modifier": Decimal("8.00"),
                "badge": "Limited Edition",
            },
        ]

        for g in glazes_data:
            glaze_obj, created = GlazeOption.objects.update_or_create(
                name=g["name"],
                defaults=g
            )
            self.stdout.write(f"Glaze Option '{glaze_obj.name}' ready.")

        self.stdout.write(self.style.SUCCESS("Atelier Terra database successfully seeded with all aesthetic ceramic catalog items!"))