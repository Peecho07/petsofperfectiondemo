# Pets of Perfection: site audit + demo talking points

Prepared by tsKaizen · November 2026 · current site: petsofperfection.com (WordPress + Elementor)

## What's holding the current site back

1. **No services or prices on the homepage.** The homepage is three short paragraphs, then legal text. A new customer can't see what you offer or what it costs without calling.
2. **The privacy policy contradicts itself.** Section 3 says info is shared with "SMS delivery partners." Section 4 says opt-in data "will not be shared with any third parties under any circumstances." Phone carriers check this wording when they approve business texting (10DLC), so a contradiction can get texts flagged or blocked.
3. **Legal text is the main content on every page.** The full SMS terms and privacy policy are pasted onto Home, About and Contact. The policy belongs on one page, linked from the footer.
4. **No online booking.** The only form asks for name, email and a message. No phone number (even though you text customers), no pet name, breed, size or service.
5. **No photos of your work on the homepage.** You have about 288 posts on Instagram that customers never see on the site.
6. **Cats are hidden.** The About page says you groom dogs and cats, but the homepage and meta description only say dogs.
7. **Hours only appear on the Contact page.** No "open now" indicator anywhere.
8. **No reviews on the site,** even though you're rated around 4.5 on Google.
9. **Old social links.** Twitter and LinkedIn icons sit in the header on every page. Worth checking if they're still active.

## What the new site does

- **Services with clear starting prices.** Pick your dog's size (Small, Medium, Large, X-Large) and every price on the page updates.
- **A real booking request form.** Owner, phone, pet name, breed, dog or cat, size, services, preferred day (Tue to Sat only), drop-off window, notes, a vaccine confirmation and an optional SMS opt-in. Every "Book this" button opens the form with that service already ticked.
- **One clean privacy and SMS policy** that says the same thing everywhere and meets carrier wording.
- **A dedicated Cats page** with its own menu.
- **Before and after gallery** with drag sliders and filters.
- **Reviews from real customers** on the homepage and Reviews page.
- **Live "Open now / Closed" status** in the header, based on Boynton Beach time.
- **Mobile call / text / book bar** pinned to the bottom of phones.
- **Personality:** bubble-bath hero with a wagging tail, swinging dog-tag service cards, playful copy ("Fetch my appointment", "Pawsome! We'll text you to confirm.").

## Confirm with the owner before launch

- [ ] **Prices.** Every price is a SAMPLE. Replace in `tools/build.py` (DOG_SERVICES, ADDONS, CAT_SERVICES).
- [ ] **Owner and groomer names and photos** for the About page.
- [ ] **Real before and after photos** to replace the illustrations (pull from Instagram).
- [ ] **FAQ answers:** vaccine policy, typical appointment length, matting approach.
- [ ] **Cat handling claims** on the Cats page ("we'll call you if your cat is done").
- [ ] **Current Google rating** (shown as 4.5).
- [ ] **Booking form inbox:** add a Formspree endpoint in `js/config.js` so requests reach their email.
- [ ] **Boutique products** they actually carry.

## Monday call walkthrough (about 5 minutes)

1. "I pulled up your current site the way a new customer would. Two things jumped out: there are no prices, and your privacy policy says two opposite things about texting."
2. Open the demo homepage. Point out the "Open now" status, the rating and the service cards with prices.
3. Go to Services and tap the size buttons. Watch the prices change.
4. Go to Book. Show how fast the request form is, and that it collects the pet details they'd normally ask for on the phone.
5. Show the Gallery slider, then the Policies page (contradiction fixed).
6. Close: "This is yours to keep as a starting point. If you like it, I'll swap in your real prices and photos and get it live."
