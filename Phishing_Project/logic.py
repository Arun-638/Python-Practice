import requests
import base64
import math
import socket
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from urllib.parse import urlparse

# --- CONFIGURATION ---
API_KEY = 'dd280f438240fd78b8ba20feb7c1adbf16efbf1ebbdfeb2334a7469e0bb7f1b5'  # <--- PASTE YOUR KEY HERE !!!
HEADERS = {"x-apikey": API_KEY}

def trace_redirects(url):
    """
    ADVANCED: Follows short links (bit.ly, etc.) to find the TRUE destination.
    """
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.head(url, allow_redirects=True, timeout=3)
        return response.url
    except:
        return url

def get_domain_age(url):
    """
    ADVANCED: Checks if the domain is 'suspiciously new'.
    (Mock function for demo purposes since real WHOIS requires paid API)
    """
    domain = urlparse(url).netloc
    # In a real app, you would query WHOIS here.
    # For this project, we assume long random domains are 'new'.
    if len(domain) > 30:
        return "NEW/UNREGISTERED"
    return "ESTABLISHED"

def get_url_reputation(url):
    """Query VirusTotal API."""
    # Step 1: Unshorten the link first!
    final_url = trace_redirects(url)
    print(f"Tracing URL: {url} -> {final_url}")
    
    try:
        url_id = base64.urlsafe_b64encode(final_url.encode()).decode().strip("=")
        api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        response = requests.get(api_url, headers=HEADERS)
        if response.status_code == 200:
            stats = response.json()['data']['attributes']['last_analysis_stats']
            return stats['malicious'], stats['suspicious'], final_url
        else:
            return 0, 0, final_url
    except Exception:
        return 0, 0, final_url

def calculate_entropy(url):
    """Calculates randomness."""
    if not url: return 0
    prob = [float(url.count(c)) / len(url) for c in dict.fromkeys(list(url))]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

def check_suspicious_keywords(url):
    """Checks for generic suspicious words."""
    url = url.lower()
    suspicious_words = [
        'secure', 'login', 'update', 'verify', 'account', 'banking', 'alert', 
        'confirm', 'signin', 'wallet', 'password', 'unlock', 'suspended',
        'free', 'generator', 'winner', 'claim', 'prize', 'gift', 'paypal'
    ]
    found_keyword = [k for k in suspicious_words if k in url]
    return found_keyword

def calculate_fuzzy_risk(malicious_votes, entropy_score, url_text):
    """
    Advanced Logic Engine
    """
    bad_keywords = check_suspicious_keywords(url_text)
    
    # BASE LOGIC
    if malicious_votes > 0:
        return 85.0 + (malicious_votes * 5) 
    
    if len(bad_keywords) > 0:
        return 65.0 # High Caution
        
    if entropy_score > 4.5:
        return 45.0

    return 10.0