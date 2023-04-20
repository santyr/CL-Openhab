# CL-OpenHAB Plugin

*** This code is untested, and under development.***

This c-lightning plugin sends data from your c-lightning node to your OpenHAB instance using the OpenHAB API. The plugin gathers various information from your c-lightning node and updates the corresponding OpenHAB items.

## Features

- Retrieves the following data from your c-lightning node:
  - Node ID, alias, blockheight, network, and c-lightning version
  - Active channels, pending channels, and inactive channels
  - Incoming and outgoing transaction counts and amounts
  - Top 5 and bottom 5 performing peers based on earnings and forwarding events
- Automatically creates the corresponding OpenHAB items if they don't already exist
- Updates the OpenHAB items with the latest data from your c-lightning node

## Requirements

- Python 3.6 or higher
- c-lightning v0.9.3 or higher
- OpenHAB 3.x with a configured API key

## Installation

1. Clone this repository to your c-lightning plugins directory:



2. Install the required Python packages:

pip install -r requirements.txt


3. Configure the OpenHAB URL and API key in the `openhab.py` file.

4. Enable the plugin by adding the following line to your c-lightning configuration file:

plugin=/path/to/your/clightning/plugins/directory/clightning-openhab-plugin/openhab.py


5. Restart your c-lightning node.

## License

This project is licensed under the [MIT License](LICENSE).
