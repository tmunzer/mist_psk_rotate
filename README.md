# Mist PSK Rotate

This Python scripts helps Mist administrators to rotate WLAN PSK. It is designed to be manualy started or as a CRON job.

## MIT License

Copyright (c) 2021 Thomas Munzer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

 
## How it works?
1. The script will retrieve the WLAN configuration (it can be a SITE Wlan or an ORG Wlan)
2. The script will will generate a new PSK for the WLAN. The PSK strength can be configured.
3. The script will update the WLAN configuration.
4. If configured, the script will send the new PSK to the administrator(s)

<div>
<img src="https://github.com/tmunzer/mist_psk_rotate/raw/main/._readme/img/rotate.png" width="45%">
</div>
 <div>
<img src="https://github.com/tmunzer/mist_psk_rotate/raw/main/._readme/img/email.png" width="45%">
</div>

## How to use it?
1. Just install the dependencies manually or with the `requirements.txt` file. For example with `pîp -r requirements.txt`.
2. Then configure the `.env` file (an example can be found in the `example.env` file).
3. And to finish start the script with `python mist_psk_rotate.py` or `python3 mist_psk_rotate.py` depending on your system

## Configuration
### Script settings
Check the `example.env` file to know how to configure the script. You will have to create a `.env` file with the required settings.

By default, the script is looking for the `.env` file in its own directory. You can also pass the `.env` file location when running the script with the `-e` option (i.e. `python3 mist_psk_rotate.py -e <path to the env file>`).

You can use the `-c` option to check your configuration.
<div>
<img src="https://github.com/tmunzer/mist_psk_rotate/raw/main/._readme/img/check.png" width="50%">
</div>

### Email template
**Any change in the `psk_template.html` is at your own risks!**

If you want to customize the email sent to the users, you can modify the `psk_template.html` file. It's basicaly a HTML file, but:
- Be sure to use double curly brackets "{{" and "}}" instead of single curly brackets for HTML
- The script will inject 3 information in the template:
  - `{0}` will be replaced by the logo image location. It must be published on a web server and reachable by the users' devices
  - `{1}` will be replaced by the SSID name
  - `{2}` wll be replaced by the PPSK value
  - If QRcode is enabled, `{3}` wll be replaced by the QRCode information (i.e. "You can also scan the QRCode below to configure your device:")
  - If QRcode is enabled, `{4}` wll be replaced by the QRCode
