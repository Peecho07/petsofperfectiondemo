/* =========================================================
   Pets of Perfection | runtime settings
   Edit these values. Nothing else needs to change.
   ========================================================= */
window.POP_CONFIG = {
  // Paste a Formspree (or similar) endpoint here to receive booking requests by email,
  // e.g. "https://formspree.io/f/abcd1234". Left empty, the form runs in demo mode:
  // it validates and shows the success screen but sends nothing.
  FORM_ENDPOINT: "",

  BUSINESS_NAME: "Pets of Perfection",
  PHONE_DISPLAY: "561-369-0913",
  PHONE_TEL: "+15613690913",
  TIMEZONE: "America/New_York",

  // Opening hours by weekday (0 = Sunday). [open, close] in 24h decimal hours.
  HOURS: {
    0: null,
    1: null,
    2: [8.5, 16],
    3: [8.5, 16],
    4: [8.5, 16],
    5: [8.5, 16],
    6: [8.5, 16]
  },

  // Days the booking form accepts (0 = Sunday). Matches HOURS above.
  BOOKABLE_DAYS: [2, 3, 4, 5, 6]
};
