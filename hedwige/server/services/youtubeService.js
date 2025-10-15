const axios = require('axios');

exports.getLikedVideos = async (accessToken) => {
    const response = await axios.get(
        'https://www.googleapis.com/youtube/v3/videos', {
        headers: { Authorization: `Bearer ${accessToken}` },
        params: {
            myRating: 'like',
            part: 'snippet',
            maxResults: 10
        }
    }
    );

    return response.data.items.map(video => ({
        id: video.id,
        title: video.snippet.title,
        thumbnail: video.snippet.thumbnails.medium.url,
        url: `https://www.youtube.com/watch?v=${video.id}`
    }));
};
