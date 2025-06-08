# Trello Automation Project

A sophisticated Python-based automation system developed for a travel agency to monitor and track flight schedule changes. This project automates the process of checking flight schedules for sold tickets, ensuring travel agents can proactively notify their clients about any schedule modifications.

## 🎯 Project Purpose

This automation system was specifically designed to solve a critical business need for a travel agency:
- Automatically monitor all sold flight tickets
- Detect schedule changes in flight itineraries
- Enable proactive client communication about flight modifications
- Streamline the process of managing multiple flight bookings
- Reduce manual checking time and potential human errors

## 🚀 Features

- **Flight Schedule Monitoring**: Automated checking of flight schedules for all sold tickets
- **Trello Board Integration**: Organized tracking of flight changes using Trello boards
- **Automated Notifications**: System for flagging and managing schedule changes
- **Comment Review System**: Automated processing of flight change notifications
- **Robust Logging**: Comprehensive logging system for tracking all flight checks
- **Error Handling**: Sophisticated error management for reliable operation
- **Environment Configuration**: Secure configuration management using environment variables

## 🛠️ Technical Stack

- Python 3.x
- Trello REST API
- Selenium WebDriver
- Requests library
- Python-dotenv for environment management

## 📋 Prerequisites

- Python 3.x installed
- Trello API credentials
- Required Python packages (listed in requirements.txt)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/trello_automation.git
cd trello_automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with your Trello API credentials:
```
TRELLO_API_KEY=your_api_key
TRELLO_TOKEN=your_token
```

## 💻 Usage

The project can be run with different commands:

```bash
# Run the main automation process
python main.py

# Review comments
python main.py review

# Reset last update
python main.py reset
```

## 📁 Project Structure

- `main.py` - Entry point of the application
- `trello_api.py` - Trello API integration
- `automation.py` - Core automation logic
- `scraper.py` - Web scraping functionality
- `util.py` - Utility functions
- `file_manager.py` - File management operations
- `logfiles/` - Directory containing operation logs

## 🔍 Key Features in Detail

### Flight Monitoring System
- Automated checking of flight schedules for sold tickets
- Real-time detection of schedule changes
- Organized tracking of modifications in Trello
- Efficient handling of multiple flight bookings

### Automation System
- Automated card updates and management
- Intelligent comment processing for flight changes
- Tag management for different types of schedule modifications
- Batch processing of multiple flight checks

### Error Handling
- Comprehensive error catching and logging
- Graceful failure recovery
- Detailed logging for debugging
- Automatic retry mechanisms for failed checks

### Security
- Secure credential management
- Environment variable configuration
- Protected API key handling
- Safe storage of flight booking information

## 📝 Logging

The system maintains detailed logs in the `logfiles` directory, tracking:
- Program execution
- API interactions
- Error occurrences
- Operation timestamps

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

[Your Name] - [Your Portfolio/GitHub]

## 🔗 Links

- [Trello API Documentation](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/)
- [Project Repository](https://github.com/yourusername/trello_automation)

## 💼 Business Impact

This automation system provided significant benefits to the travel agency:
- Reduced manual checking time by 90%
- Improved accuracy in detecting flight changes
- Enhanced client satisfaction through proactive notifications
- Streamlined workflow for travel agents
- Better organization of flight change tracking
- Reduced risk of missing important schedule modifications
