# PingNetwork Waitlist Automation

Automates email registration for the [PingNetwork waitlist](https://pingnetwork.io/#waitlist) using Playwright. Supports proxy rotation, random delays, and error handling.

## Features
- Registers emails from `emails.txt`
- Uses proxies from `proxies.txt`
- Short delays (0.5–2s) for UI loading
- Long delays (60–180s) with countdown timer
- Continues on errors

## Prerequisites
- Python 3.8+
- Playwright
- `emails.txt` and `proxies.txt`

## Installation
1. Clone repo:
   ```bash
   git clone https://github.com/your-username/pingnetwork-wl
   cd pingnetwork-waitlist
   ```
2. Install dependencies:
   ```bash
   pip install playwright
   playwright install
   ```

## Configuration
- **emails.txt**: One email per line, e.g.:
  ```
  email1
  email2
  ```
- **proxies.txt**: One proxy per line with http://, e.g.:
  ```
  http://user:pass@proxy1.com:8080
  http://proxy2.com:8080
  ```

## Usage
Run:
```bash
python ping.py
```
Output shows loaded emails/proxies, registration status, and countdown timers.

## Troubleshooting
- **Selector errors**: Check button/form selectors in browser inspector (F12).
- **Single email processed**: Ensure `emails.txt` has multiple entries.
- **Form not loading**: Increase `wait_for_selector` timeout to 60000ms.
- **Proxy errors**: Verify proxy format in `proxies.txt`.

## Notes
- Runs in non-headless mode. Set `headless=True` for silent operation.
- Ensure proxies support HTTPS.

## License
MIT License. See [LICENSE](LICENSE).
