import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import pyfiglet
import webbrowser
import subprocess
import sys
import random
from colorama import init, Fore, Back, Style
init(autoreset=True)

requirements = ['pyfiglet', 'phonenumbers','webbrowser','colorama','requests']

def install_requirements():
    for package in requirements:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
try:
    import pyfiglet
    import phonenumbers
except ImportError:
    print("Some required packages are missing. Installing them...")
    install_requirements()
print("All requirements are installed!")

telegram_channel_url = 'https://t.me/shadowprotocol01'
webbrowser.open(telegram_channel_url)

def display_made_by_mrx():
    # Generate the ASCII art text using pyfiglet
    ascii_art = pyfiglet.figlet_format("MADE BY MR-X", font="slant")
    
    # Print the ASCII art in a bordered and colorful way
    print(Fore.GREEN + "╔═════════════════════════════════════════╗")
    print(Fore.GREEN + "║" + Fore.CYAN + ascii_art.strip() + Fore.GREEN + "║")
    print(Fore.GREEN + "╚═════════════════════════════════════════╝")
#made by mrx

def get_ifsc_details(ifsc_code):
    url = f"https://ifsc.razorpay.com/{ifsc_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch IFSC details."}


def display_made_by_mrx():
    # ASCII Art for "MADE BY MR-X"
    ascii_art = pyfiglet.figlet_format("MADE BY MR-X")
    print(Fore.CYAN + ascii_art)


def ifsc_lookup():
    # Stylish Header
    display_made_by_mrx()
    
    ifsc_code = input(Fore.YELLOW + "Enter IFSC code (e.g., BKID0004952): ").strip()
    ifsc_data = get_ifsc_details(ifsc_code)
    
    # Error handling
    if "error" in ifsc_data:
        print(Fore.RED + f"Error: {ifsc_data['error']}")
    else:
        # Stylish Output
        print(Fore.CYAN + "╔════════════════════════════════════════════════════╗")
        print(Fore.MAGENTA + f"║               Bank Information for {ifsc_code}            ║")
        print(Fore.CYAN + "╠════════════════════════════════════════════════════╣")
        
        print(Fore.GREEN + f"║ Bank: {Fore.WHITE}{ifsc_data.get('BANK', 'N/A')}{" " * (40 - len(ifsc_data.get('BANK', 'N/A')))} ")
        print(Fore.GREEN + f"║ Branch: {Fore.WHITE}{ifsc_data.get('BRANCH', 'N/A')}{" " * (35 - len(ifsc_data.get('BRANCH', 'N/A')))} ")
        print(Fore.GREEN + f"║ Address: {Fore.WHITE}{ifsc_data.get('ADDRESS', 'N/A')}{" " * (30 - len(ifsc_data.get('ADDRESS', 'N/A')))} ")
        print(Fore.GREEN + f"║ State: {Fore.WHITE}{ifsc_data.get('STATE', 'N/A')}{" " * (38 - len(ifsc_data.get('STATE', 'N/A')))} ")
        print(Fore.GREEN + f"║ City: {Fore.WHITE}{ifsc_data.get('CITY', 'N/A')}{" " * (39 - len(ifsc_data.get('CITY', 'N/A')))} ")
        print(Fore.GREEN + f"║ District: {Fore.WHITE}{ifsc_data.get('DISTRICT', 'N/A')}{" " * (34 - len(ifsc_data.get('DISTRICT', 'N/A')))} ")
        print(Fore.GREEN + f"║ Contact: {Fore.WHITE}{ifsc_data.get('CONTACT', 'N/A')}{" " * (32 - len(ifsc_data.get('CONTACT', 'N/A')))} ")
        print(Fore.GREEN + f"║ UPI Enabled: {Fore.WHITE}{'Yes' if ifsc_data.get('UPI', False) else 'No'}{" " * (27 - len('Yes' if ifsc_data.get('UPI', False) else 'No'))} ")
        print(Fore.GREEN + f"║ RTGS Enabled: {Fore.WHITE}{'Yes' if ifsc_data.get('RTGS', False) else 'No'}{" " * (25 - len('Yes' if ifsc_data.get('RTGS', False) else 'No'))} ")
        print(Fore.GREEN + f"║ NEFT Enabled: {Fore.WHITE}{'Yes' if ifsc_data.get('NEFT', False) else 'No'}{" " * (26 - len('Yes' if ifsc_data.get('NEFT', False) else 'No'))} ")
        
        print(Fore.CYAN + "╚════════════════════════════════════════════════════╝")



