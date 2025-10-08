# Gym-Class-Auto-Booking-Bot

A Python script that uses Selenium to automatically log in to a gym’s website (Demo Site: https://appbrewery.github.io/gym/) 
and book specific classes (e.g., Tuesday and Thursday at 6 PM).
It handles login, class detection, booking, and waitlists automatically.

Features:

- Automated login using saved credentials from .env

- Retry mechanism for reliable execution even if the site is slow

- Smart booking logic — books available spots or joins waitlists automatically

- Detailed summary of all actions taken (booked, waitlisted, already booked)

- Chrome user profile support to maintain session and cookies
