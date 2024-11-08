## Running the app:
Once you have the API key setup, you are ready to run the application. Simply run the `WeatherAPI.py` script in your Python environment.

## Log File for Debugging
To help with debugging and tracking the application’s behavior, all logs are saved in a rotating log file. By default, logs are saved in `../logs/app.log`. The log file captures key events, warnings, and errors, such as API request failures, connection issues, or any other exceptions.

### How to View Logs:
- The logs will automatically rotate when they reach a size of 5MB. Old logs are archived as backup files.
- You can open `app.log` to view detailed information about the app’s operation and any errors that may occur.

## Key Features & Exception Handling

### Key Features:
- **Weather Data Retrieval**: The app retrieves weather data such as temperature, humidity, wind speed, UV index, and condition for the user-specified city.
- **Graphical UI**: The weather data is displayed in a neat and structured manner using a GUI built with Tkinter.
- **Image Display**: Weather condition icons are displayed alongside the weather information.
- **Error Handling**: The program includes robust error handling to manage:
  - Internet connection issues
  - Invalid city name or API error responses
  - Missing or invalid API key

### Exception Handling:
This project covers various potential exceptions that could cause the program to crash:

- **FileNotFoundError**: Handles missing API key file gracefully.
  - If the API key file is missing, the program will log an error and terminate without crashing.
  
- **requests.ConnectionError**: Ensures that the application won't crash if the internet is not available.
  - If there’s no internet connection, the program will notify the user and terminate gracefully.
  
- **Invalid API Response**: Handles situations where the WeatherAPI returns an error (e.g., incorrect city name or API issues).
  - If the API returns a 400 or other error codes, the program logs the error and notifies the user.

- **KeyError**: Catches cases where some weather data may be missing in the API response.
  - If any expected data is missing (e.g., condition icon or temperature), the program won’t crash but will provide a fallback value or error message.

- **Other Errors**: Catches general exceptions and ensures that the program can fail safely.

## How It Works
- When the program starts, it automatically fetches weather data for the user's current location based on their IP address.
- The user can enter a city name via a custom dialog box to fetch weather data for a specific location.
- The application displays the weather data along with an icon representing the weather condition.

## Contributing
If you would like to contribute to this project, feel free to fork the repository, create a branch, and submit a pull request with your proposed changes.

## License
This project is open-source and available under the MIT License. See the LICENSE file for more information.

## Troubleshooting
- **API Key Not Working**: Double-check that your `API_KEY.txt` file contains the correct API key and is located in the `WeatherAPI/apikey` folder.
- **No Internet Connection**: Make sure that you have an active internet connection to fetch weather data.
- **Invalid City**: If you enter an invalid city name, the program will display an error message indicating that the location could not be found.
- **Log Files**: Check the `app.log` file in the `../logs` directory for detailed error messages and application logs.
## Conclusion
This project marks an important step in my journey as a BTech 1st-year student. While I've successfully implemented the core features of the weather app, I will continue practicing and honing my skills, especially in GUI and backend development. As I gain more experience, I look forward to improving the functionality, performance, and user interface of this application.

Thank you for reviewing this project!