def get_phone_info(phone_number):
    try:
        # Parse the phone number using phonenumbers library
        number = phonenumbers.parse(phone_number, None)
        country_code = phonenumbers.region_code_for_number(number)
        location = geocoder.description_for_number(number, "en") or "Location not available"
        carrier_name = carrier.name_for_number(number, "en") or "Unknown Carrier"
        country_name = geocoder.country_name_for_number(number, "en") or "Country not available"
        number_type = phonenumbers.number_type(number)
        number_type_description = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed-line",
        }.get(number_type, "Other")
        validity = "Valid" if phonenumbers.is_valid_number(number) else "Invalid"
        formatted_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        is_possible = "Possible" if phonenumbers.is_possible_number(number) else "Not possible"
        time_zones = timezone.time_zones_for_number(number)
        time_zones_description = ", ".join(time_zones) if time_zones else "Time zone information not available"
        national_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL)
        e164_format = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        rfc3966_format = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.RFC3966)
        
        # Prepare the details to be displayed
        details = {
            "Country Code": country_code,
            "Country Name": country_name,
            "Location": location,
            "Carrier": carrier_name,
            "Number Type": number_type_description,
            "Validity": validity,
            "Formatted Number": formatted_number,
            "Is Possible Number": is_possible,
            "Time Zones": time_zones_description,
            "National Number": national_number,
            "E164 Format": e164_format,
            "RFC3966 Format": rfc3966_format,
        }

        # Stylish output with colored borders and headings
        print(Fore.GREEN + "\n **Phone Number Details** ")
        print(Fore.CYAN + "╔══════════════════════════════════════════════════╗")
        print(Fore.CYAN + f"║ Phone Number: {Fore.MAGENTA}{formatted_number}   ║")
        print(Fore.CYAN + "╠══════════════════════════════════════════════════╣")
        
        # Displaying the details in a well-structured format
        for key, value in details.items():
            print(Fore.YELLOW + f"║ {Fore.WHITE}{key}: {Fore.MAGENTA}{value} ")

        print(Fore.CYAN + "╚══════════════════════════════════════════════════╝")
        print()

    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(Fore.RED + f" Number could not be parsed: {e}")


def phone_lookup():
    # Stylish prompt with a hint for the user
    print(Fore.CYAN + "Enter a valid phone number to get detailed information!\n")
    phone_number = input(Fore.YELLOW + "Enter phone number (e.g., +14155552671): ").strip()
    get_phone_info(phone_number)

def display_made_by_mrx():
    # ASCII Art for "MADE BY MR-X"
    ascii_art = pyfiglet.figlet_format("MADE BY MR-X")
    print(Fore.CYAN + ascii_art)

def whois_lookup(domain):
    url = f"https://ipwhois.app/json/{domain}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve Whois data"}

def whois_domain_lookup():
    domain = input(Fore.YELLOW + "Enter domain name (e.g., example.com): ").strip()
    whois_data = whois_lookup(domain)
    
    if "error" in whois_data:
        print(Fore.RED + f"Error: {whois_data['error']}")
    else:
        # Stylish output for Whois Information
        print(Fore.GREEN + f"\n **Whois Information for {domain}** ")
        print(Fore.CYAN + "╔══════════════════════════════════════════════════╗")
        print(Fore.CYAN + f"║ Domain: {Fore.MAGENTA}{domain}                             ║")
        print(Fore.CYAN + "╠══════════════════════════════════════════════════╣")
        
        # Displaying the Whois information in a structured format
        for key, value in whois_data.items():
            if key != 'error':  # Skip error key if present
                print(Fore.YELLOW + f"║ {Fore.WHITE}{key}: {Fore.MAGENTA}{value}                    ")
        
        print(Fore.CYAN + "╚══════════════════════════════════════════════════╝")
        print()
def main():
    display_made_by_mrx()  # Display the "MADE BY MR-X" ASCII art at the start

    print(Fore.GREEN + "Welcome to the OSINT Detective Tool! ")
    print(Fore.YELLOW + "Choose an option:".center(50, " "))
    print(Fore.CYAN + "╔══════════════════════════════════════════════════╗")
    print(Fore.CYAN + "║ 1. IFSC Lookup                                    ║")
    print(Fore.CYAN + "║ 2. Phone Number Lookup                            ║")
    print(Fore.CYAN + "║ 3. Whois Lookup                                   ║")
    print(Fore.CYAN + "║ 4. Exit                                           ║")
    print(Fore.CYAN + "╚══════════════════════════════════════════════════╝")

    while True:
        choice = input(Fore.YELLOW + "Enter your choice (1/2/3/4): ").strip()
        if choice == "1":
            print(Fore.MAGENTA + "\nYou selected IFSC Lookup. ")
            ifsc_lookup()
        elif choice == "2":
            print(Fore.MAGENTA + "\nYou selected Phone Number Lookup. ")
            phone_lookup()
        elif choice == "3":
            print(Fore.MAGENTA + "\nYou selected Whois Lookup. ")
            whois_domain_lookup()
        elif choice == "4":
            print(Fore.RED + "\nExiting the tool. Goodbye! ")
            break
        else:
            print(Fore.RED + "Invalid choice, please try again.")
#made by mrx
if __name__ == "__main__":
    main()
