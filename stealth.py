import time
from pydoll.browser.options import ChromiumOptions

def set_headless(options: ChromiumOptions) -> None:
    options.headless = True
    options.add_argument("--headless=new")  # More realistic headless mode
    options.add_argument("--enable-webgl")  # Bypasses hardware-check flags
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-popup-blocking")  # Allow popups which some sites use for login or notifications

def set_quick_stealth(options: ChromiumOptions) -> None:
    """
    For most use cases, this simple configuration provides good anti-detection

    https://pydoll.tech/docs/features/configuration/browser-preferences/?h=quick#quick-stealth-setup
    """

    # Simulate a 60-day-old browser
    fake_timestamp = int(time.time()) - (60 * 24 * 60 * 60)

    options.browser_preferences = {
        # Fake usage history
        "profile": {
            "last_engagement_time": fake_timestamp,
            "exited_cleanly": True,
            "exit_type": "Normal",
        },
        # Realistic homepage
        "homepage": "https://www.google.com",
        "session": {
            "restore_on_startup": 1,
            "startup_urls": ["https://www.google.com"],
        },
        # Enable features real users have
        "enable_do_not_track": False,  # Most users don't enable this
        "safebrowsing": {"enabled": True},
        "autofill": {"enabled": True},
        "search": {"suggest_enabled": True},
        "dns_prefetching": {"enabled": True},
    }

    # https://pydoll.tech/docs/features/configuration/browser-options/#stealth-fingerprinting
    # Make your automation harder to detect with these command-line arguments:
    # options.add_argument("--disable-blink-features=AutomationControlled")  # Hide automation flag
    options.add_argument("--use-gl=swiftshader")  # Use software rendering to bypass hardware checks
    options.webrtc_leak_protection = True  # Prevents real IP exposure through WebRTC
    # options.add_argument("--force-webrtc-ip-handling-policy=disable_non_proxied_udp")  # Prevent WebRTC IP leaks
    # options.add_argument("--no-first-run")  # Skip first run experience
    # options.add_argument("--no-default-browser-check")  # Skip default browser check
    options.add_argument("--disable-reading-from-canvas")  # Disable canvas fingerprinting
