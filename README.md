# SpotiPulse

SpotiPulse is a FastAPI-based application that integrates with the Spotify API to provide various functionalities, such as displaying your top tracks, showing the currently playing song, and managing playback. This project is designed to be deployed as part of your portfolio website.

## Features

- **Top Tracks**: Fetch and display your top 10 tracks from Spotify.
- **Now Playing**: Show the song currently playing on your Spotify account.
- **Followed Artists**: List the artists you follow on Spotify.
- **Playback Control**: Stop the currently playing song or start playing any of your top 10 tracks.

## Requirements

- Python 3.13 or higher
- Spotify Developer Account

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/SpotiPulse.git
   cd SpotiPulse
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.sample.env` to `.env`:

     ```bash
     cp .sample.env .env
     ```

   - Fill in your Spotify API credentials in the `.env` file.

## Usage

1. Run the application:

   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

2. Access the API at `http://localhost:8000`.

## API Endpoints

- `GET /spotify/top-tracks`: Returns your top 10 tracks.
- `GET /spotify/now-playing`: Shows the currently playing song.
- `GET /spotify/followed-artists`: Lists the artists you follow.
- `PUT /spotify/pause`: Stops the currently playing song.
- `PUT /spotify/play`: Starts playing a specified track.

## Deployment

This application is designed to be deployed as part of your portfolio website. You can use Docker for deployment:

1. Build the Docker image:

   ```bash
   docker build -t spotipulse .
   ```

2. Run the Docker container:

   ```bash
   docker run -d -p 8000:8000 --env-file .env spotipulse
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Spotify API](https://developer.spotify.com/documentation/web-api/)
