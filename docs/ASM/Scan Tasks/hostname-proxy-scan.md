# Hostname Proxy Scan

## Implementation Details

### Main Goal

- Identify the asset's Proxy (CDN) in use
- Identify the WAF protection against few general type of attacks
- Should help customer to see what assets are unprotected by proxy/waf 

### Asset Type
Runs on each **Hostname** discovered.

Uses the first IP address of the **Hostname** to scan through.

### Output
All results are displayed on the separate screen: Protections

Each task has a logs with the detection progress results

### Rules/Configs Impact
There are no any Rules that has an integration with this scan task.

However there is an org level Setting that controls WAF detection logic.

Org -> Settings -> Attack Surface Management -> Enable WAF detection

- If On: Run basic attacks against the asset to determine potential WAF protection
- If Off: No any attacks will be run through the asset

### Workflow
- **Step1**: Run IP addresses lookup using `dig`
    - Run  `whois`  for all `A` records
        - Run proxy detection algorithm on the `whois` output. 
    - Save all detected Proxies before next step
- **Step2**: Send `GET` request to `https://` schema. If port :443 is not reachable - run `http://` request. 
    - Run through all response headers and try to determine the Proxy
    - Save all results before next step
- **Step3**: Run only if Settings -> ... -> ASM WAF Detection is ON  
    - Run basic `GET` request and check the code
        - If code in 2XX range, proceed with attacks:
            - Run each attack type through the hostname and validate response code. If it's in 4XX range - mark as WAF protecgted.
    - Save all results and exti

## QA Check List

- **Step1**: Run IP addresses lookup using `dig`
    - Validate `dig` lookup for Top Proxies we support
    - Validate proxy detection for one A record per hostname
    - Validate few A records for the same CDN per hostname
    - Validate mix A records for two CDN's under the same hostname
    - Validate AAAA records on the hostname
    - Validate unresolvable hostname

## Top Proxies
Edgio (EdgeCast / Limelight / Layer0), Amazon Cloudfront, CloudFlare, Akamai, MS Azure, F5
