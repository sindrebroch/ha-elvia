# Elvia for HomeAssistant

![GitHub release (latest by date)](https://img.shields.io/github/v/release/sindrebroch/ha-elvia?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sindrebroch)

HomeAssistant-integration for Elvia

## Requirements

- Metering point id. Log into [Elvia](https://www.elvia.no/minside) and find your ID.
- API-key. Sign up for GridTariffAPI at [Elvia developer portal](https://elvia.portal.azure-api.net/) and you will receive an API-key via email. See [API-doc](https://assets.ctfassets.net/jbub5thfds15/1mF3J3xVf9400SDuwkChUC/a069a61a0257ba8c950432000bdefef3/Elvia_GridTariffAPI_for_smart_house_purposes_v1_1_20210212.doc.pdf) for more info.

## Installation

<details>
   <summary>HACS (Recommended)</summary>

   1. Ensure that [HACS](https://hacs.xyz/) is installed.
   2. Add this repository as a custom repository
   3. Search for and install the "Elvia" integration.
   4. Restart Home Assistant.
   5. Add the `Elvia` integration to HA from the integration-page
</details>

<details>
   <summary>Manual installation</summary>

   1. Download the `Source code (zip)` file from the
      [latest release](https://github.com/sindrebroch/ha-elvia/releases/latest).
   2. Unpack the release and copy the `custom_components/elvia` directory
      into the `custom_components` directory of your Home Assistant
      installation.
   3. Restart Home Assistant.
   4. Add the `Elvia` integration to HA from the integration-page
</details>


## Sensors
- Kapasitetsledd
- Forbruksledd


## Debugging
If something is not working properly, logs might help with debugging. To turn on debug-logging add this to your `configuration.yaml`
```
logger:
  default: info
  logs:
    custom_components.elvia: debug
```

## API limitations
Limited to 200 calls/hour/user. The integration normally polls once every hour.

## Inspiration
https://github.com/uphillbattle/NettleieElvia
